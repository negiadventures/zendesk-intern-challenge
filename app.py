from flask import Flask

from controller.routes import urls


def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = True
    app.register_blueprint(urls)
    app.secret_key = "anegi"
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='localhost', port='9000', debug=True)
