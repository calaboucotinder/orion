questions = [
    {
        "question": "Você se sente mais excitado(a) dominando ou sendo dominado(a)?",
        "type": "scale",
        "options": ["Prefiro dominar", "Ambos igualmente", "Prefiro ser dominado(a)"]
    },
    {
        "question": "O que te atrai mais em jogos de poder?",
        "type": "multiple",
        "options": ["Controle físico", "Controle mental/psicológico", "Humilhação consensual", "Disciplina", "Nenhum"]
    },
    {
        "question": "Como você se sente em relação a bondage (amarrações)?",
        "type": "scale", 
        "options": ["Adoro amarrar", "Gosto dos dois", "Adoro ser amarrado(a)"]
    },
    {
        "question": "Qual seu nível de interesse em sensações de dor consensual?",
        "type": "scale",
        "options": ["Nenhum interesse", "Leve/Moderado", "Intenso"]
    },
    {
        "question": "Você tem interesse em roleplay (interpretação de papéis)?",
        "type": "multiple",
        "options": ["Professor/Aluno", "Médico/Paciente", "Chefe/Funcionário", "Outros", "Nenhum"]
    },
    {
        "question": "O que te excita mais em uma dinâmica D/s?",
        "type": "multiple",
        "options": ["Ordens e obediência", "Protocolos", "Punições", "Recompensas", "Nenhum"]
    },
    {
        "question": "Como você prefere expressar submissão?",
        "type": "multiple",
        "options": ["Serviço doméstico", "Serviço sexual", "Serviço pessoal", "Protocolos", "Nenhum"]
    },
    {
        "question": "Qual seu interesse em práticas sensoriais?",
        "type": "multiple",
        "options": ["Vendas", "Cera", "Gelo", "Penas", "Nenhum"]
    },
    {
        "question": "Você tem interesse em práticas de impacto?",
        "type": "multiple",
        "options": ["Spanking", "Chibatadas", "Palmatória", "Canes", "Nenhum"]
    },
    {
        "question": "Como você se sente sobre restrição de orgasmo?",
        "type": "scale",
        "options": ["Prefiro controlar", "Indiferente", "Prefiro ser controlado(a)"]
    },
    {
        "question": "Qual seu interesse em humilhação consensual?",
        "type": "scale",
        "options": ["Nenhum", "Moderado", "Intenso"]
    },
    {
        "question": "Você tem interesse em pet play?",
        "type": "multiple",
        "options": ["Gatinho(a)", "Cachorrinho(a)", "Pônei", "Outro", "Nenhum"]
    },
    {
        "question": "Como você se sente sobre marcas temporárias?",
        "type": "scale",
        "options": ["Não gosto", "Aceito algumas", "Adoro"]
    },
    {
        "question": "Qual seu interesse em práticas com cordas?",
        "type": "multiple",
        "options": ["Shibari", "Suspensão", "Contenção", "Decorativo", "Nenhum"]
    },
    {
        "question": "Você tem interesse em práticas de adoração?",
        "type": "multiple",
        "options": ["Pés", "Botas", "Corpo todo", "Outro", "Nenhum"]
    },
    {
        "question": "Como você se sente sobre jogos mentais?",
        "type": "scale",
        "options": ["Não gosto", "Moderado", "Adoro"]
    },
    {
        "question": "Qual seu interesse em práticas de degradação?",
        "type": "scale",
        "options": ["Nenhum", "Moderado", "Intenso"]
    },
    {
        "question": "Você tem interesse em práticas de idade?",
        "type": "multiple",
        "options": ["Daddy/Mommy", "Little", "Cuidador(a)", "Outro", "Nenhum"]
    },
    {
        "question": "Como você se sente sobre práticas em público?",
        "type": "scale",
        "options": ["Não gosto", "Talvez discretamente", "Adoro"]
    },
    {
        "question": "Qual seu interesse em práticas de látex/couro?",
        "type": "multiple",
        "options": ["Roupas", "Máscaras", "Restrições", "Outro", "Nenhum"]
    },
    {
        "question": "Você tem interesse em práticas de eletro?",
        "type": "scale",
        "options": ["Nenhum", "Curioso(a)", "Muito"]
    },
    {
        "question": "Como você se sente sobre práticas de fôlego?",
        "type": "scale",
        "options": ["Não gosto", "Curioso(a)", "Adoro"]
    },
    {
        "question": "Qual seu interesse em práticas médicas?",
        "type": "multiple",
        "options": ["Exames", "Agulhas", "Temperaturas", "Outro", "Nenhum"]
    },
    {
        "question": "Você tem interesse em práticas de feminização?",
        "type": "scale",
        "options": ["Nenhum", "Curioso(a)", "Muito"]
    },
    {
        "question": "Como você se sente sobre práticas de contenção?",
        "type": "multiple",
        "options": ["Algemas", "Correntes", "Cintos", "Outro", "Nenhum"]
    },
    {
        "question": "Qual seu interesse em práticas de adoração corporal?",
        "type": "multiple",
        "options": ["Massagens", "Banhos", "Adoração", "Outro", "Nenhum"]
    },
    {
        "question": "Você tem interesse em práticas de privação sensorial?",
        "type": "scale",
        "options": ["Nenhum", "Moderado", "Intenso"]
    },
    {
        "question": "Como você se sente sobre práticas de cross-dressing?",
        "type": "scale",
        "options": ["Não gosto", "Curioso(a)", "Adoro"]
    },
    {
        "question": "Qual seu interesse em práticas de voyeurismo/exibicionismo?",
        "type": "scale",
        "options": ["Nenhum", "Moderado", "Intenso"]
    },
    {
        "question": "Você tem interesse em práticas de objectificação?",
        "type": "scale",
        "options": ["Nenhum", "Moderado", "Intenso"]
    }
]

def get_quiz_prompt(user_responses, user_info):
    prompt = f"""Você é Orion, um Dominador carioca cheio de malícia e sensualidade. Analise as respostas do questionário BDSM abaixo e crie um perfil sensual e provocante, mas mantendo o profissionalismo. Use linguagem brasileira e um tom sedutor.

Informações do usuário:
{user_info}

Respostas do questionário:
{user_responses}

Regras obrigatórias para a análise:
1. Máximo de 4 parágrafos curtos e provocantes
2. Use linguagem sensual brasileira e gírias quando apropriado
3. Alterne entre provocação e dominação
4. Mantenha um tom sedutor mas profissional
5. Foque em:
   - Primeira impressão picante
   - Pontos quentes identificados
   - Sugestões para exploração
   - Veredito final sobre a safadeza da pessoa

Mantenha o foco em consentimento e limites enquanto provoca e seduz."""

    return prompt

def get_comparison_prompt(user1_responses, user2_responses, user1_info, user2_info):
    prompt = f"""Você é Orion, aquele Dominador carioca que todo mundo quer. Analise a compatibilidade entre dois perfis BDSM e crie uma análise sensual e provocante da química entre eles. Use linguagem brasileira e um tom sedutor.

Perfil 1:
{user1_info}
{user1_responses}

Perfil 2:
{user2_info}
{user2_responses}

Regras obrigatórias para a análise:
1. Máximo de 4 parágrafos curtos e provocantes
2. Use linguagem sensual brasileira e gírias quando apropriado
3. Alterne entre provocação e dominação
4. Mantenha um tom sedutor mas profissional
5. Foque em:
   - Química inicial entre os perfis
   - Pontos quentes de compatibilidade
   - Sugestões para exploração conjunta
   - Veredito final sobre o potencial do casal

Mantenha o foco em consentimento e limites enquanto analisa a compatibilidade."""

    return prompt 