from flask import Flask, render_template, request, redirect, flash
from forms import formServidor, formMagistrado
from Sistema_RH_TJGO import Servidores , Magistrados, AnalisadorDados # Importa a classe corretamente
import plotly.express as px
import sqlite3
import pandas as pd
import os

app = Flask(__name__, template_folder="Templates")

app.config['SECRET_KEY'] = '1234'

@app.route('/')
def home():
    return render_template('Home.html')

# Nome do banco de dados
DB_PATH = "RH_TJGO.db"

# Função para criar a tabela se não existir
def criar_tabela():
    con = sqlite3.connect(DB_PATH)
    cursor = con.cursor()
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS servidores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf TEXT NOT NULL UNIQUE,
            cargo TEXT NOT NULL,
            status TEXT NOT NULL,
            telefone TEXT NOT NULL,
            naturalidade TEXT NOT NULL,
            data_nascimento TEXT NOT NULL,
            email TEXT NOT NULL,
            sexo TEXT NOT NULL,
            identidade_genero TEXT NOT NULL,
            raca_cor TEXT NOT NULL,
            deficiencia TEXT NOT NULL,
            aprovado_cotas TEXT NOT NULL,
            data_posse TEXT NOT NULL,
            orgao_lotacao TEXT NOT NULL,
            situacao_profissional TEXT NOT NULL,
            data_inicio_situacao TEXT NOT NULL,
            data_saida_situacao TEXT
        )
    ''')
    con.commit()
    con.close()

# Função para criar a tabela se não existir
def criar_tabela():
    con = sqlite3.connect(DB_PATH)
    cursor = con.cursor()
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS magistrados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf TEXT NOT NULL UNIQUE,
            cargo TEXT NOT NULL,
            status TEXT NOT NULL,
            telefone TEXT NOT NULL,
            naturalidade TEXT NOT NULL,
            data_nascimento TEXT NOT NULL,
            email TEXT NOT NULL,
            sexo TEXT NOT NULL,
            identidade_genero TEXT NOT NULL,
            raca_cor TEXT NOT NULL,
            deficiencia TEXT NOT NULL,
            aprovado_cotas TEXT NOT NULL,
            data_posse TEXT NOT NULL,
            orgao_lotacao TEXT NOT NULL,
            situacao_profissional TEXT NOT NULL,
            data_inicio_situacao TEXT NOT NULL,
            data_saida_situacao TEXT,
            promocao TEXT NOT NULL,
            data_promocao TEXT
        )
    ''')
    con.commit()
    con.close()

# Função para importar o CSV para o banco de dados
def importar_csv_para_sqlite(filepath):
    df = pd.read_csv(filepath, delimiter=",", encoding="utf-8")
    
    con = sqlite3.connect(DB_PATH)
    df.to_sql("servidores", con, if_exists="append", index=False)
    con.close()

# Função para importar o CSV para o banco de dados
def importar_csv_magistrados_para_sqlite(filepath):
    df = pd.read_csv(filepath, delimiter=",", encoding="utf-8")
    
    con = sqlite3.connect(DB_PATH)
    df.to_sql("magistrados", con, if_exists="append", index=False)
    con.close()

def traduzir_erro(mensagem):
    traducoes = {
        "table servidores has no column named id": "Erro ao importar: A tabela 'servidores' não possui uma coluna chamada 'id'.",
        "UNIQUE constraint failed": "Erro ao importar: O registro já existe no banco de dados.",
        "datatype mismatch": "Erro ao importar: O tipo de dado está incorreto para uma coluna."
    }
    
    for erro_ingles, erro_portugues in traducoes.items():
        if erro_ingles in mensagem:
            return erro_portugues

    return mensagem  # Se não houver tradução, retorna o erro original


# Defina o diretório de upload
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'csv'}

