from flask import Flask
from flask_restful import Api
from roots_api import RootsAPI
from word_processing import WordProcessor

if __name__ == '__main__':
    # инициализация словарей перед стартом сервера (около 10 секунд)
    a = WordProcessor.get_instance()
    app = Flask(__name__)
    app.config['JSON_AS_ASCII'] = False
    api = Api(app)
    api.add_resource(RootsAPI, '/api/v1/word_roots')
    app.run(debug=False)