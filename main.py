from fastapi import FastAPI
from database.connection import Base, Session, engine
from schemas.schema import OrgCreate, UserCreate, RoleCreate, AssignUserRole
from models.organization import Organization
from models.user import User, Role, UserRole

session = Session()
Base.metadata.create_all(bind=engine)

app = FastAPI()

#team
@app.post("/orgs")
def create_org(org: OrgCreate):
    session_org = Organization(name=org.name)
    session.add(session_org)
    session.commit()
    return {"message": "Organization created successfully"}

#fhd
@app.get("/orgs/{page_number}") 
def get_org(page_number: int, limit: int = 10):
    offset = (page_number-1) * limit
    orgs = session.query(Organization).offset(offset).limit(limit).all()
    return orgs

#fhd
@app.delete("/orgs/{org_id}")
def del_org(org_id: int):
    session_org = session.query(Organization).filter(
        Organization.id == org_id).first()
    session.delete(session_org)
    session.commit()
    return {"message": "Organization deleted successfully"}
#fhd
@app.delete("/users/{user_id}")
def del_org(user_id: int):
    session_user = session.query(User).filter(
        User.id == user_id).first()
    session.delete(session_user)
    session.commit()
    return {"message": "User deleted successfully"}

#team
@app.post("/users")
def create_user(user: UserCreate):
    new_user = User(name=user.name, email=user.email,
                    password=user.password, organization_id=user.organization_id)
    session.add(new_user)
    session.commit()
    return {"message": "User created successfully"}

#fhd
@app.get("/users/{page_number}")
def get_user(page_number: int):
    offset = (page_number-1) * 10
    users = session.query(User).offset(offset).limit(10).all()
    return users

#team
@app.post("/roles")
def create_user(newRole: RoleCreate):
    new_role = Role(name=newRole.name)
    session.add(new_role)
    session.commit()
    return {"message": "Role created successfully"}

#team
@app.get("/roles")
def get_roles():
    roles = session.query(Role).all()
    return {"Roles": roles}

#team
@app.post("/role_assign")
def assign_role(assign: AssignUserRole):
    assignRole = UserRole(user_id=assign.user_id, role_id=assign.role_id)
    session.add(assignRole)
    session.commit()
    return {"message": "Role assigned successfully"}

#team
@app.get("/assignedRoles")
def get_assigned_roles():
    assigned_roles = session.query(UserRole).all()
    return {"AssignedRoles": assigned_roles}

# -------------Put method for updating the user----------------

#prv
@app.put("/user/{user_id}")
def update_user(user_id: int, param: str, value: str):
    put_user_data = session.query(User).filter(User.id == user_id).first()
    if not put_user_data:
        return {"message": "User not found"}

    valid_params = {"name", "email", "password", "organization_id"}
    if param in valid_params:
        setattr(put_user_data, param, value)
    else:
        return {"message": "Invalid parameter"}

    session.commit()
    return {"message": "User updated successfully"}

# --------------put method for update the org name-------------

#prv
@app.put("/org/{org_id}")
def update_org(org_id: int, param: str, value: str):
    put_org_data = session.query(Organization).filter(
        Organization.id == org_id).first()
    if not put_org_data:
        return {"message": "Organization not found"}
    valid_params = {"name"}
    if param in valid_params:
        setattr(put_org_data, param, value)
    else:
        return {"message": "Invalid parameter"}
    session.commit()
    return {"message": "Organization updated successfully"}

# --------------put method for update the role name-------------

#prv
@app.put("/roles/{role_id}")
def update_role(role_id: int, param: str, value: str):
    put_role_data = session.query(Role).filter(Role.id == role_id).first()
    if not put_role_data:
        return {"message": "Role not found"}
    vaild_params = {"name"}
    if param in vaild_params:
        setattr(put_role_data, param, value)
    else:
        return {"message": "Invalid parameter"}
    session.commit()
    return {"message": "Role updated successfully"}

# ----------put method for update the user role id----------------

#prv
@app.put("/user/{user_id}/role/{role_id}")
def update_user_role(user_id: int, role_id: int):
    user_role_data = session.query(UserRole).filter(
        UserRole.user_id == user_id).first()

    if not user_role_data:
        return {"message": "User does not have a role assigned"}

    role_data = session.query(Role).filter(Role.id == role_id).first()
    if not role_data:
        return {"message": "Role not found"}

    user_role_data.role_id = role_id
    session.commit()
    return {"message": "User role updated successfully"}

#nor
@app.get("/get_user_by_id/{user_id}")
def get_user_by_id(user_id: int):
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        return {"message": "user not found"}
    return user

#nor
@app.get("/search_users/{name}")
def search_users(name: str):
    users = session.query(User).filter(User.name.ilike(f"%{name}%")).all()
    if not users:
        return {"message": "not found in that name"}
    return users

#nor
@app.get("/search_orgs/{name}")
def search_orgs(name: str):
    orgs = session.query(Organization).filter(
        Organization.name.ilike(f"%{name}%")).all()
    if not orgs:
        return {"message": "not found in data"}
    return orgs
