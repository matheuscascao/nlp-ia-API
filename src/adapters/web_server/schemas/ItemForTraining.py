from pydantic import BaseModel

class ItemForTraining(BaseModel):
    id: int
    text: str
    NAME: str
    CPF: str