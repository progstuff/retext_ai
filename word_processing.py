from ru_synonyms import SynonymsGraph
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import wordnet
from re import search as re_search
from typing import Union, Set, List
from networkx.exception import NetworkXError as WordProcessorError
from morpholog import Morpholog


class WordProcessor:
    __instance__ = None

    def __init__(self):
        if WordProcessor.__instance__ is None:
            self.ru_processor = RussianWordsProcessing()
            self.en_processor = EnglishWordsProcessing()
            WordProcessor.__instance__ = self

    @staticmethod
    def get_instance():
        if not WordProcessor.__instance__:
            WordProcessor()
        return WordProcessor.__instance__

    def is_russian_word(self, word: str) -> bool:
        check_result = re_search('[a-zA-Z]', word)
        if check_result is None:
            return True
        return False

    def is_numbers_in_word(self, word: str) -> bool:
        check_result = re_search('[1-9]', word)
        if check_result is None:
            return False
        return True

    def get_roots(self, word: str) -> Union[None, List[str]]:
        roots = []
        if not self.is_numbers_in_word(word):
            if self.is_russian_word(word):
                synonyms = self.ru_processor.get_synonyms(word)
                roots = self.ru_processor.get_roots(synonyms)
            else:
                synonyms = self.en_processor.get_synonyms(word)
                roots = self.en_processor.get_roots(synonyms)
        return roots


class RussianWordsProcessing:
    def __init__(self):
        self._sg = SynonymsGraph()
        self._morph = Morpholog()

        # для инициализации (выполнение около 5-ти секунд)
        r = self.get_synonyms('тест')
        self.get_roots(r)

    def get_synonyms(self, word: str) -> Set[str]:
        result = []
        try:
            synonyms = self._sg.get_list(word)
            for synonym in synonyms:
                if not ('_' in synonym) and not ('-' in synonym):
                    result.append(synonym)
        except WordProcessorError:
            pass
        result.append(word)
        return set(result)

    def get_roots(self, words: set) -> List[str]:

        words_roots = []
        for word in words:
            roots = self._morph.get_roots(word)
            for root in roots:
                if root != '' and not('=' in root) and not('-' in root):
                    words_roots.append(root)

        return list(set(words_roots))


class EnglishWordsProcessing:
    def __init__(self):
        self._stemmer = SnowballStemmer('english')
        # для инициализации (выполнение около 5-ти секунд)
        r = self.get_synonyms('test')
        self.get_roots(r)

    def get_synonyms(self, word: str) -> Set[str]:
        synonyms = []
        for syn in wordnet.synsets(word):
            for lem in syn.lemmas():
                s = lem.name()
                if not('_' in s) and not('-' in s):
                    synonyms.append(s)
        synonyms.append(word)
        return set(synonyms)

    def get_roots(self, words: set) -> List[str]:
        words_roots = []
        for word in words:
            stem = self._stemmer.stem(word)
            words_roots.append(stem)
        return list(set(words_roots))
