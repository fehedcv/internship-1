from fastapi import APIRouter,HTTPException
from database.connection import  Session
from models.user import User,Role,UserRole
from schemas.base_schemas import MultiUpdate
from schemas.user_schemas import UserCreate,UpdateUser
from controllers.base_controller import commit_session,get_object_by_id,validate_param,apply_updates,handle_update_response,get_updatable_fields

session = Session()
router = APIRouter()

@router.post("/create")
def create_user(user: UserCreate):
    new_user = User(name=user.name, email=user.email,
                    password=user.password, organization_id=user.organization_id)
    session.add(new_user)
    commit_session()
    return {"message": "User created successfully"}

@router.get("/{page_number}")
def get_user(page_number: int):
    offset = (page_number-1) * 10
    users = session.query(User).offset(offset).limit(10).all()
    return users

# error 500 not working delete method 
@router.delete("/{user_id}")
def del_user(user_id: int,):  # fixed function name conflict
    session_user = session.query(User).filter(User.id==user_id).first()
    session.delete(session_user)
    commit_session()
    return {"message": "User deleted successfully"}

@router.put("/{user_id}")
def update_user(user_id: int, update: MultiUpdate):
    user = get_object_by_id(User, user_id, not_found_msg="User not found")
    valid_params = get_updatable_fields(User)
    for param, value in update.updates.items():
        validate_param(param, valid_params)
        setattr(user, param, value)
    commit_session()
    return {"message": "User updated successfully"}

@router.put("/{user_id}/roles/{role_id}")
def update_user_role(user_id: int, role_id: int):
    user_role = get_object_by_id(UserRole, user_id, 'user_id', "User does not have a role assigned")
    _ = get_object_by_id(Role, role_id, not_found_msg="Role not found")
    user_role.role_id = role_id
    commit_session()
    return {"message": "User role updated successfully"}

@router.get("/{user_id}")
def get_user_by_id(user_id: int):
    user = get_object_by_id(User, user_id, not_found_msg="User not found")
    return user

@router.get("/{name}")
def search_users(name: str):
    users = session.query(User).filter(User.name.ilike(f"%{name}%")).all()
    if not users:
        raise HTTPException(status_code=404, detail="No users found with that name")
    return users

@router.patch("/{user_id}")
def updateUser(user_id: int, updateData: UpdateUser):
    try:
        userData = get_object_by_id(User, user_id, not_found_msg="User not found")

        allowed_fields = get_updatable_fields(User)
        updated = apply_updates(userData, updateData, allowed_fields)
        handle_update_response(updated)

        commit_session()
        return {"message": "User updated successfully"}

    except HTTPException as http_err:
        raise http_err

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

    finally:
        session.close()
