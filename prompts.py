# -*- coding: utf-8 -*-
import ast

def load_prompts_from_file(filepath="PROMPTS AGENTES.txt"):
    """
    Lê um arquivo de texto que contém um dicionário Python e o carrega de forma segura.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # A variável no arquivo de texto se chama AGENT_PROMPTS
        # Precisamos remover o nome da variável para avaliar apenas o dicionário
        if 'AGENT_PROMPTS = ' in content:
            content = content.split('AGENT_PROMPTS = ', 1)[1]

        # ast.literal_eval avalia a string como um literal Python (dicionário, lista, etc.)
        # É muito mais seguro do que usar eval()
        prompts = ast.literal_eval(content)
        return prompts

    except FileNotFoundError:
        print(f"!!! ERRO CRÍTICO: O arquivo de prompts '{filepath}' não foi encontrado.")
        return {}
    except Exception as e:
        print(f"!!! ERRO CRÍTICO: Falha ao ler e processar o arquivo de prompts: {e}")
        return {}

# Carrega os prompts quando este módulo é importado
AGENT_PROMPTS = load_prompts_from_file()

