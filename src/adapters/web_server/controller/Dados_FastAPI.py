from fastapi import FastAPI
from typing import Optional
import json

from src.adapters.NLP.NLP_IA import NLP_IA
from src.adapters.web_server.schemas.ItemForTraining import ItemForTraining

app = FastAPI()
with open('database.json', 'r') as f:
    items_db = json.load(f)

@app.get("/db_items")
def get_item(item_id: Optional[int] = None):
    if item_id:
        print("---------------- Not None ----------------")
        training_item = [item for item in items_db if item['id'] == item_id]
        return training_item
    else:
        print("---------------- None ----------------")
        return items_db

# epocas e betsize
@app.get("/retornar_atributo")
def retornar_atributos(texto: str):
    path = "output/model-best"
    data = NLP_IA.retornar_atributos(path, texto)

    return data

@app.post(
    "/add_item/", 
    status_code=201,
    response_description="IA Treinada",
    )
def add_item(item: ItemForTraining):
    item_id = (max([item['id'] for item in items_db]) + 1) if len(items_db) != 0 else 1
    new_item = {
        "id": item_id,
        "text": item.text,
        "NAME": item.NAME,
        "CPF": item.CPF
    }

    items_db.append(new_item)
    print(f"ITEM: {items_db}")
    with open("database.json", "w") as f:
        json.dump(items_db, f)

    NLP_IA.treina_ia_windows(NLP_IA)
    return {'message': f'Retorno do item de ID {item_id} feito com sucesso'}

@app.delete("/delete_all/")
def delete_all_items():
    item_to_be_deleted = [item for item in items_db if item['id'] != 0]
    items_db.remove(item_to_be_deleted[0])    
    print(f"item to be deleted: {item_to_be_deleted}")
    
    with open("database.json", "w") as f:
        json.dump(items_db, f)

@app.delete("/delete_by_id/{item_id}")
def delete_item(item_id: int):
    print("passed")
    item_to_be_deleted = [item for item in items_db if item['id'] == item_id]
    items_db.remove(item_to_be_deleted[0])    
    print(f"item to be deleted: {item_to_be_deleted}")
    
    with open("database.json", "w") as f:
        json.dump(items_db, f)

@app.delete("/delete_by_cpf/{item_cpf}")
def delete_item(item_cpf: str):
    item_to_be_deleted = [item for item in items_db if item['CPF'] == item_cpf]
    items_db.remove(item_to_be_deleted[0])    
    print(f"item to be deleted: {item_to_be_deleted}")
    
    with open("database.json", "w") as f:
        json.dump(items_db, f)
    