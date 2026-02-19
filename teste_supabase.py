import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Carrega as variáveis do seu arquivo .env
load_dotenv()

print(">>> Iniciando teste de conexão com o Supabase...")

# Pega as credenciais do seu arquivo .env
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_SECRET_KEY")

# Verifica se as credenciais foram carregadas
if not url or not key:
    print("\n!!! ERRO: Não consegui encontrar a URL ou a SECRET KEY no seu arquivo .env.")
    print("!!! Verifique se o arquivo .env está na mesma pasta e se as chaves estão lá.")
else:
    print(f">>> URL encontrada: {url}")
    print(f">>> Chave encontrada: A chave secreta termina com '...{key[-4:]}'") # Mostra só o final da chave por segurança

    try:
        # Tenta se conectar e listar as tabelas do seu banco de dados
        print("\n>>> Tentando criar o cliente Supabase...")
        supabase: Client = create_client(url, key)
        print(">>> Cliente Supabase criado com sucesso!")

        print("\n>>> Tentando buscar dados da tabela 'conversations'...")
        response = supabase.table('conversations').select('id').limit(1).execute()

        # Se a chamada deu certo, mesmo que não retorne nada, a conexão funcionou
        if response:
             print("\n✅ SUCESSO! A conexão com o Supabase foi estabelecida e os dados foram consultados.")
             print("✅ Isso prova que suas chaves no arquivo .env estão CORRETAS.")

    except Exception as e:
        # Se der erro aqui, significa que a chave no seu .env está errada
        print(f"\n❌ FALHA NA CONEXÃO: O Supabase retornou um erro.")
        print(f"❌ Detalhe do erro: {e}")
        print("\n❌ Isso significa que a SUPABASE_URL ou a SUPABASE_SECRET_KEY no seu arquivo .env está incorreta.")

