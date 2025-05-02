from flask import Blueprint, request, jsonify
from src.models.user import db, Usuario # Import db and Usuario model

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register_user():
    print("\n=== INÍCIO DO PROCESSAMENTO DE REGISTRO ===")
    print("Headers recebidos:", dict(request.headers))
    
    data = request.get_json()
    print("Dados recebidos:", data)
    
    nick = data.get("nick")
    telefone = data.get("telefone")
    
    print("Dados extraídos:", {
        "nick": nick,
        "telefone": telefone
    })

    if not nick or not telefone:
        print("Erro: Dados obrigatórios faltando")
        return jsonify({"error_key": "MISSING_NICK_PHONE"}), 400

    if not nick.startswith("@"):
        nick = "@" + nick
        print("Nick atualizado com @:", nick)

    try:
        print("Verificando usuário existente...")
        existing_user = Usuario.query.filter((Usuario.nick == nick) | (Usuario.telefone == telefone)).first()

        if existing_user:
            if existing_user.nick == nick and existing_user.telefone == telefone:
                print(f"Usuário existente encontrado: {nick} com telefone {telefone}")
                response_data = {
                    "message": "Usuário já registrado.",
                    "nick": existing_user.nick,
                    "telefone": existing_user.telefone
                }
                print("Resposta:", response_data)
                return jsonify(response_data), 200
            else:
                field_taken = "nick" if existing_user.nick == nick else "telefone"
                print(f"Conflito: {field_taken} já está em uso")
                return jsonify({"error_key": "FIELD_ALREADY_TAKEN", "field": field_taken}), 409

        print(f"Novo usuário: {nick} com telefone {telefone}")
        response_data = {
            "message": "Informações validadas. Prossiga para o quiz.",
            "nick": nick,
            "telefone": telefone
        }
        print("Resposta:", response_data)
        print("=== FIM DO PROCESSAMENTO DE REGISTRO ===\n")
        return jsonify(response_data), 200

    except Exception as e:
        print(f"Erro ao verificar/registrar usuário: {e}")
        db.session.rollback()
        return jsonify({"error_key": "INTERNAL_SERVER_ERROR"}), 500

@auth_bp.route("/retrieve", methods=["POST"])
def retrieve_results():
    data = request.get_json()
    nick = data.get("nick")
    telefone = data.get("telefone")
    codigo_acesso = data.get("codigo_acesso")

    if not (nick and telefone) and not codigo_acesso:
         # Return error key
         return jsonify({"error_key": "MISSING_RETRIEVAL_IDENTIFIER"}), 400

    try:
        user = None
        if codigo_acesso:
            user = Usuario.query.filter_by(codigo_acesso=codigo_acesso).first()
        elif nick and telefone:
            if not nick.startswith("@"):
                nick = "@" + nick
            user = Usuario.query.filter_by(nick=nick, telefone=telefone).first()

        if user:
            return jsonify({
                "nick": user.nick,
                "telefone": user.telefone,
                "summary": user.resumo_gerado,
                "access_code": user.codigo_acesso,
                "language": user.idioma,
                "timestamp": user.data_atualizacao.isoformat()
            }), 200
        else:
            # Return error key
            return jsonify({"error_key": "RESULT_NOT_FOUND"}), 404

    except Exception as e:
        print(f"Erro ao recuperar resultado: {e}")
        # Return error key
        return jsonify({"error_key": "INTERNAL_SERVER_ERROR"}), 500

