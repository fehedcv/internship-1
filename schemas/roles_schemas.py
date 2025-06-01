from pydantic import BaseModel

class RoleCreate(BaseModel):
    name : str
    
class AssignUserRole(BaseModel):
    role_id : int
    user_id : int
