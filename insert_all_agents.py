#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para inserir todos os 19 agentes no Supabase
e gerar o mapeamento para o app.py
"""

import os
import json
from dotenv import load_dotenv
from supabase import create_client, Client

# Carregar variáveis de ambiente
load_dotenv()

# Inicializar Supabase
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_ANON_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

# Lista de todos os 19 agentes
AGENTS = [
    {"name": "allex", "role": "Mentor de Líderes", "description": "Estrategista de Potencial Integral"},
    {"name": "lucas", "role": "Mentor de Comunicação", "description": "Especialista em Relacionamentos"},
    {"name": "fernando", "role": "Mentor de Negócios", "description": "Especialista em Estratégia"},
    {"name": "ricardo", "role": "Mentor Técnico", "description": "Especialista em Tecnologia"},
    {"name": "julia", "role": "Mentora de Desenvolvimento", "description": "Especialista em Crescimento Pessoal"},
    {"name": "rafaela", "role": "Mentora de Criatividade", "description": "Especialista em Inovação"},
    {"name": "leo", "role": "Mentor de Liderança", "description": "Especialista em Gestão"},
    {"name": "marcos", "role": "Mentor de Vendas", "description": "Especialista em Negociação"},
    {"name": "camila", "role": "Mentora de Marketing", "description": "Especialista em Branding"},
    {"name": "isabela", "role": "Mentora de RH", "description": "Especialista em Pessoas"},
    {"name": "gabriela", "role": "Mentora de Finanças", "description": "Especialista em Gestão Financeira"},
    {"name": "tiago", "role": "Mentor de Operações", "description": "Especialista em Processos"},
    {"name": "sofia", "role": "Mentora de Bem-estar", "description": "Especialista em Qualidade de Vida"},
    {"name": "eduardo", "role": "Mentor de Educação", "description": "Especialista em Aprendizado"},
    {"name": "drgustavo", "role": "Mentor de Saúde", "description": "Especialista em Bem-estar"},
    {"name": "helena", "role": "Mentora de Cultura", "description": "Especialista em Valores"},
    {"name": "carolina", "role": "Mentora de Sustentabilidade", "description": "Especialista em Responsabilidade"},
    {"name": "daniel", "role": "Mentor de Inovação", "description": "Especialista em Transformação"},
    {"name": "beatriz", "role": "Mentora de Coaching", "description": "Especialista em Desenvolvimento"},
]

print("🚀 Iniciando inserção de agentes no Supabase...\n")

# Dicionário para armazenar o mapeamento
agent_mapping = {}

# Inserir cada agente
for agent in AGENTS:
    try:
        response = supabase.table('agents').insert({
            'name': agent['name'],
            'role': agent['role'],
            'description': agent['description'],
            'avatar_url': f'https://example.com/{agent["name"]}.png'
        } ).execute()
        
        agent_id = response.data[0]['id']
        agent_mapping[agent['name']] = agent_id
        
        print(f"✅ {agent['name'].upper():12} -> {agent_id}")
        
    except Exception as e:
        print(f"❌ Erro ao inserir {agent['name']}: {str(e)}")

print("\n" + "="*80)
print("📝 MAPEAMENTO PARA app.py:")
print("="*80 + "\n")

# Gerar código Python para o app.py
print("AGENT_MAPPING = {")
for name, uuid in sorted(agent_mapping.items()):
    print(f'    "{name}": "{uuid}",')
print("}")

print("\n" + "="*80)
print("💾 Salvando mapeamento em 'agent_mapping_complete.json'...")
print("="*80 + "\n")

# Salvar em arquivo JSON
with open('agent_mapping_complete.json', 'w', encoding='utf-8') as f:
    json.dump(agent_mapping, f, indent=2, ensure_ascii=False)

print("✅ Arquivo 'agent_mapping_complete.json' criado com sucesso!")
print(f"\n✅ Total de agentes inseridos: {len(agent_mapping)}")
