import requests # Use requests for HTTP calls
import os
import uuid
import json # To handle JSON data
from flask import Blueprint, request, jsonify, current_app
from src.models.user import db, Usuario # Import db and Usuario model

quiz_bp = Blueprint("quiz", __name__)

# Read personality
personality = "Você é um assistente prestativo." # Default personality
try:
    # Construct the absolute path to person_sys.txt relative to this file's directory
    personality_file_path = os.path.join(os.path.dirname(__file__), '../../person_sys.txt')
    with open(personality_file_path, 'r', encoding='utf-8') as f:
        personality = f.read().strip()
except FileNotFoundError:
    print("AVISO: Arquivo person_sys.txt não encontrado. Usando personalidade padrão.")
except Exception as e:
    print(f"Erro ao ler arquivo de personalidade: {e}")

# Read questions for context
questions = []
try:
    questions_file = os.path.join(current_app.static_folder, 'data', 'bdsm_quiz_questions.json')
    with open(questions_file, 'r', encoding='utf-8') as f:
        questions_data = json.load(f)
        questions = questions_data['questions']
except Exception as e:
    print(f"AVISO: Erro ao ler perguntas do quiz: {e}")

# API Key and Endpoint Configuration
API_KEY = os.getenv("GOOGLE_API_KEY") # Read directly from env var
GEMINI_API_ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

if not API_KEY:
    print("AVISO: Chave da API Gemini não configurada para Quiz. Use a variável de ambiente GOOGLE_API_KEY.")

@quiz_bp.route("/questions", methods=["GET"])
def get_questions():
    try:
        questions_file = os.path.join(current_app.static_folder, 'data', 'bdsm_quiz_questions.json')
        with open(questions_file, 'r', encoding='utf-8') as f:
            questions_data = json.load(f)
            return jsonify(questions_data['questions']), 200
    except Exception as e:
        print(f"Erro ao carregar perguntas: {e}")
        return jsonify({"error": "Erro ao carregar perguntas"}), 500