# Função para verificar a extensão do arquivo
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Rota para upload do CSV
@app.route('/importar_csv', methods=['GET', 'POST'])
def importar_csv():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash("Nenhum arquivo enviado!", "danger")
            return redirect(request.url)
        
        file = request.files['file']
        
        if file.filename == '':
            flash("Nenhum arquivo selecionado!", "danger")
            return redirect(request.url)
        
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)  # Salvar arquivo temporariamente
            
            try:
                importar_csv_para_sqlite(filepath)  # Importar para SQLite
                os.remove(filepath)  # Remover o arquivo após a importação
                flash("Dados importados com sucesso!", "success")
            except Exception as e:
                flash(f"Erro ao importar: {e}", "danger")
    
    return render_template('Importar_CSV.html')

# Rota para upload do CSV
@app.route('/importar_csv_magistrados', methods=['GET', 'POST'])
def importar_csv_magistrados():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash("Nenhum arquivo enviado!", "danger")
            return redirect(request.url)
        
        file = request.files['file']
        
        if file.filename == '':
            flash("Nenhum arquivo selecionado!", "danger")
            return redirect(request.url)
        
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)  # Salvar arquivo temporariamente
            
            try:
                importar_csv_magistrados_para_sqlite(filepath)  # Importar para SQLite
                os.remove(filepath)  # Remover o arquivo após a importação
                flash("Dados importados com sucesso!", "success")
            except Exception as e:
                flash(f"Erro ao importar: {traduzir_erro(str(e))}", "danger")

    
    return render_template('Importar_CSV_magistrados.html')


# Rota para dados do gráfico
@app.route('/dados')
def dados():
    # Caminho para o banco de dados SQLite
    db_path = 'RH_TJGO.db'
    tabela = 'servidores'

    # Inicializa a classe AnalisadorDados para a tabela servidores
    analisador = AnalisadorDados(db_path=db_path, tabela=tabela)
    # Acessa os dados carregados no atributo 'dados'
    df = analisador.dados

    # Verifica se o DataFrame contém os dados necessários
    if df.empty:
        return "Erro: O banco de dados não retornou dados para a tabela servidores."

    # Converte o DataFrame em HTML para exibição no dashboard
    tabela_html = df.to_html(classes='table table-bordered')

    # Criação dos gráficos

    # Agrupamento de dados para diferentes categorias
    df_agrupado_sexo = df[['cpf','sexo']].drop_duplicates().groupby(['sexo']).size().reset_index(name='contagem')
    df_agrupado_raca = df[['cpf','raca_cor']].drop_duplicates().groupby(['raca_cor']).size().reset_index(name='contagem')
    df_agrupado_deficiencia = df[['cpf','deficiencia']].drop_duplicates().groupby(['deficiencia']).size().reset_index(name='contagem')
    df_agrupado_cargo = df[['cpf','cargo']].drop_duplicates().groupby(['cargo']).size().reset_index(name='contagem')

    # Gráfico 1: Número de Servidores por Cargo
    fig = px.bar(df_agrupado_cargo, x='cargo', y='contagem', color='cargo')
    # Personalizando layout
    fig.update_layout(
        xaxis_title='Cargo',
        yaxis_title='Número de Servidores',
        width=1200,  # Largura do gráfico
        height=600,  # Altura do gráfico
    )
    fig.update_traces(marker=dict(line=dict(width=0.5, color='black')))
    fig.update_layout(barmode='group')


    # Gráfico 2: Número de Servidores por Sexo
    fig_2 = px.bar(df_agrupado_sexo, x='sexo', y='contagem', color='sexo')
    fig_2.update_layout(xaxis_title='Sexo', yaxis_title='Número de Servidores')
    fig_2.update_traces(marker=dict(line=dict(width=0.5, color='black')))
    fig_2.update_layout(barmode='group')

    # Gráfico 3: Distribuição de Servidores por Raça/Cor
    fig_3 = px.pie(df_agrupado_raca, values='contagem', names='raca_cor')
    fig_3.update_traces(textinfo='percent+label')
    fig_3.update_layout(title_text='Distribuição de Servidores por Raça/Cor')

    # Gráfico 4: Distribuição de Servidores por Deficiência
    fig_4 = px.scatter(df_agrupado_deficiencia, x='deficiencia', y='contagem')
    fig_4.update_layout(xaxis_title='Deficiência', yaxis_title='Número de Servidores')
    fig_4.update_traces(marker=dict(line=dict(width=0.5, color='black')))   

    #Gráfico 5: Quantidade de servidores por situação profissional
    # Agrupando por situação profissional
    df_agrupado_situacao = df[['cpf','situacao_profissional']].groupby(['situacao_profissional']).size().reset_index(name='contagem')

    # Criando o gráfico
    fig_5 = px.pie(df_agrupado_situacao, names='situacao_profissional', values='contagem')
    fig_5.update_layout(xaxis_title='Situação Profissional', yaxis_title='Número de Servidores')
    fig_5.update_traces(marker=dict(line=dict(width=0.5, color='black')))


    #Gráfico 6: Soma de dias por situação profissional
    # Convertendo as colunas de data
    df_new = df.copy()
    df_new['data_inicio_situacao'] = pd.to_datetime(df_new['data_inicio_situacao'], format='%d-%m-%y', errors='coerce')
    df_new['data_saida_situacao'] = pd.to_datetime(df_new['data_saida_situacao'], format='%d-%m-%y', errors='coerce')
    df_new['data_saida_situacao'] = df_new['data_saida_situacao'].fillna(pd.to_datetime('today'))  # Preenchendo com a data atual se estiver vazia

    # Calculando a diferença de dias
    df_new['dias'] = (df_new['data_saida_situacao'] - df_new['data_inicio_situacao']).dt.days

    # Agrupando por situação profissional
    df_agrupado_situacao = df_new.groupby(['situacao_profissional']).agg({'dias': 'mean'}).reset_index()

    # Criando o gráfico
    fig_6 = px.bar(df_agrupado_situacao, x='situacao_profissional', y='dias', color='situacao_profissional')
    fig_6.update_layout(xaxis_title='Situação Profissional', yaxis_title='Média de Dias')
    fig_6.update_traces(marker=dict(line=dict(width=0.5, color='black')))
    fig_6.update_layout(barmode='group')



    # Renderiza o template com os dados e gráficos
    return render_template('Dashboard.html', tabela_html=tabela_html, 
                           fig=fig.to_html(full_html=False), 
                           fig_2=fig_2.to_html(full_html=False), 
                           fig_3=fig_3.to_html(full_html=False),
                           fig_4=fig_4.to_html(full_html=False),
                           fig_5=fig_5.to_html(full_html=False),
                            fig_6=fig_6.to_html(full_html=False))

