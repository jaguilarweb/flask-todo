from flask import Flask, request, make_response, redirect, render_template

app = Flask(__name__)

todos = ['Todo1', 'Todo2', 'Todo3']

@app.route('/')
def index():
    user_ip = request.remote_addr
    response = make_response(redirect('/hello'))
    response.set_cookie('user_ip', user_ip)

    return response


@app.route('/hello')
def hello():
    user_ip = request.cookies.get('user_ip')
    context = {
        'user_ip': user_ip,
        'todos': todos
    }
    return render_template('hello.html', **context)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)