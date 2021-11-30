from flask import Flask

from controller.routes import urls, page_not_found


def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = True
    app.register_blueprint(urls)
    app.register_error_handler(404, page_not_found)
    app.secret_key = "anegi"
    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='localhost', port='9000', debug=True)
