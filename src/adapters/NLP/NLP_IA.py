import spacy
from spacy.tokens import Span
from spacy.tokens import DocBin
from spacy.matcher import PhraseMatcher

from random import shuffle
import os

from src.helpers.treina_ia import treina_ia_windows

class NLP_IA():
    def __init__(self):
        pass

    def treinar(self, data):
        shuffle(data)
        proporcao_de_treino = len(data)//5

        data_treino = data[proporcao_de_treino:]
        data_teste = data[:proporcao_de_treino]

        data_final = {
            'data_treino': DocBin(docs=data_treino),
            'data_dev': DocBin(docs=data_teste),
        }
        
        return data_final

    def cria_ents(self, model, data, attributes):
        nlp = spacy.load(model)
        matcher = PhraseMatcher(nlp.vocab)
        
        print(data)
        dadosPreparados = []
        for item in data:
            doc = nlp(item["text"])
            for index, attribute in enumerate(attributes):
                pattern = [nlp.make_doc(item[attribute])]
                matcher.add(attribute, pattern)
                
                matches = matcher(doc)

                doc.set_ents([Span(doc, matches[index][1], matches[index][2], label=attribute)], default="unmodified")
                print("")
                print("DOC: ", doc)
                print("DOC: ", doc.ents)
                dadosPreparados.append(doc)

        return dadosPreparados

    def salvar_arquivo(self, data_treino, data_dev):
        data_treino.to_disk("./train.spacy")
        data_dev.to_disk("./dev.spacy")

    def retornar_nome(self, model_path, texto):
        nlp = spacy.load(model_path)
        docTeste = nlp(texto)

    @staticmethod
    def retornar_atributos(path, texto):
        nlp = spacy.load(path)
        doc = nlp(texto)

        print("DOCS: ", doc)
        print("DOCS: ", doc.ents)
        print("Texto: ", texto)
        
        data = {
            "texto_bruto": texto,
            doc.ents[0].label_: doc.ents[0].text,
            doc.ents[1].label_: doc.ents[1].text
        }
        return data

    @staticmethod
    def treina_ia_windows(self):
        print("Treinando IA com os arquivos")

        treina_ia_windows(self)
        os.system("python -m spacy train config.cfg --output output --paths.train train.spacy --paths.dev dev.spacy")