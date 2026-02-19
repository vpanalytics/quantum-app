# Quantum Minds - Plataforma de Agentes IA

Uma plataforma web completa que integra múltiplos agentes de IA usando OpenAI GPT e Supabase para gerenciamento de conversas.

## 🎯 Características

- **18 Agentes IA** dispostos em uma formação visual interativa
- **Histórico de Conversas** persistido no Supabase
- **Interface Futurista** com design responsivo
- **Integração OpenAI** para respostas inteligentes
- **Backend Flask** com CORS habilitado

## 🚀 Instalação Local

### Pré-requisitos
- Python 3.11+
- pip ou pipenv

### Passos

1. **Clone o repositório:**
```bash
git clone https://github.com/vpanalytics/quantum-app.git
cd quantum-app
```

2. **Crie um ambiente virtual:**
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente:**
```bash
cp .env.example .env
# Edite .env com suas credenciais reais
```

5. **Execute a aplicação:**
```bash
python app.py
```

A aplicação estará disponível em `http://localhost:5001`

## 📦 Dependências

- **Flask 3.0.3** - Framework web
- **Flask-Cors 4.0.1** - Suporte CORS
- **Gunicorn 22.0.0** - Servidor WSGI para produção
- **OpenAI 1.30.1** - Cliente da API OpenAI
- **Supabase 2.5.0** - Cliente do Supabase
- **python-dotenv 1.0.1** - Carregamento de variáveis de ambiente

## 🔧 Variáveis de Ambiente

```
OPENAI_API_KEY=your_openai_api_key_here
SUPABASE_URL=your_supabase_url_here
SUPABASE_ANON_KEY=your_supabase_anon_key_here
SUPABASE_SECRET_KEY=your_supabase_secret_key_here
```

## 📡 Endpoints da API

### POST `/ask`
Envia uma pergunta para um agente IA e recebe uma resposta.

**Request:**
```json
{
  "agent_id": "allex",
  "history": [
    {"role": "user", "content": "Olá"},
    {"role": "assistant", "content": "Oi! Como posso ajudar?"}
  ]
}
```

**Response:**
```json
{
  "response": "Resposta do agente..."
}
```

### POST `/conversation`
Obtém ou cria uma conversa para um usuário e agente.

**Request:**
```json
{
  "user_id": "user123",
  "agent_id": "allex"
}
```

### POST `/message`
Adiciona uma mensagem ao histórico de conversa.

**Request:**
```json
{
  "conversation_id": "conv123",
  "content": "Sua mensagem",
  "role": "user"
}
```

### DELETE `/conversation/<conversation_id>`
Limpa o histórico de uma conversa.

## 🐳 Deploy com Docker

```bash
docker build -t quantum-app .
docker run -p 5000:5000 --env-file .env quantum-app
```

## 🚢 Deploy no Render

1. Conecte seu repositório GitHub ao Render
2. Configure as variáveis de ambiente no painel do Render
3. O Render detectará automaticamente o Dockerfile e fará o deploy

## 📝 Estrutura do Projeto

```
quantum-app/
├── app.py                      # Backend Flask
├── index.html                  # Frontend
├── prompts.py                  # Carregador de prompts
├── requirements.txt            # Dependências Python
├── Dockerfile                  # Configuração Docker
├── Procfile                    # Configuração Heroku/Render
├── .env.example               # Exemplo de variáveis de ambiente
└── README.md                  # Este arquivo
```

## 🤝 Contribuindo

Faça um fork do projeto, crie uma branch para sua feature e envie um pull request.

## 📄 Licença

Este projeto está sob licença MIT.

## 👨‍💻 Autor

Desenvolvido com ❤️ para o Quantum Academy

---

**Nota:** Nunca commite o arquivo `.env` com credenciais reais. Use `.env.example` como template.
