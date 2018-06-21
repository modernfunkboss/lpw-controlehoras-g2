from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Length

class FuncionarioForm(FlaskForm):
    matricula = IntegerField('Matricula')
    nome = StringField('Nome', validators=[DataRequired(), Length(1, 64)])
    admin = BooleanField('Administrador')
    password = PasswordField('Password', validators=[DataRequired(), Length(min=3, max=64)])
    salvar = SubmitField('Cadastrar')
    cancelar = SubmitField('Cancelar')

    def validacao(__self__, form):
    	print('password ' + form.password.data)
    	if form.nome.data == '' or form.password.data == '':
    		print('Algum campo vazio!')
    		return True
    	return False

    def validInteger(__self__, matricula):
    	if type(matricula) == int:
    		print('number')
    		return False
    	return True