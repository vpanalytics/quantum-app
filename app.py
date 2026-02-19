# -*- coding: utf-8 -*-
import os
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv
from supabase import create_client, Client

# Tenta importar os prompts, mas lida com o erro se o arquivo não existir
try:
    from prompts import AGENT_PROMPTS
except ImportError:
    print("!!! AVISO: Arquivo 'prompts.py' não encontrado. Usando dicionário vazio.")
    AGENT_PROMPTS = {}

# ===== CARREGA VARIÁVEIS DE AMBIENTE =====
load_dotenv()

# ===== INICIALIZAR SUPABASE =====
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_SECRET_KEY")

if not supabase_url or not supabase_key:
    raise ValueError("As variáveis de ambiente SUPABASE_URL e SUPABASE_SECRET_KEY não foram definidas.")

supabase: Client = create_client(supabase_url, supabase_key)

# --- Configuração do Cliente OpenAI ---
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("A variável de ambiente OPENAI_API_KEY não foi definida.")

client = OpenAI(api_key=openai_api_key)

# --- Configuração do Servidor Flask ---
app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": ["*"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# ===================================================================
# == ROTA PRINCIPAL DA IA: /ask                                  ==
# ===================================================================
@app.route('/ask', methods=['POST'])
def ask_agent():
    data = request.get_json()
    agent_id = data.get('agent_id')
    history = data.get('history', [])

    if not agent_id or agent_id not in AGENT_PROMPTS:
        return jsonify({"error": "Agent ID é inválido ou não foi fornecido."}), 400

    messages = [{"role": "system", "content": AGENT_PROMPTS.get(agent_id, "")}]
    messages.extend(history)

    force_format_instruction = "\n\nLembre-se: Responda em no máximo 3 frases curtas, com cada frase em um novo parágrafo."
    messages.append({"role": "user", "content": force_format_instruction})

    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=150,
            temperature=0.7
        )
        ai_response = completion.choices[0].message.content
        return jsonify({"response": ai_response})

    except Exception as e:
        print(f"!!! Erro ao chamar a API da OpenAI: {e}")
        return jsonify({"error": f"Desculpe, não consegui processar sua solicitação. Detalhe: {str(e)}"}), 500

# ===================================================================
# == ROTAS PARA GERENCIAR O HISTÓRICO NO SUPABASE                ==
# ===================================================================

@app.route('/conversation', methods=['POST'])
def get_or_create_conversation():
    data = request.get_json()
    user_id = data.get('user_id')
    agent_id = data.get('agent_id')

    if not user_id or not agent_id:
        return jsonify({"error": "user_id e agent_id são obrigatórios"}), 400

    try:
        response = supabase.table('conversations').select('id').eq('user_id', user_id).eq('agent_id', agent_id).execute()
        
        conversation_id = None
        if response.data:
            conversation_id = response.data[0]['id']
        else:
            insert_response = supabase.table('conversations').insert({'user_id': user_id, 'agent_id': agent_id}).execute()
            if insert_response.data:
                conversation_id = insert_response.data[0]['id']
            else:
                return jsonify({"error": "Falha ao criar a conversa no Supabase"}), 500

        messages_response = supabase.table('messages').select('content, role, created_at').eq('conversation_id', conversation_id).order('created_at', desc=False).execute()

        return jsonify({
            "success": True,
            "conversation_id": conversation_id,
            "messages": messages_response.data
        })

    except Exception as e:
        print(f"!!! Erro em /conversation: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/message', methods=['POST'])
def add_message():
    data = request.get_json()
    conversation_id = data.get('conversation_id')
    content = data.get('content')
    role = data.get('role')

    if not all([conversation_id, content, role]):
        return jsonify({"error": "conversation_id, content, e role são obrigatórios"}), 400

    try:
        response = supabase.table('messages').insert({'conversation_id': conversation_id, 'content': content, 'role': role}).execute()
        if response.data:
            return jsonify({"success": True, "message": "Mensagem salva com sucesso"})
        else:
            return jsonify({"success": False, "error": "Falha ao salvar a mensagem"}), 500

    except Exception as e:
        print(f"!!! Erro em /message: {e}")
        return jsonify({"error": str(e)}), 500

# NOVA ROTA PARA LIMPAR O HISTÓRICO
@app.route('/conversation/<conversation_id>', methods=['DELETE'])
def delete_conversation_history(conversation_id):
    if not conversation_id:
        return jsonify({"error": "ID da conversa é obrigatório"}), 400

    try:
        response = supabase.table('messages').delete().eq('conversation_id', conversation_id).execute()
        print(f">>> Histórico da conversa {conversation_id} limpo. Mensagens removidas: {len(response.data)}")
        return jsonify({"success": True, "message": "Histórico limpo com sucesso."}), 200

    except Exception as e:
        print(f"!!! Erro ao deletar histórico da conversa {conversation_id}: {e}")
        return jsonify({"error": str(e)}), 500

# ===================================================================
# == ROTAS DE SERVIÇO E INICIALIZAÇÃO                            ==
# ===================================================================
@app.route('/')
def home():
    return send_file('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')

