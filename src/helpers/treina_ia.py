import json
from spacy.tokens import Span

def treina_ia_windows(classe):
    classe_nlp = classe()

    with open('database.json', 'r') as f:
        items_db = json.load(f)
    path = "output\model-last"

    attributes = ["NAME", "CPF"]
    docs = classe_nlp.cria_ents(path, items_db, attributes)

    data_treinada = classe_nlp.treinar(docs)
    classe_nlp.salvar_arquivo(data_treinada['data_treino'],
    data_treinada['data_dev'])