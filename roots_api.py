from flask import jsonify, request
from flask_restful import Resource
from typing import Tuple, List, Dict
from word_processing import WordProcessor


class RootsAPI(Resource):

    def data_check(self, json_data: Dict[str, List[str]]) -> Tuple[str, str, bool, List[str]]:
        words = json_data.get('words', None)
        if words is None:
            return '400', 'Bad Request: no key - words', False, []
        for word in words:
            if type(word) is not str:
                return '400', 'Bad Request: bad data format', False, []
        return 'ok', '', True, words

    def post(self):
        json_data = request.get_json(force=True)
        (status, er_message, is_ok, words) = self.data_check(json_data)
        result = dict()
        result['data'] = {'word_roots': {}}
        result['status'] = status
        if is_ok:
            word_processor = WordProcessor.get_instance()
            for word in words:
                result['data']['word_roots'][word] = word_processor.get_roots(word)
        else:
            result['error_message'] = er_message
        return jsonify(result)
