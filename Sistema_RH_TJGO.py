import csv # Para manipulação de arquivos CSV
import sqlite3 # Para manipulação de banco de dados SQLite
import pandas as pd  # Para manipulação de dados
import os  # Para verificar se o arquivo já existe

# Classe Servidores: Representa um servidor e suas propriedades.
class Servidores:
    def __init__(self, nome, cpf, cargo, status, telefone, naturalidade, data_nascimento,
                 email, sexo, identidade_genero, raca_cor, deficiencia,
                 aprovado_cotas, data_posse, orgao_lotacao, situacao_profissional,
                 data_inicio_situacao, data_saida_situacao=None):
        # Inicializa as variáveis de instância com os dados do servidor
        self.nome = nome
        self.cpf = cpf
        self.cargo = cargo
        self.status = status
        self.telefone = telefone
        self.naturalidade = naturalidade
        self.data_nascimento = data_nascimento
        self.email = email
        self.sexo = sexo
        self.identidade_genero = identidade_genero
        self.raca_cor = raca_cor
        self.deficiencia = deficiencia
        self.aprovado_cotas = aprovado_cotas
        self.data_posse = data_posse
        self.orgao_lotacao = orgao_lotacao
        self.situacao_profissional = situacao_profissional
        self.data_inicio_situacao = data_inicio_situacao
        self.data_saida_situacao = data_saida_situacao

    def salvar_servidor(self):
        """ Salva os dados do servidor no banco de dados SQLite. """
        try:
            # Estabelece a conexão com o banco de dados SQLite
            con = sqlite3.connect('RH_TJGO.db')
            cursor = con.cursor()

            # Insere os dados do servidor na tabela 'servidores'
            cursor.execute('''
                INSERT INTO servidores (nome, cpf, cargo, status, telefone, naturalidade, data_nascimento, 
                                        email, sexo, identidade_genero, raca_cor, deficiencia, aprovado_cotas, 
                                        data_posse, orgao_lotacao, situacao_profissional, data_inicio_situacao, 
                                        data_saida_situacao)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (self.nome, self.cpf, self.cargo, self.status, self.telefone, self.naturalidade,
                  self.data_nascimento, self.email, self.sexo, self.identidade_genero, self.raca_cor,
                  self.deficiencia, self.aprovado_cotas, self.data_posse, self.orgao_lotacao,
                  self.situacao_profissional, self.data_inicio_situacao, self.data_saida_situacao))

            # Confirma a transação no banco de dados e fecha a conexão
            con.commit()
            con.close()
            print("Servidor salvo no banco com sucesso!")
        except Exception as e:
            # Em caso de erro, exibe a mensagem de erro no console
            print(f"Erro ao salvar servidor: {e}")

# Herança de Servidores: Magistrados herda os atributos e métodos de Servidores
class Magistrados(Servidores):
    def __init__(self, nome, cpf, cargo, status):
        # Chama o construtor da classe pai (Servidores) para inicializar os atributos comuns
        super().__init__(nome, cpf, cargo, status)
        self.promocao = None  # Inicializa atributos específicos de magistrados
        self.data_promocao = None

    def salvar_magistrado(self):
        """ Salva os dados do magistrado no banco de dados SQLite. """
        try:
            # Estabelece a conexão com o banco de dados SQLite
            con = sqlite3.connect('RH_TJGO.db')
            cursor = con.cursor()

            # Insere os dados do magistrado na tabela 'magistrados'
            cursor.execute('''
                INSERT INTO magistrados (nome, cpf, cargo, status, telefone, naturalidade, data_nascimento, 
                                        email, sexo, identidade_genero, raca_cor, deficiencia, aprovado_cotas, 
                                        data_posse, orgao_lotacao, situacao_profissional, data_inicio_situacao, 
                                        data_saida_situacao,promocao, data_promocao)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (self.nome, self.cpf, self.cargo, self.status, self.telefone, self.naturalidade,
                  self.data_nascimento, self.email, self.sexo, self.identidade_genero, self.raca_cor,
                  self.deficiencia, self.aprovado_cotas, self.data_posse, self.orgao_lotacao,
                  self.situacao_profissional, self.data_inicio_situacao, self.data_saida_situacao,
                  self.promocao, self.data_promocao))

            # Confirma a transação no banco de dados e fecha a conexão
            con.commit()
            con.close()
            print("Magistrado salvo no banco com sucesso!")
        except Exception as e:
            # Em caso de erro, exibe a mensagem de erro no console
            print(f"Erro ao salvar magistrado: {e}")

# Classe para análise de dados do banco de dados
class AnalisadorDados:
    def __init__(self, db_path: str, tabela: str):
        """
        Inicializa o analisador de dados carregando os dados de uma tabela do banco SQLite.

        :param db_path: Caminho para o banco de dados SQLite.
        :param tabela: Nome da tabela a ser carregada.
        """
        self.db_path = db_path
        self.tabela = tabela
        # Carrega os dados da tabela especificada
        self.dados = self.carregar_dados()

    def carregar_dados(self) -> pd.DataFrame:
        """Carrega os dados da tabela especificada no banco de dados."""
        # Estabelece a conexão com o banco de dados SQLite
        con = sqlite3.connect(self.db_path)
        # Cria a query para selecionar todos os dados da tabela
        query = f"SELECT * FROM {self.tabela}"
        # Executa a consulta SQL e armazena o resultado em um DataFrame
        df = pd.read_sql_query(query, con)
        # Fecha a conexão com o banco de dados
        con.close()
        return df