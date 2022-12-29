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

    def __cria_obj_ents(self, model, data, attributes):
        # Retorna lista de objetos com atributos: matches
        nlp = spacy.load(model)

        # Lista de objetos com texto e atributos: 
        dadosPreparados = []
        for item in data:
            matchesObjeto = {
                "text": item["text"]
            }

            for attribute in attributes:
                doc = nlp(item["text"])
                pattern = [nlp.make_doc(item[attribute])]

                matcher = PhraseMatcher(nlp.vocab)
                matcher.add(attribute, pattern)
                matches = matcher(doc)  
                
                matchesObjeto[attribute] = matches[0] #retorna uma tupla com os dados do match: id, posicao inicial, posicao final

            dadosPreparados.append(matchesObjeto)
        return dadosPreparados # lista de objetos: recebe uma lista de objetos e retorna outra lista de objetos com texto e informações sobre os atributos 
    
    def retorna_docs_preparados(self, model, data, attributes):
        #retorna lista de docs com ents adicionados com base na __cria_obj_ents
        nlp = spacy.load(model)
        data = self.__cria_obj_ents(model, data, attributes)

        docs_com_ents = []
        for item in data:
            print(item)
            doc = nlp(item["text"])
            doc.ents = ""
            for attribute in attributes:
                doc.set_ents([Span(doc, item[attribute][1], item[attribute][2], label=attribute)], default="unmodified") #Adiciona as ents ao doc
                print("-------------------------------------")
            docs_com_ents.append(doc) # a cada iteracao da lista, adiciona um doc a lista de docs

        return docs_com_ents
    
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
        print("DOCSa: ", doc.ents)
        
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