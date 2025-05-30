from flask import Blueprint, render_template, request, redirect, url_for, flash
from . import models

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/tarefas')
def tarefas():
    lista_tarefas = models.carregar_tarefas()
    return render_template('tarefas.html', tarefas=lista_tarefas)

@bp.route('/adicionar_tarefa', methods=['POST'])
def adicionar_tarefa_rota():
    descricao = request.form['descricao']
    data_inicio = request.form['data_inicio']
    data_termino = request.form['data_termino']
    
    if not all([descricao, data_inicio, data_termino]):
        flash('Todos os campos são obrigatórios para adicionar uma tarefa!', 'error')
        return redirect(url_for('main.tarefas'))
        
    models.adicionar_tarefa(descricao, data_inicio, data_termino)
    flash('Tarefa adicionada com sucesso!', 'success')
    return redirect(url_for('main.tarefas'))

@bp.route('/remover_tarefa/<id_tarefa>')
def remover_tarefa_rota(id_tarefa):
    if models.remover_tarefa(id_tarefa):
        flash('Tarefa removida com sucesso!', 'success')
    else:
        flash('Erro ao remover tarefa. ID não encontrado.', 'error')
    return redirect(url_for('main.tarefas'))

@bp.route('/atualizar_status_tarefa/<id_tarefa>', methods=['POST'])
def atualizar_status_tarefa_rota(id_tarefa):
    novo_status = request.form.get('status')
    if models.atualizar_status_tarefa(id_tarefa, novo_status):
        flash('Status da tarefa atualizado!', 'success')
    else:
        flash('Erro ao atualizar status da tarefa.', 'error')
    
    return redirect(url_for('main.tarefas'))

# Rotas para subtarefas
@bp.route('/tarefa/<id_tarefa_principal>/adicionar_subtarefa', methods=['POST'])
def adicionar_subtarefa_rota(id_tarefa_principal):
    descricao_subtarefa = request.form.get('descricao_subtarefa')
    if not descricao_subtarefa:
        flash('A descrição da subtarefa é obrigatória!', 'error')
    elif models.adicionar_subtarefa(id_tarefa_principal, descricao_subtarefa):
        flash('Subtarefa adicionada com sucesso!', 'success')
    else:
        flash('Erro ao adicionar subtarefa. Tarefa principal não encontrada.', 'error')
    return redirect(url_for('main.tarefas'))

@bp.route('/tarefa/<id_tarefa_principal>/remover_subtarefa/<id_subtarefa>')
def remover_subtarefa_rota(id_tarefa_principal, id_subtarefa):
    if models.remover_subtarefa(id_tarefa_principal, id_subtarefa):
        flash('Subtarefa removida com sucesso!', 'success')
    else:
        flash('Erro ao remover subtarefa.', 'error')
    return redirect(url_for('main.tarefas'))

@bp.route('/tarefa/<id_tarefa_principal>/atualizar_subtarefa/<id_subtarefa>', methods=['POST'])
def atualizar_subtarefa_rota(id_tarefa_principal, id_subtarefa):
    concluida_status = 'concluida' in request.form
    if models.atualizar_status_subtarefa(id_tarefa_principal, id_subtarefa, concluida_status):
        flash('Status da subtarefa atualizado!', 'success')
    else:
        flash('Erro ao atualizar status da subtarefa.', 'error')
    return redirect(url_for('main.tarefas'))

    

