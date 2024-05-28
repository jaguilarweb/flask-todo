from flask import Flask, request, make_response, redirect, render_template, session
from flask_bootstrap import Bootstrap # type: ignore
from flask_wtf import FlaskForm # type: ignore
from wtforms.fields import StringField, SubmitField # type: ignore
from wtforms.validators import DataRequired # type: ignore


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


@app.route('/hello')
def hello():
    user_ip = session.get('user_ip')
    loginForm = LoginForm()
    context = {
        'user_ip': user_ip,
        'todos': todos,
        'loginForm': loginForm
    }
    return render_template('hello.html', **context)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)