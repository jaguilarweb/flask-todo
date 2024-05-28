from flask import Flask, request, make_response, redirect, render_template, session, url_for, flash
from flask_bootstrap import Bootstrap # type: ignore
from flask_wtf import FlaskForm # type: ignore
from wtforms.fields import StringField, SubmitField # type: ignore
from wtforms.validators import DataRequired # type: ignore
import unittest 


app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = 'SUPER SECRET WORD'

todos = [
        'Comprar café',
        'Enviar solicitud de compra',
        'Entregar video a productor'
        ]

class LoginForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    password = StringField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Enviar')

@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html', error=error)

@app.route('/')
def index():
    user_ip = request.remote_addr
    response = make_response(redirect('/hello'))
    session['user_ip'] = user_ip

    return response


@app.route('/hello', methods=['GET', 'POST'])
def hello():
    user_ip = session.get('user_ip')
    loginForm = LoginForm()
    username = session.get('username')

    context = {
        'user_ip': user_ip,
        'todos': todos,
        'loginForm': loginForm,
        'username': username
    }

    if loginForm.validate_on_submit():
        username = loginForm.username.data
        session['username'] = username

        flash('Nombre de usuario registrado con éxito')

        return redirect(url_for('index'))

    return render_template('hello.html', **context)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)