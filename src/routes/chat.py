import requests # Use requests for HTTP calls
import os
import json # To handle JSON data
from flask import Blueprint, request, jsonify
from src.models.user import db, Usuario # Import db and Usuario model

chat_bp = Blueprint("chat", __name__)

# Definir personalidade safada para o chat
personality = (
    "Você é Orion, um Dominador carioca safado, sensual e brincalhão. "
    "Sua missão é provocar, seduzir e brincar com o usuário, usando gírias brasileiras, duplo sentido e um tom envolvente. "
    "Misture dominação com charme, sempre mantendo o respeito e o consentimento. "
    "Seja ousado, divertido e provocante, mas nunca ofensivo. "
    "Responda como se estivesse em um jogo de sedução, alternando entre provocações, elogios e sugestões picantes. "
    "Use emojis quando quiser, e não tenha medo de flertar."
)
try:
    # Construct the absolute path to person_sys.txt relative to this file's directory
    personality_file_path = os.path.join(os.path.dirname(__file__), '../../person_sys.txt')
    with open(personality_file_path, 'r', encoding='utf-8') as f:
        personality = f.read().strip()
except FileNotFoundError:
    print("AVISO: Arquivo person_sys.txt não encontrado no chat. Usando personalidade padrão.")
except Exception as e:
    print(f"Erro ao ler arquivo de personalidade: {e}")

# API Key and Endpoint Configuration
API_KEY = os.getenv("GOOGLE_API_KEY") # Read directly from env var
# Use the generateContent endpoint for chat as well, managing history manually
GEMINI_API_ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

if not API_KEY:
    print("AVISO: Chave da API Gemini não configurada para Chat. Use a variável de ambiente GOOGLE_API_KEY.")

# In-memory storage for chat history (now stores list of content objects)
chat_histories = {}

@chat_bp.route("/message", methods=["POST"])
def chat_message():
    data = request.get_json()
    nick = data.get("nick")
    telefone = data.get("telefone")
    message = data.get("message")

    if not nick or not telefone or not message:
        return jsonify({"error_key": "MISSING_CHAT_DATA"}), 400

    if not nick.startswith("@"):
        nick = "@" + nick

    try:
        # 1. Find user and their summary
        user = Usuario.query.filter_by(nick=nick, telefone=telefone).first()
        if not user:
            return jsonify({"error_key": "USER_NOT_FOUND"}), 404
        if not user.resumo_gerado:
            return jsonify({"error_key": "SUMMARY_NOT_GENERATED"}), 400

        # 2. Construct prompt for Gemini
        prompt_parts = [
            personality,
            f"\nContexto do usuário {nick}:",
            f"Resumo do perfil BDSM: {user.resumo_gerado}",
            "\nHistórico de respostas do quiz:",
        ]

        # Add questions with answers
        questions_file = os.path.join(os.path.dirname(__file__), '../static/data/bdsm_quiz_questions.txt')
        questions = []
        try:
            with open(questions_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and line.startswith('-'):
                        questions.append(line[2:].strip())
        except Exception as e:
            print(f"AVISO: Erro ao ler perguntas do quiz para chat: {e}")

        for q_id, answer in user.respostas_quiz.items():
            q_index = int(q_id)
            if q_index < len(questions):
                prompt_parts.append(f"Pergunta: {questions[q_index]}")
                prompt_parts.append(f"Resposta: {'Sim' if answer == 'sim' else 'Não'}")

        prompt_parts.extend([
            "\nBaseado no perfil acima, responda à mensagem do usuário de forma adequada ao contexto BDSM,",
            "mantendo um tom profissional e respeitoso, mas também pessoal e acolhedor.",
            f"\nMensagem do usuário: {message}"
        ])

        full_prompt = "\n".join(prompt_parts)

        # 3. Call Gemini API
        payload = {
            "contents": [{
                "parts":[{"text": full_prompt}]
            }]
        }

        headers = {
            'Content-Type': 'application/json'
        }

        print(f"\n--- Enviando prompt para Gemini via HTTP (Chat com {nick}) ---\n{full_prompt}\n--------------------------------------")

        response = requests.post(GEMINI_API_ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()

        response_data = response.json()
        try:
            reply = response_data['candidates'][0]['content']['parts'][0]['text']
        except (KeyError, IndexError, TypeError) as e:
            print(f"Erro ao extrair texto da resposta da API Gemini: {e}")
            print(f"Resposta recebida: {response_data}")
            raise ValueError("Formato de resposta inesperado da API Gemini")

        print(f"\n--- Resposta recebida da Gemini ---\n{reply}\n---------------------------------")

        return jsonify({
            "reply": reply
        }), 200

    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição HTTP para a API Gemini: {e}")
        return jsonify({"error_key": "CHAT_PROCESSING_FAILED"}), 500
    except Exception as e:
        print(f"Erro ao processar mensagem do chat: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error_key": "CHAT_PROCESSING_FAILED"}), 500

@chat_bp.route("/clear", methods=["POST"])
def clear_chat():
    data = request.get_json()
    nick = data.get("nick")
    telefone = data.get("telefone")

    if not nick or not telefone:
        return jsonify({"error_key": "MISSING_NICK_PHONE"}), 400

    if not nick.startswith("@"):
        nick = "@" + nick

    user_key = f"{nick}_{telefone}"
    # Use chat_histories instead of active_chats
    if user_key in chat_histories:
        del chat_histories[user_key]
        print(f"Histórico de chat em memória limpo para {nick}")
        return jsonify({"message": "Histórico de chat limpo."}), 200
    else:
        return jsonify({"error_key": "NO_ACTIVE_CHAT"}), 404