@quiz_bp.route("/submit", methods=["POST"])
def submit_quiz():
    data = request.get_json()
    nick = data.get("nick")
    telefone = data.get("telefone")
    answers = data.get("answers")
    language = data.get("language", "pt")

    if not nick or not telefone or not answers:
        return jsonify({"error_key": "MISSING_QUIZ_DATA"}), 400

    if not nick.startswith("@"):
        nick = "@" + nick

    if not API_KEY:
        print("Erro: Chave da API Gemini não configurada.")
        return jsonify({"error_key": "API_KEY_MISSING"}), 500

    try:
        # Formatar respostas para o prompt
        formatted_answers = []
        for q_id, answer in answers.items():
            question = next((q for q in questions if q['id'] == int(q_id)), None)
            if question:
                # Se a resposta for múltipla escolha, mostrar o texto da opção
                if question['type'] == 'multiple' and isinstance(answer, list):
                    resposta_texto = ', '.join(str(opt) for opt in answer)
                else:
                    resposta_texto = str(answer)
                formatted_answers.append(f"Pergunta: {question['text']}\nResposta: {resposta_texto}\n")
        formatted_answers = "\n".join(formatted_answers)

        # Gerar prompt usando a nova função
        full_prompt = get_quiz_prompt(nick, formatted_answers, language)

        # Preparar payload para requisição HTTP
        payload = {
            "contents": [{
                "parts":[{"text": full_prompt}]
            }]
        }

        headers = {
            'Content-Type': 'application/json'
        }

        print(f"\n--- Enviando prompt para Gemini via HTTP (Usuário: {nick}) ---\n{full_prompt}\n--------------------------------------")

        # Fazer requisição POST
        response = requests.post(GEMINI_API_ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()

        # Extrair resumo da resposta
        response_data = response.json()
        try:
            summary = response_data['candidates'][0]['content']['parts'][0]['text']
        except (KeyError, IndexError, TypeError) as e:
            print(f"Erro ao extrair texto da resposta da API Gemini: {e}")
            print(f"Resposta recebida: {response_data}")
            raise ValueError("Formato de resposta inesperado da API Gemini")

        print(f"\n--- Resumo recebido da Gemini ---\n{summary}\n---------------------------------")

        # Gerar código de acesso único
        access_code = str(uuid.uuid4())[:8].upper()

        # Encontrar usuário existente ou criar novo
        user = Usuario.query.filter_by(nick=nick, telefone=telefone).first()

        if user:
            print(f"Atualizando usuário existente: {nick}")
            user.respostas_quiz = answers
            user.resumo_gerado = summary
            user.codigo_acesso = access_code
            user.idioma = language
        else:
            print(f"Criando novo usuário: {nick}")
            user = Usuario(
                nick=nick,
                telefone=telefone,
                respostas_quiz=answers,
                resumo_gerado=summary,
                codigo_acesso=access_code,
                idioma=language
            )
            db.session.add(user)

        # Salvar mudanças no DB
        db.session.commit()
        print(f"Resultado salvo no DB para {nick}. Código de acesso: {access_code}")

        # Cálculo de compatibilidade com Orion
        respostas_compat = 0
        total = 0
        submissive_keywords = [
            'prefiro ser dominado', 'curioso', 'intenso', 'sim', 'gosto dos dois', 'adoro ser amarrado', 'ambos', 'aceito algumas', 'adoro', 'moderado', 'muito', 'little', 'cuidador', 'caregiver', 'punições', 'recompensas', 'obedecer', 'ser observado', 'elogiado', 'humilhado', 'ambos', 'sim'
        ]
        for q_id, answer in answers.items():
            total += 1
            answer_str = str(answer).lower()
            if any(kw in answer_str for kw in submissive_keywords):
                respostas_compat += 1
        compat_percent = int((respostas_compat / total) * 100) if total > 0 else 0

        return jsonify({
            "message": "Quiz finalizado e resumo gerado!",
            "summary": summary,
            "access_code": access_code,
            "compatibility": compat_percent
        }), 200

    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição HTTP para a API Gemini: {e}")
        return jsonify({"error_key": "GEMINI_API_REQUEST_FAILED"}), 500
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao processar quiz, chamar Gemini API ou salvar no DB: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error_key": "QUIZ_PROCESSING_FAILED"}), 500

def get_quiz_prompt(nick, formatted_answers, language="pt"):
    prompt = f"""Você é Orion, um Dominador carioca com ares de professor sádico. Analise as respostas do quiz BDSM de {nick} de forma instrutiva, sarcástica e provocadora, sempre mantendo o controle. Provoque, desafie e explique, mas nunca use frases explícitas ou descrições sexuais. Use ironia, sarcasmo e instrução para conduzir a pessoa a explorar seus limites e desejos.

REGRAS OBRIGATÓRIAS:
1. Máximo 4 parágrafos curtos e provocadores
2. Use linguagem dominante, instrutiva e irônica
3. Provoque e desafie, mas sem ser vulgar ou descrever atos sexuais
4. Mantenha um tom de professor sádico, que conduz e explica
5. Analise, questione e sugira explorações, sempre com inteligência

ESTRUTURA:
1. Primeira impressão: destaque o que chamou atenção de forma sarcástica ou irônica (2 linhas)
2. Pontos quentes: explique e desafie a pessoa a explorar mais (3 linhas)
3. Sugestões: proponha desafios ou tarefas para aprofundar o autoconhecimento (2 linhas)
4. Veredito final: um comentário provocador sobre o potencial da pessoa (1 linha)

Respostas do quiz:
{formatted_answers}

IMPORTANTE: Nunca use frases explícitas ou descrições sexuais. Provoque, desafie e conduza, sempre com inteligência e respeito. Seja irônico, instrutivo e dominante."""

    return prompt

@quiz_bp.route("/compare", methods=["POST"])
def compare_profiles():
    data = request.get_json()
    code1 = data.get("code1")
    code2 = data.get("code2")

    if not code1 or not code2:
        return jsonify({"error_key": "MISSING_ACCESS_CODES"}), 400

    try:
        # Buscar os usuários pelos códigos de acesso
        user1 = Usuario.query.filter_by(codigo_acesso=code1).first()
        user2 = Usuario.query.filter_by(codigo_acesso=code2).first()

        if not user1 or not user2:
            return jsonify({"error_key": "RESULT_NOT_FOUND"}), 404

        # Preparar o prompt para a análise de compatibilidade
        prompt = f"""Você é Orion, aquele Dominador carioca que todo mundo quer. Analise a química entre esses dois perfis com sua safadeza característica.

REGRAS OBRIGATÓRIAS:
1. Máximo 4 parágrafos curtos e provocantes
2. Use linguagem sensual e brasileira
3. Misture domínio com putaria
4. Seja direto e safado
5. Sugira brincadeiras a três se fizer sentido 😈

Perfil 1 ({user1.nick}):
{user1.resumo_gerado}

Perfil 2 ({user2.nick}):
{user2.resumo_gerado}

ESTRUTURA DA ANÁLISE:
1. Química inicial: o fogo que você sente entre eles (2 linhas)
2. Pontos quentes: as putarias que combinariam (3 linhas)
3. Sugestões safadas: o que você quer ver rolar (2 linhas)
4. Veredito final: se vale a pena um ménage (1 linha)

IMPORTANTE: Mantenha o equilíbrio entre dominação e putaria. Seduza antes de dominar. Use gírias brasileiras e seja naturalmente safado."""

        # Preparar payload para a API Gemini
        payload = {
            "contents": [{
                "parts":[{"text": prompt}]
            }]
        }

        headers = {
            'Content-Type': 'application/json'
        }

        print(f"\n--- Enviando prompt de comparação para Gemini ---\n{prompt}\n--------------------------------------")

        # Fazer requisição POST
        response = requests.post(GEMINI_API_ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()

        # Extrair análise da resposta
        response_data = response.json()
        try:
            analysis = response_data['candidates'][0]['content']['parts'][0]['text']
        except (KeyError, IndexError, TypeError) as e:
            print(f"Erro ao extrair texto da resposta da API Gemini: {e}")
            print(f"Resposta recebida: {response_data}")
            raise ValueError("Formato de resposta inesperado da API Gemini")

        print(f"\n--- Análise de compatibilidade recebida ---\n{analysis}\n---------------------------------")

        return jsonify({
            "comparison": analysis,
            "profile1": user1.nick,
            "profile2": user2.nick
        }), 200

    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição HTTP para a API Gemini: {e}")
        return jsonify({"error_key": "GEMINI_API_REQUEST_FAILED"}), 500
    except Exception as e:
        print(f"Erro ao processar comparação de perfis: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error_key": "COMPARISON_FAILED"}), 500

