import json
import os
import uuid

CAMINHO_TAREFAS = os.path.join(os.path.dirname(__file__), 'tarefas.json')

def carregar_tarefas():
    '''''Carrega as tarefas do arquivo tarefas.json.'''
    if not os.path.exists(CAMINHO_TAREFAS):
        # Se o arquivo não existir cria um vazio
        with open(CAMINHO_TAREFAS, 'w', encoding='utf-8') as arquivo:
            json.dump([], arquivo, indent=4, ensure_ascii=False)
    with open(CAMINHO_TAREFAS, 'r', encoding='utf-8') as arquivo:
        try:
            return json.load(arquivo)
        except json.JSONDecodeError: # Tratar caso o JSON esteja malformado
            return[]
    
def salvar_tarefas(tarefas):
    '''Salva a lista de tarefas no arquivo tarefas.json.'''
    with open(CAMINHO_TAREFAS, 'w', encoding='utf-8') as arquivo:
        json.dump(tarefas, arquivo, indent=4, ensure_ascii=False)
        
def adicionar_tarefa(descricao, data_inicio, data_termino, status="A iniciar"):
    '''Adiciona uma nova tarefa a lista.'''
    tarefas = carregar_tarefas()
    nova_tarefa = {
        "id": str(uuid.uuid4()), # Adicionar ID único
        "descricao": descricao,
        "data_inicio": data_inicio,
        "data_termino": data_termino,
        "status": status,
        "subtarefas": [] # Inicializar lista de subtarefas
    }   
    tarefas.append(nova_tarefa)
    salvar_tarefas(tarefas)
    return nova_tarefa['id'] # Retornar o ID da nova tarefa

def remover_tarefa(id_tarefa):
    '''Remove uma tarefa da lista pelo índice.'''
    tarefas = carregar_tarefas()
    tarefas_filtradas = [t for t in tarefas if t['id'] != id_tarefa]
    
    if len(tarefas_filtradas) < len(tarefas):
        salvar_tarefas(tarefas_filtradas)
        return True
    
    return False
    
def atualizar_status_tarefa(id_tarefa, novo_status):
    '''Atualiza o status de uma tarefa pelo índice.'''
    tarefas = carregar_tarefas()
    tarefa_encontrada = False
    
    for tarefa in tarefas:
        if tarefa['id'] == id_tarefa:
            tarefa['status'] = novo_status
            tarefa_encontrada = True
            break
    
    if tarefa_encontrada:
        salvar_tarefas(tarefas)
        return True
    
    return False

def encontrar_tarefa_por_id(id_tarefa):
    tarefas = carregar_tarefas()
    
    for tarefa in tarefas:
        if tarefa['id'] == id_tarefa:
            return tarefa
        
    return None

# Funções para subtarefas
def adicionar_subtarefa(id_tarefa_principal, descricao_subtarefa):
    tarefas = carregar_tarefas()
    modificado = False
    
    for tarefa in tarefas:
        if tarefa['id'] == id_tarefa_principal:
            nova_subtarefa = {
                "id_sub": str(uuid.uuid4()),
                "descricao_sub": descricao_subtarefa,
                "concluida": False
            }
            tarefa.setdefault('subtarefas', []).append(nova_subtarefa) # Garante que a lista exista
            modificado = True
            break
        
    if modificado:
        salvar_tarefas(tarefas)
        return nova_subtarefa['id_sub']
    
    return None

def remover_subtarefa(id_tarefa_principal, id_subtarefa):
    tarefas = carregar_tarefas()
    modificado = False
    for tarefa in tarefas:
        if tarefa['id'] == id_tarefa_principal:
            subtarefas_originais_len = len(tarefa.get('subtarefas', []))
            tarefa['subtarefas'] = [st for st in tarefa.get('subtarefas', []) if st['id_sub'] != id_subtarefa]
            if len(tarefa['subtarefas']) < subtarefas_originais_len:
                modificado = True
                break
    
    if modificado:
        salvar_tarefas(tarefas)
        return True
    
    return False

def atualizar_status_subtarefa(id_tarefa_principal, id_subtarefa, concluida: bool):
    tarefas = carregar_tarefas()
    modificado = False
    for tarefa in tarefas:
        if tarefa['id'] == id_tarefa_principal:
            for subtarefa in tarefa.get('subtarefas', []):
                if subtarefa['id_sub'] == id_subtarefa:
                    subtarefa['concluida'] = concluida
                    modificado = True
                    break
            if modificado:
                break
    
    if modificado:
        salvar_tarefas(tarefas)
        return True
    
    return False

            


