from flask import Flask
from .views import bp

def create_app():
    app = Flask(__name__)
    app.secret_key = 'chave_secreta_apenas_para_mensagens_flash'
    app.register_blueprint(bp)
    return app