# Rota para dados do gráfico
@app.route('/dados_magistrado')
def dados_magistrado():
    # Caminho para o banco de dados SQLite
    db_path = 'RH_TJGO.db'
    tabela = 'magistrados'

    # Inicializa a classe AnalisadorDados para a tabela magistrados
    analisador = AnalisadorDados(db_path=db_path, tabela=tabela)
    # Acessa os dados carregados no atributo 'dados'
    df = analisador.dados

    # Verifica se o DataFrame contém os dados necessários
    if df.empty:
        return "Erro: O banco de dados não retornou dados para a tabela magistrados."

    # Converte o DataFrame em HTML para exibição no dashboard
    tabela_html = df.to_html(classes='table table-bordered')

    # Criação dos gráficos

    # Agrupamento de dados para diferentes categorias
    df_agrupado_sexo = df[['cpf','sexo']].drop_duplicates().groupby(['sexo']).size().reset_index(name='contagem')
    df_agrupado_raca = df[['cpf','raca_cor']].drop_duplicates().groupby(['raca_cor']).size().reset_index(name='contagem')
    df_agrupado_deficiencia = df[['cpf','deficiencia']].drop_duplicates().groupby(['deficiencia']).size().reset_index(name='contagem')
    df_agrupado_cargo = df[['cpf','cargo']].drop_duplicates().groupby(['cargo']).size().reset_index(name='contagem')

    # Gráfico 1: Número de Magistrados por Cargo
    fig = px.bar(df_agrupado_cargo, x='cargo', y='contagem', color='cargo')
    # Personalizando layout
    fig.update_layout(
        xaxis_title='Cargo',
        yaxis_title='Número de Magistrados',
        width=1200,  # Largura do gráfico
        height=600,  # Altura do gráfico
    )
    fig.update_traces(marker=dict(line=dict(width=0.5, color='black')))
    fig.update_layout(barmode='group')


    # Gráfico 2: Número de Magistrados por Sexo
    fig_2 = px.bar(df_agrupado_sexo, x='sexo', y='contagem', color='sexo')
    fig_2.update_layout(xaxis_title='Sexo', yaxis_title='Número de Magistrados')
    fig_2.update_traces(marker=dict(line=dict(width=0.5, color='black')))
    fig_2.update_layout(barmode='group')

    # Gráfico 3: Distribuição de Tipos de Promoção por Data de Promoção
    # Convertendo a coluna de data para datetime
    df['data_promocao'] = pd.to_datetime(df['data_promocao'], format='%d-%m-%y', errors='coerce')
    # Agrupando por data de promoção
    df_agrupado_promocao = df[['cpf','data_promocao']].drop_duplicates().groupby(['data_promocao']).size().reset_index(name='contagem')
    # Criando o gráfico
    fig_3 = px.line(df_agrupado_promocao, x='data_promocao', y='contagem')
    fig_3.update_traces(marker=dict(line=dict(width=0.5, color='black')))
    fig_3.update_layout(xaxis_title='Data de Promoção', yaxis_title='Número de Promoções')


    # Gráfico 4: Distribuição de Magistrados por tipo de promoção
    # Agrupando por tipo de promoção
    df_agrupado_promocao = df[['cpf','promocao']].drop_duplicates().groupby(['promocao']).size().reset_index(name='contagem')
    # Criando o gráfico
    fig_4 = px.pie(df_agrupado_promocao, values='contagem', names='promocao')
    fig_4.update_traces(textinfo='percent+label')

    # Gráfico 5: Quantidade de magistrados por situação profissional
    # Agrupando por situação profissional
    df_agrupado_situacao = df[['cpf','situacao_profissional']].groupby(['situacao_profissional']).size().reset_index(name='contagem')
    # Criando o gráfico
    fig_5 = px.bar(df_agrupado_situacao, x='situacao_profissional', y='contagem', color='situacao_profissional')
    fig_5.update_layout(xaxis_title='Situação Profissional', yaxis_title='Número de Magistrados')
    fig_5.update_traces(marker=dict(line=dict(width=0.5, color='black')))


    # Gráfico 6: Soma de dias por situação profissional
    # Convertendo as colunas de data
    df_new = df.copy()
    df_new['data_inicio_situacao'] = pd.to_datetime(df_new['data_inicio_situacao'], format='%d-%m-%y', errors='coerce')
    df_new['data_saida_situacao'] = pd.to_datetime(df_new['data_saida_situacao'], format='%d-%m-%y', errors='coerce')
    df_new['data_saida_situacao'] = df_new['data_saida_situacao'].fillna(pd.to_datetime('today'))  # Preenchendo com a data atual se estiver vazia

    # Calculando a diferença de dias
    df_new['dias'] = (df_new['data_saida_situacao'] - df_new['data_inicio_situacao']).dt.days

    # Agrupando por situação profissional
    df_agrupado_situacao = df_new.groupby(['situacao_profissional']).agg({'dias': 'sum'}).reset_index()

    # Criando o gráfico
    fig_6 = px.bar(df_agrupado_situacao, x='situacao_profissional', y='dias', color='situacao_profissional')
    fig_6.update_layout(xaxis_title='Situação Profissional', yaxis_title='Soma de Dias')
    fig_6.update_traces(marker=dict(line=dict(width=0.5, color='black')))
    fig_6.update_layout(barmode='group')



    # Renderiza o template com os dados e gráficos
    return render_template('Dashboard_Magistrado.html', tabela_html=tabela_html, 
                           fig=fig.to_html(full_html=False), 
                           fig_2=fig_2.to_html(full_html=False), 
                           fig_3=fig_3.to_html(full_html=False),
                           fig_4=fig_4.to_html(full_html=False),
                           fig_5=fig_5.to_html(full_html=False),
                           fig_6=fig_6.to_html(full_html=False))


