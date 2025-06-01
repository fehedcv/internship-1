from pydantic import BaseModel,EmailStr,Field
from typing import Dict



class UpdateParam(BaseModel):
    param: str
    value: str

class MultiUpdate(BaseModel):
    updates: Dict[str, str]

