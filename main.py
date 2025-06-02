from fastapi import FastAPI
from database.connection import Base, engine
from routes import roles_routes,user_routes,organization_routes

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_routes.router,prefix="/users")
app.include_router(organization_routes.router,prefix="/orgs")
app.include_router(roles_routes.router,prefix="/roles")