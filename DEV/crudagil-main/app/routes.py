# Arquivo `routes.py`

from flask_login import login_required, current_user, login_user, logout_user
from flask import render_template, redirect, url_for, request, flash
from app import app, db
from app.models import Usuario
from app.models import Projeto
from app.models import Sprint
from app.models import Agendamento
from datetime import datetime



@app.route('/')
def index():
    if current_user.is_authenticated:
        # Se o usuário estiver autenticado, redireciona para a lista de projetos
        return render_template('index.html')
    else:
        # Caso contrário, redireciona para a página de login
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        senha = request.form['senha']
        
        # Lógica para verificar o login e senha (pode ser feita com SQLAlchemy)
        usuario = Usuario.query.filter_by(login=login, senha=senha).first()
        
        if usuario:
            # Usuário autenticado, realiza o login e redireciona
            login_user(usuario)

            # Agora, você pode redirecionar para a rota desejada após o login
            return render_template('index.html')
            # return redirect(url_for('home'))
        else:
            # Caso contrário, exibe uma mensagem de erro
            return render_template('login.html', error='Login ou senha incorretos')

    return render_template('login.html', error=None)

@app.route('/logout')
@login_required
def logout():
    # Encerra a sessão
    logout_user()
    return redirect(url_for('login'))

@app.route('/cadastro_usuario', methods=['GET', 'POST'])
def cadastro_usuario():
    if request.method == 'POST':
        # Lógica para cadastrar o usuário no banco (pode ser feita com SQLAlchemy)
        novo_usuario = Usuario(
            login=request.form['login'],
            senha=request.form['senha'],
            nome=request.form['nome'],
            funcao=request.form['funcao']
        )
        db.session.add(novo_usuario)
        db.session.commit()
        
        # Redireciona para a página de login
        return redirect(url_for('login'))

    return render_template('cadastro_usuario.html')

@app.route('/lista_projetos')
@login_required
def lista_projetos():
    projetos = Projeto.query.all()
    return render_template('lista_projetos.html', projetos=projetos)

@app.route('/novo_projeto', methods=['GET', 'POST'])
@login_required
def novo_projeto():
    if request.method == 'POST':
        # Extrai os dados do formulário
        nome_projeto = request.form['nome_projeto']
        descricao = request.form['descricao']
        data_inicio = request.form['data_inicio']
        data_termino = request.form['data_termino']
        prioridade = request.form['prioridade']
        # Cria uma nova instância de Projeto
        novo_projeto = Projeto(
            nome_projeto=nome_projeto,
            descricao=descricao,
            data_inicio=data_inicio,
            data_termino=data_termino,
            prioridade=prioridade
        )

        # Adiciona o novo projeto ao banco de dados
        db.session.add(novo_projeto)
        db.session.commit()
        flash('Novo projeto cadastrado com sucesso!')
        return redirect(url_for('lista_projetos'))
    return render_template('novo_projeto.html')

@app.route('/editar_projeto/<int:projeto_id>', methods=['GET', 'POST'])
@login_required
def editar_projeto(projeto_id):
    projeto = Projeto.query.get(projeto_id)
    if request.method == 'POST':
        projeto = Projeto.query.get(projeto_id)
        projeto.nome_projeto = request.form['nome_projeto']
        projeto.descricao = request.form['descricao']
        projeto.data_inicio = request.form['data_inicio']
        projeto.data_termino = request.form['data_termino']
        projeto.prioridade = request.form['prioridade']
        db.session.commit()
        flash('Projeto editado com sucesso!')
        return redirect(url_for('lista_projetos'))
    return render_template('editar_projeto.html', projeto=projeto)

@app.route('/excluir_projeto/<int:projeto_id>')
@login_required
def excluir_projeto(projeto_id):
    projeto = Projeto.query.get(projeto_id)

    if projeto:
        # Exclui o projeto do banco de dados
        db.session.delete(projeto)
        db.session.commit()

        flash('Projeto excluído com sucesso!')
    else:
        flash('Projeto não encontrado.')

    return redirect(url_for('lista_projetos'))

@app.route('/visualizar_sprints/<int:projeto_id>')
@login_required
def visualizar_sprints(projeto_id):
    projeto = Projeto.query.get(projeto_id)
    sprints = Sprint.query.filter_by(projeto_id=projeto_id).all()
    responsavel = {usuario.usuario_id: usuario.nome for usuario in Usuario.query.all()}

    return render_template('visualizar_sprints.html', projeto=projeto, sprints=sprints, responsavel=responsavel)

