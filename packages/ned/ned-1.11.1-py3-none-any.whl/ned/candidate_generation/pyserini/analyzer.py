from enum import Enum
from pyserini.analysis import Analyzer as PyseriniAnalyzer, get_lucene_analyzer


class AnalyzerType(str, Enum):
    DefaultEnglishAnalyzer = "default_analyzer"
    TrigramAnalyzer = "trigram_analyzer"

    def need_pretokenize(self):
        return self == AnalyzerType.TrigramAnalyzer


def DefaultEnglishAnalyzer(query):
    return query


class TrigramAnalyzer:
    def __init__(self):
        self.pyserini_analyzer = PyseriniAnalyzer(
            get_lucene_analyzer(
                language="en", stemming=True, stemmer="krovetz", stopwords=True
            )
        )

    def __call__(self, text: str):
        return " ".join(
            [
                ngram
                for token in self.pyserini_analyzer.analyze(text)
                for ngram in self.ngram_filter(token, min=3, max=4)
            ]
        )

    @staticmethod
    def ngram_filter(text, min, max):
        if len(text) <= min:
            return [text]

        size = len(text)
        output = []
        for start in range(0, size - min + 1):
            for nchar in range(min, max + 1):
                end = start + nchar
                if end > size:
                    break
                output.append(text[start:end])
        return output

    def __getstate__(self):
        return {}

    def __setstate__(self, state):
        self.__init__()
