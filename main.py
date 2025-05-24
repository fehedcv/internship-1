from fastapi import FastAPI
from database.connection import Base,Session,engine
from schemas.schema import OrgCreate,UserCreate,RoleCreate,AssignUserRole
from models.organization import Organization
from models.user import User,Role,UserRole

session = Session()
Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/create_org")
def create_org(org:OrgCreate):
    session_org = Organization(name = org.name)
    session.add(session_org)
    session.commit()
    return {"message":"Organization created successfully"}


@app.get("/get_orgs/{page_number}")
def get_org(page_number : int,limit : int = 10):
    offset  = (page_number-1) * limit
    orgs = session.query(Organization).offset(offset).limit(limit).all()
    return orgs
    

@app.delete("/delete_org/{org_id}")
def del_org(org_id:int):
    session_org = session.query(Organization).filter(Organization.id == org_id).first()
    session.delete(session_org)
    session.commit()
    return {"message":"Organization deleted successfully"}
    
@app.post("/create_user")
def create_user(user:UserCreate):
    new_user = User(name = user.name,email = user.email , password = user.password, organization_id = user.organization_id, is_customer = user.is_customer)
    session.add(new_user)
    session.commit()
    return {"message":"User created successfully"}


@app.get("/get_users/{page_number}")
def get_user(page_number:int):
    offset = (page_number-1) * 10
    users = session.query(User).offset(offset).limit(10).all()
    return users


@app.post("/create_role")
def create_user(newRole:RoleCreate):
    new_role = Role(name = newRole.name)
    session.add(new_role)
    session.commit()
    return {"message": "Role created successfully"}


@app.get("/get_roles")
def get_roles():
    roles = session.query(Role).all()
    return {"Roles":roles}

@app.post("/role_assign")
def assign_role(assign:AssignUserRole):
    assignRole = UserRole(user_id = assign.user_id, role_id = assign.role_id)
    session.add(assignRole)
    session.commit()
    return {"message": "Role assigned successfully"}

@app.get("/AssignedRoles")
def get_assigned_roles():
    assigned_roles = session.query(UserRole).all()
    return {"AssignedRoles":assigned_roles}