@app.route('/nova_sprint/<int:projeto_id>', methods=['GET', 'POST'])
@login_required
def nova_sprint(projeto_id):
    usuarios = Usuario.query.all()  # Obter todos os usuários cadastrados

    if request.method == 'POST':
        # Extrai os dados do formulário
        nome_sprint = request.form['nome_sprint']
        descricao = request.form['descricao']
        data_inicio = request.form['data_inicio']
        data_termino = request.form['data_termino']
        status = request.form['status']
        responsavel_id = int(request.form['responsavel'])

        # Verifica se o responsável está entre os usuários cadastrados
        if Usuario.query.get(responsavel_id):
            # Cria uma nova instância de Sprint
            nova_sprint = Sprint(
                projeto_id=projeto_id,
                nome_sprint=nome_sprint,
                descricao=descricao,
                data_inicio=data_inicio,
                data_termino=data_termino,
                status=status,
                responsavel=responsavel_id
            )

            # Adiciona a nova sprint ao banco de dados
            db.session.add(nova_sprint)
            db.session.commit()

            flash('Nova sprint cadastrada com sucesso!')
            return redirect(url_for('visualizar_sprints', projeto_id=projeto_id))
        else:
            flash('Usuário selecionado como responsável não encontrado.')

    return render_template('nova_sprint.html', projeto_id=projeto_id, usuarios=usuarios)

@app.route('/editar_sprint/<int:sprint_id>', methods=['GET', 'POST'])
@login_required
def editar_sprint(sprint_id):
    sprint = Sprint.query.get(sprint_id)
    usuarios = Usuario.query.all()  # Obter todos os usuários cadastrados

    if request.method == 'POST':
        # Extrai os dados do formulário
        sprint.nome_sprint = request.form['nome_sprint']
        sprint.descricao = request.form['descricao']
        sprint.data_inicio = request.form['data_inicio']
        sprint.data_termino = request.form['data_termino']
        sprint.status = request.form['status']
        responsavel_id = int(request.form['responsavel'])

        # Verifica se o responsável está entre os usuários cadastrados
        if Usuario.query.get(responsavel_id):
            sprint.responsavel = responsavel_id
            # Atualiza a sprint no banco de dados
            db.session.commit()
            flash('Sprint editada com sucesso!')
            return redirect(url_for('visualizar_sprints', projeto_id=sprint.projeto_id))
        else:
            flash('Usuário selecionado como responsável não encontrado.')

    return render_template('editar_sprint.html', sprint=sprint, usuarios=usuarios)

@app.route('/excluir_sprint/<int:sprint_id>')
@login_required
def excluir_sprint(sprint_id):
    sprint = Sprint.query.get(sprint_id)
    
    if sprint:
        # Exclui a sprint do banco de dados
        db.session.delete(sprint)
        db.session.commit()

        flash('Sprint excluída com sucesso!')
    else:
        flash('Sprint não encontrada.')

    return redirect(url_for('visualizar_sprints', projeto_id=sprint.projeto_id))

@app.route('/agendar_passeio', methods=['GET', 'POST'])
@login_required

def agendar_passeio():
    if request.method == 'POST':
        # Obter os dados do formulário
        nome_pet = request.form['nome_pet']
        tipo_servico = request.form['tipo_servico']
        data_hora = request.form['data_hora']
        observacoes = request.form['observacoes']

        # Converter data_hora para formato datetime
        data_hora = datetime.strptime(data_hora, '%Y-%m-%dT%H:%M')

        # Criação do agendamento
        novo_agendamento = Agendamento(
            usuario_id=current_user.usuario_id,
            nome_pet=nome_pet,
            tipo_servico=tipo_servico,
            data_hora=data_hora,
            observacoes=observacoes
        )

        # Adicionar ao banco de dados
        db.session.add(novo_agendamento)
        db.session.commit()
        
        flash('Agendamento realizado com sucesso!')
        return redirect(url_for('listar_agendamentos'))
    
    return render_template('agendar_passeio.html')

@app.route('/listar_agendamentos')
@login_required
def listar_agendamentos():
    # Buscar os agendamentos do usuário logado
    agendamentos = Agendamento.query.filter_by(usuario_id=current_user.usuario_id).all()
    return render_template('listar_agendamentos.html', agendamentos=agendamentos)

@app.route('/editar_agendamento/<int:agendamento_id>', methods=['GET', 'POST'])
@login_required
def editar_agendamento(agendamento_id):
    agendamento = Agendamento.query.get(agendamento_id)
    if request.method == 'POST':
        # Atualizar dados do agendamento
        agendamento.nome_pet = request.form['nome_pet']
        agendamento.tipo_servico = request.form['tipo_servico']
        agendamento.data_hora = request.form['data_hora']
        agendamento.observacoes = request.form['observacoes']

        # Commit para salvar alterações
        db.session.commit()
        flash('Agendamento atualizado com sucesso!')
        return redirect(url_for('listar_agendamentos'))

    return render_template('editar_agendamento.html', agendamento=agendamento)

@app.route('/excluir_agendamento/<int:agendamento_id>')
@login_required
def excluir_agendamento(agendamento_id):
    agendamento = Agendamento.query.get(agendamento_id)
    if agendamento:
        db.session.delete(agendamento)
        db.session.commit()
        flash('Agendamento excluído com sucesso!')
    else:
        flash('Agendamento não encontrado.')

    return redirect(url_for('listar_agendamentos'))
