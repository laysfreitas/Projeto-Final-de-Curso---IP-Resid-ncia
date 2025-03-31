from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Length, Email, Regexp

class formServidor(FlaskForm):
    # Campos de texto
    nome = StringField('Nome', validators=[DataRequired(message="Preenchimento obrigatório."), Length(min=2, max=50)])
    cpf = StringField('CPF', validators=[DataRequired(message="Preenchimento obrigatório."), Length(min=11, max=11), Regexp('^\\d{11}$', message="CPF inválido!")])
    email = StringField('Email', validators=[DataRequired(message="Preenchimento obrigatório."),Email(message="Email inválido!")])

    # Campos de select
    cargo = SelectField('Cargo', choices=[
        ('Servidor(a) efetivo(a) ou removido(a) para o Tribunal', 'Servidor(a) efetivo(a) ou removido(a) para o Tribunal'),
        ('Servidor(a) cedido(a) ou requisitado(a) de outro tribunal', 'Servidor(a) cedido(a) ou requisitado(a) de outro tribunal'),
        ('Servidor(a) cedido(a) ou requisitado(a) de órgãos de fora do judiciário', 'Servidor(a) cedido(a) ou requisitado(a) de órgãos de fora do judiciário'),
        ('Servidor(a) Comissionado(a) Sem vínculo', 'Servidor(a) Comissionado(a) Sem vínculo'),
        ('Estagiário(a)', 'Estagiário(a)'),
        ('Terceirizado(a)', 'Terceirizado(a)'),
        ('Servidor(a) de serventia privatizada', 'Servidor(a) de serventia privatizada'),
        ('Juiz(a) leigo(a)', 'Juiz(a) leigo(a)'),
        ('Conciliador(a)', 'Conciliador(a)'),
        ('Aprendiz', 'Aprendiz'),
        ('Voluntário(a)', 'Voluntário(a)'),
        ('Residência Jurídica', 'Residência Jurídica'),
        ('Outros', 'Outros')
    ], validators=[DataRequired(message="Preenchimento obrigatório.")])

    status = SelectField('Status', choices=[
        ('Ativo', 'Ativo'), 
        ('Inativo', 'Inativo')
    ], validators=[DataRequired(message="Preenchimento obrigatório.")])

    telefone = StringField('Telefone', validators=[DataRequired(message="Preenchimento obrigatório.")])

    sexo = SelectField('Sexo', choices=[
        ('Masculino', 'Masculino'),
        ('Feminino', 'Feminino'),
        ('Não declarado', 'Não declarado'),
        ('Intersex', 'Intersex'),
    ], validators=[DataRequired(message="Preenchimento obrigatório.")])

    naturalidade = SelectField('Naturalidade', choices=[
        ('AC', 'AC'),
        ('AL', 'AL'),
        ('AP', 'AP'),
        ('AM', 'AM'),
        ('BA', 'BA'),
        ('CE', 'CE'),
        ('DF', 'DF'),
        ('ES', 'ES'),
        ('GO', 'GO'),
        ('MA', 'MA'),
        ('MT', 'MT'),
        ('MS', 'MS'),
        ('MG', 'MG'),
        ('PA', 'PA'),
        ('PB', 'PB'),
        ('PR', 'PR'),
        ('PE', 'PE'),
        ('PI', 'PI'),
        ('RJ', 'RJ'),
        ('RN', 'RN'),
        ('RS', 'RS'),
        ('RO', 'RO'),
        ('RR', 'RR'),
        ('SC', 'SC'),
        ('SP', 'SP'),
        ('SE', 'SE'),
        ('TO', 'TO'),
        ('EX', 'EX') # Para servidores que são estrangeiros
    ], validators=[DataRequired(message="Preenchimento obrigatório.")])

    raca_cor = SelectField('Raça/Cor', choices=[
        ('Amarelo', 'Amarelo'),
        ('Branco', 'Branco'),
        ('Índigena', 'Índigena'),
        ('Negro(a) - Pardo(a)', 'Negro(a) - Pardo(a)'),
        ('Negro(a) - Preto(a)', 'Negro(a) - Preto(a)'),
    ], validators=[DataRequired(message="Preenchimento obrigatório.")])

    identidade_genero = SelectField('Identidade de Gênero', choices=[
        ('Cisgênero', 'Cisgênero'),
        ('Transgênero', 'Transgênero'),
        ('Transexual', 'Transexual'),
        ('Travesti', 'Travesti'),
        ('Gênero fluido', 'Gênero fluido'),
        ('Agênero', 'Agênero'),
        ('Outra', 'Outra')
    ], validators=[DataRequired(message="Preenchimento obrigatório.")])

    aprovado_cotas = SelectField('Aprovado em Cotas', choices=[
        ('Não', 'Não'),
        ('Cota étnico-racial', 'Cota étnico-racial'),
        ('Cota para pessoa com deficiência', 'Cota para pessoa com deficiência'),
        ('Cota para Gênero', 'Cota para Gênero'),
        ('Cota para outras ações afirmativas', 'Cota para outras ações afirmativas'),
        ('Cota para Indígenas', 'Cota para Indígenas'),
        ('Reserva de vagas para a Resolução n. 497', 'Reserva de vagas para a Resolução n. 497')
    ], validators=[DataRequired(message="Preenchimento obrigatório.")])

    # Campos de checkbox para deficiência
    deficiencia = SelectMultipleField('Deficiência', choices=[
        ('fisica', 'Física/motora'),
        ('auditiva', 'Auditiva'),
        ('visual', 'Visual'),
        ('intelectual', 'Intelectual'),
        ('psicossocial', 'Psicossocial'),
        ('mental', 'Mental'),
        ('outras', 'Outras deficiências'),
        ('nao_possui', 'Não possui')
    ], coerce=str, validators=[DataRequired(message="Preenchimento obrigatório.")])

    # Campos de data
    data_nascimento = StringField('Data de Nascimento', validators=[DataRequired(message="Preenchimento obrigatório.")])
    data_posse = StringField('Data de Posse', validators=[DataRequired(message="Preenchimento obrigatório.")])

    # Outros campos
    orgao_lotacao = StringField('Órgão de Lotação', validators=[DataRequired(message="Preenchimento obrigatório."), Length(max=50)])
    situacao_profissional = SelectField('Situação Profissional', choices=[
        ('Cargo de chefia', 'Cargo de chefia'),
        ('Outros cargos em comissão', 'Outros cargos em comissão'),
        ('Não exerce cargo em comissão', 'Não exerce cargo em comissão'),
        ('Afastado(a)', 'Afastado(a)'),
        ('Aposentado(a)', 'Aposentado(a)'),
        ('Falecido(a)', 'Falecido(a)'),
        ('Exoneração/Vacância', 'Exoneração/Vacância'),
        ('Demitido(a)', 'Demitido(a)'),
        ('Saída por Remoção', 'Saída por Remoção'),
        ('Saída por cessão/requisição', 'Saída por cessão/requisição'),
        ('Vigência de Contrato/Vínculo', 'Vigência de Contrato/Vínculo')
    ], validators=[DataRequired(message="Preenchimento obrigatório.")])

    data_inicio_situacao = StringField('Data de Início da Situação', validators=[DataRequired(message="Preenchimento obrigatório.")])
    data_saida_situacao = StringField('Data de Saída da Situação')

