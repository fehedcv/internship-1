from fastapi import APIRouter,HTTPException,Path
from database.connection import  Session
from models.user import User,Role,UserRole
from schemas.base_schemas import MultiUpdate
from schemas.user_schemas import UserCreate,UpdateUser
from controllers.base_controller import commit_session,get_object_by_id,validate_param,apply_updates,handle_update_response,get_updatable_fields

session = Session()
router = APIRouter()

@router.post("/create")
def create_user(user: UserCreate):
    #create user
    session = Session()
    try:
        new_user = User(
            name=user.name,
            email=user.email,
            password=user.password,
            organization_id=user.organization_id
        )
        session.add(new_user)
        session.commit()
        return {"message": "User created successfully"}

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

    finally:
        session.close()


#get
@router.get("/{page_number}")
def get_user(page_number: int = Path(..., gt=0, description="Page number must be greater than 0")):
    session = Session()
    try:
        offset = (page_number - 1) * 10
        users = session.query(User).offset(offset).limit(10).all()
        
        if not users:
            raise HTTPException(status_code=404, detail="No users found on this page.")
        
        return users

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

    finally:
        session.close()

@router.delete("/{user_id}")
def del_user(user_id: int):
    #delete user
    session = Session()
    try:
        session_user = session.query(User).filter(User.id == user_id).first()
        if not session_user:
            raise HTTPException(status_code=404, detail="User not found")
        session.delete(session_user)
        session.commit()
        return {"message": "User deleted successfully"}

    except HTTPException as http_err:
        raise http_err

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

    finally:
        session.close()

@router.put("/{user_id}")
def update_user(user_id: int, update: MultiUpdate):
    #update whole user
    session = Session()
    try:
        user = get_object_by_id(User, user_id, not_found_msg="User not found")
        valid_params = get_updatable_fields(User)

        for param, value in update.updates.items():
            validate_param(param, valid_params)
            setattr(user, param, value)

        session.commit()
        return {"message": "User updated successfully"}

    except HTTPException as http_err:
        raise http_err

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

    finally:
        session.close()




@router.get("/search/{name}")
def search_users(name: str):
    #search user by name
    session = Session()
    try:
        users = session.query(User).filter(User.name.ilike(f"%{name}%")).all()
        if not users:
            raise HTTPException(status_code=404, detail="No users found with that name")
        return users

    except HTTPException as http_err:
        raise http_err

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

    finally:
        session.close()

@router.patch("/{user_id}")
def updateUser(user_id: int, updateData: UpdateUser):
    #patch user
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
