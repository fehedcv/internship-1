from fastapi import FastAPI,HTTPException
from database.connection import Base, Session, engine
from schemas.schema import OrgCreate, UserCreate, RoleCreate, AssignUserRole,UpdateUser
from models.organization import Organization
from models.user import User, Role, UserRole
from sqlalchemy.orm import Session as f_Session
from schemas.schema import UpdateParam,MultiUpdate

session = Session()
Base.metadata.create_all(bind=engine)

app = FastAPI()
# -------------functions for repeated code----------------

def get_object_by_id(model, obj_id, id_field='id', not_found_msg='Object not found', session: f_Session = session):
    obj = session.query(model).filter(getattr(model, id_field) == obj_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail=not_found_msg)
    return obj

def validate_param(param, valid_params):
    if param not in valid_params:
        raise HTTPException(status_code=400, detail=f"Invalid parameter: {param}")

def set_and_commit(obj, param, value):
    try:
        setattr(obj, param, value)
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))

def commit_session():
    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
# ------------function end here-------------


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
@app.put("/users/{user_id}")
def update_user(user_id: int, update: MultiUpdate):
    user = get_object_by_id(User, user_id, not_found_msg="User not found")
    valid_params = {"name", "email", "password", "organization_id"}

    for param, value in update.updates.items():
        validate_param(param, valid_params)
        setattr(user, param, value)
    commit_session()
    return {"message": "User updated successfully"}

# --------------put method for update the org name-------------

#prv
@app.put("/orgs/{org_id}")
def update_org(org_id: int, update: UpdateParam):
    org = get_object_by_id(Organization, org_id, not_found_msg="Organization not found")
    validate_param(update.param, {"name"})
    set_and_commit(org, update.param, update.value)
    return {"message": "Organization updated successfully"}

# --------------put method for update the role name-------------

#prv
@app.put("/roles/{role_id}")
def update_role(role_id: int, update: UpdateParam):
    role = get_object_by_id(Role, role_id, not_found_msg="Role not found")
    validate_param(update.param, {"name"})
    set_and_commit(role, update.param, update.value)
    return {"message": "Role updated successfully"}

# ----------put method for update the user role id----------------

#prv
@app.put("/users/{user_id}/roles/{role_id}")
def update_user_role(user_id: int, role_id: int):
    user_role = get_object_by_id(UserRole, user_id, 'user_id', "User does not have a role assigned")
    _ = get_object_by_id(Role, role_id, not_found_msg="Role not found")
    user_role.role_id = role_id
    commit_session()
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

#sha
@app.patch("/users/{user_id}")
def updateUser(user_id: int, updateData: UpdateUser):
    message = ""
    try:
        userData = session.query(User).filter(User.id == user_id).first()
        if not userData:
            message = "User not found"
            raise HTTPException(status_code=404, detail=message)

        updated = False 

        if updateData.name is not None:
            userData.name = updateData.name
            updated = True

        if updateData.email is not None:
            userData.email = updateData.email
            updated = True

        if not updated:
            message = "No data provided to update"
            raise HTTPException(status_code=400, detail=message)

        session.commit()
        message = "User updated successfully"
        return {"message": message}

    except HTTPException as http_err:
        message = http_err.detail
        raise http_err

    except Exception as e:
        session.rollback()
        message = "User update failed due to internal error"
        raise HTTPException(status_code=500, detail=f"Internal Server Error:{e}")

    finally:
        print(f"Update status: {message}")
        session.close()