class formMagistrado(FlaskForm):
    # Campos de texto
    nome = StringField('Nome', validators=[DataRequired(message="Preenchimento obrigatório."), Length(min=2, max=50)])
    cpf = StringField('CPF', validators=[DataRequired(message="Preenchimento obrigatório."), Length(min=11, max=11), Regexp('^\\d{11}$', message="CPF inválido!")])
    email = StringField('Email', validators=[DataRequired(message="Preenchimento obrigatório."), Email(message="Email inválido!")])

    # Campos de select
    cargo = SelectField('Cargo', choices=[
        ('Juiz(a) Titular', 'Juiz(a) Titular'),
        ('Juiz(a) Substituto(a)', 'Juiz(a) Substituto(a)'),
        ('Juiz(a) substituto(a) de 2º grau', 'Juiz(a) substituto(a) de 2º grau'),
        ('Desembargador(a)', 'Desembargador(a)'),
        ('Ministro(a) ou Conselheiro(a)', 'Ministro(a) ou Conselheiro(a)'),
        ('Magistrado(a) que atua no 1º grau eleitoral', 'Magistrado(a) que atua no 1º grau eleitoral'),
        ('Magistrado(a) que atua como titular no 2º grau eleitoral ou no TSE', 'Magistrado(a) que atua como titular no 2º grau eleitoral ou no TSE'),
        ('Magistrado(a) que atua como substituto no 2º grau eleitoral ou no TSE', 'Magistrado(a) que atua como substituto no 2º grau eleitoral ou no TSE'),
        ('Juiz(a) da classe advogado que atua como titular no TRE ou TSE', 'Juiz(a) da classe advogado que atua como titular no TRE ou TSE'),
        ('Juiz(a) da classe advogado que atua como substituto no TRE ou no TSE', 'Juiz(a) da classe advogado que atua como substituto no TRE ou no TSE'),
        ('Juiz Auxiliar que atua no 1º grau', 'Juiz Auxiliar que atua no 1º grau')
    ], validators=[DataRequired(message="Preenchimento obrigatório.")])

    status = SelectField('Status', choices=[
        ('Ativo', 'Ativo'), 
        ('Inativo', 'Inativo')
    ], validators=[DataRequired(message="Preenchimento obrigatório.")])

    telefone = StringField('Telefone', validators=[DataRequired(message="Preenchimento obrigatório.")])

    sexo = SelectField('Sexo', choices=[
        ('Masculino', 'Masculino'),
        ('Feminino', 'Feminino'),
        ('Não declarado', 'Não declarado'),
        ('Intersex', 'Intersex')
    ], validators=[DataRequired(message="Preenchimento obrigatório.")])

    naturalidade = SelectField('Naturalidade', choices=[
        ('AC', 'AC'),
        ('AL', 'AL'),
        ('AP', 'AP'),
        ('AM', 'AM'),
        ('BA', 'BA'),
        ('CE', 'CE'),
        ('DF', 'DF'),
        ('ES', 'ES'),
        ('GO', 'GO'),
        ('MA', 'MA'),
        ('MT', 'MT'),
        ('MS', 'MS'),
        ('MG', 'MG'),
        ('PA', 'PA'),
        ('PB', 'PB'),
        ('PR', 'PR'),
        ('PE', 'PE'),
        ('PI', 'PI'),
        ('RJ', 'RJ'),
        ('RN', 'RN'),
        ('RS', 'RS'),
        ('RO', 'RO'),
        ('RR', 'RR'),
        ('SC', 'SC'),
        ('SP', 'SP'),
        ('SE', 'SE'),
        ('TO', 'TO'),
        ('EX', 'EX') # Para servidores que são estrangeiros
    ], validators=[DataRequired(message="Preenchimento obrigatório.")])

    raca_cor = SelectField('Raça/Cor', choices=[
        ('Amarelo', 'Amarelo'),
        ('Branco', 'Branco'),
        ('Índigena', 'Índigena'),
        ('Negro(a) - Pardo(a)', 'Negro(a) - Pardo(a)'),
        ('Negro(a) - Preto(a)', 'Negro(a) - Preto(a)'),
    ], validators=[DataRequired(message="Preenchimento obrigatório.")])

    identidade_genero = SelectField('Identidade de Gênero', choices=[
        ('Cisgênero', 'Cisgênero'),
        ('Transgênero', 'Transgênero'),
        ('Transexual', 'Transexual'),
        ('Travesti', 'Travesti'),
        ('Gênero fluido', 'Gênero fluido'),
        ('Agênero', 'Agênero'),
        ('Outra', 'Outra')
    ], validators=[DataRequired(message="Preenchimento obrigatório.")])

    aprovado_cotas = SelectField('Aprovado em Cotas', choices=[
        ('Não', 'Não'),
        ('Cota étnico-racial', 'Cota étnico-racial'),
        ('Cota para pessoa com deficiência', 'Cota para pessoa com deficiência'),
        ('Cota para Gênero', 'Cota para Gênero'),
        ('Cota para outras ações afirmativas', 'Cota para outras ações afirmativas'),
        ('Cota para Indígenas', 'Cota para Indígenas')
    ], validators=[DataRequired(message="Preenchimento obrigatório.")])

    # Campos de checkbox para deficiência
    deficiencia = SelectMultipleField('Deficiência', choices=[
        ('fisica', 'Física/motora'),
        ('auditiva', 'Auditiva'),
        ('visual', 'Visual'),
        ('intelectual', 'Intelectual'),
        ('psicossocial', 'Psicossocial'),
        ('mental', 'Mental'),
        ('outras', 'Outras deficiências'),
        ('nao_possui', 'Não possui')
    ], coerce=str, validators=[DataRequired(message="Preenchimento obrigatório.")])

    # Campos de data
    data_nascimento = StringField('Data de Nascimento', validators=[DataRequired(message="Preenchimento obrigatório.")])
    data_posse = StringField('Data de Posse', validators=[DataRequired(message="Preenchimento obrigatório.")])

    # Outros campos
    orgao_lotacao = StringField('Órgão de Lotação', validators=[DataRequired(message="Preenchimento obrigatório."), Length(max=50)])

    # Campos de select para Situação Profissional
    situacao_profissional = SelectField('Situação Profissional', choices=[
        ('presidente_tribunal', 'Presidente do tribunal'),
        ('vice_presidente_tribunal', 'Vice-presidente do tribunal'),
        ('diretor_escola_magistratura', 'Diretor(a) de escola da magistratura'),
        ('ouvidor', 'Ouvidor(a)'),
        ('corregedor', 'Corregedor(a)'),
        ('juiz_convocado_substituicao', 'Juiz(a) convocado(a) para substituição de desembargador(a) ou Ministro(a)'),
        ('juiz_auxiliar_instrutor', 'Juiz(a) Auxiliar ou Juiz(a) Instrutor(a) que atua em Tribunal/Conselho'),
        ('ocupante_cargo_jurisdicao', 'Ocupante de cargo próprio na Jurisdição'),
        ('afastado_decisao_administrativa', 'Afastado(a) por decisão administrativa'),
        ('licencas_concessoes', 'Licenças ou concessões previstas em lei'),
        ('ingresso_remocao_externa', 'Ingresso por Remoção externa'),
        ('aposentado', 'Aposentado(a)'),
        ('falecido', 'Falecido(a)'),
        ('exonerado', 'Exonerado(a)'),
        ('demitido', 'Demitido(a)'),
        ('diretor_foro', 'Diretor(a) de foro'),
        ('saida_remocao_externa', 'Saída por Remoção Externa'),
        ('ocupante_acumulacao_jurisdicao', 'Ocupante de cargo em acumulação na Jurisdição'),
        ('magistrado_convocado_outro_tribunal', 'Magistrado(a) convocado para atuar em outro Tribunal ou Conselho')
    ], validators=[DataRequired(message="Preenchimento obrigatório.")])


    data_inicio_situacao = StringField('Data de Início da Situação', validators=[DataRequired(message="Preenchimento obrigatório.")])
    data_saida_situacao = StringField('Data de Saída da Situação')

    # Campos para promoção
    promocao = SelectField('Promoção', choices=[
        ('nao_possui', 'Não possui'),
        ('desembargador_quinto_oab', 'Desembargador(a) por Quinto Constitucional/OAB'),
        ('desembargador_quinto_mp', 'Desembargador(a) por Quinto Constitucional/MP'),
        ('desembargador_antiguidade', 'Desembargador(a) por Antiguidade'),
        ('desembargador_merecimento_mista', 'Desembargador(a) por Merecimento lista mista'),
        ('desembargadora_merecimento_mulher', 'Desembargadora por Merecimento lista mulher'),
        ('juiz_titular_antiguidade', 'Juiz(a) Titular por Antiguidade'),
        ('juiz_titular_merecimento', 'Juiz(a) Titular por Merecimento'),
    ])

    data_promocao = StringField('Data da Promoção')