# Rota para exibir e processar o formulário de cadastro de servidores
@app.route('/servidor', methods=['GET', 'POST'])
def servidor():
    # Criação do formulário de servidor
    form = formServidor()

    # Verifica se o formulário foi submetido com dados válidos
    if form.validate_on_submit():
        try:
            # Cria uma instância do objeto Servidores com os dados do formulário
            servidor = Servidores(
                nome=form.nome.data,
                cpf=form.cpf.data,
                cargo=form.cargo.data,
                status=form.status.data,
                telefone=form.telefone.data,
                naturalidade=form.naturalidade.data,
                data_nascimento=form.data_nascimento.data,
                email=form.email.data,
                sexo=form.sexo.data,
                identidade_genero=form.identidade_genero.data,
                raca_cor=form.raca_cor.data,
                # Verifica se a lista de deficiências é uma lista antes de concatenar as opções
                deficiencia=", ".join(form.deficiencia.data) if isinstance(form.deficiencia.data, list) else str(form.deficiencia.data),
                aprovado_cotas=form.aprovado_cotas.data,
                data_posse=form.data_posse.data,
                orgao_lotacao=form.orgao_lotacao.data,
                situacao_profissional=form.situacao_profissional.data,
                data_inicio_situacao=form.data_inicio_situacao.data,
                data_saida_situacao=form.data_saida_situacao.data
            )

            # Salva os dados do servidor no banco de dados
            servidor.salvar_servidor()

            # Exibe uma mensagem de sucesso
            print("Dados salvos com sucesso!")
            # Redireciona para a página de confirmação de envio
            return formulario_enviado()
        except Exception as e:
            # Em caso de erro, exibe a mensagem de erro
            print(f"Erro ao salvar no banco: {e}")

    # Se não for uma submissão do formulário, renderiza a página do formulário de servidor
    return render_template('Base_Servidor.html', form=form)

# Rota para exibir e processar o formulário de cadastro de magistrados
@app.route('/magistrado', methods=['GET', 'POST'])
def magistrado():
    # Criação do formulário de magistrado
    form = formMagistrado()

    # Verifica se o formulário foi submetido com dados válidos
    if form.validate_on_submit():
        try:
            # Cria uma instância do objeto Magistrados com os dados do formulário
            magistrado = Magistrados(
                nome=form.nome.data,
                cpf=form.cpf.data,
                cargo=form.cargo.data,
                status=form.status.data,
                telefone=form.telefone.data,
                naturalidade=form.naturalidade.data,
                data_nascimento=form.data_nascimento.data,
                email=form.email.data,
                sexo=form.sexo.data,
                identidade_genero=form.identidade_genero.data,
                raca_cor=form.raca_cor.data,
                # Verifica se a lista de deficiências é uma lista antes de concatenar as opções
                deficiencia=", ".join(form.deficiencia.data) if isinstance(form.deficiencia.data, list) else str(form.deficiencia.data),
                aprovado_cotas=form.aprovado_cotas.data,
                data_posse=form.data_posse.data,
                orgao_lotacao=form.orgao_lotacao.data,
                situacao_profissional=form.situacao_profissional.data,
                data_inicio_situacao=form.data_inicio_situacao.data,
                data_saida_situacao=form.data_saida_situacao.data,
                promocao=form.promocao.data,
                data_promocao=form.data_promocao.data
            )

            # Salva os dados do magistrado no banco de dados
            magistrado.salvar_magistrado()

            # Exibe uma mensagem de sucesso
            print("Dados salvos com sucesso!")
            # Redireciona para a página de confirmação de envio
            return formulario_enviado()
        except Exception as e:
            # Em caso de erro, exibe a mensagem de erro
            print(f"Erro ao salvar no banco: {e}")

    # Se não for uma submissão do formulário, renderiza a página do formulário de magistrado
    return render_template('Base_Magistrado.html', form=form)

# Rota para exibir a página de confirmação após o envio do formulário
@app.route('/formulario_enviado')
def formulario_enviado():
    # Renderiza a página de confirmação de envio do formulário
    return render_template('Formulario_enviado.html')

# Inicia o servidor Flask
if __name__ == '__main__':
    app.run(debug=True)
    