import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from graphene_example.app.core.config import settings
from graphene_example.app.db.session import init_db
from graphene_example.app.api.routes import init_gql_route

app = FastAPI(title=settings.PROJECT_NAME)
init_gql_route(app)


@app.on_event("startup")
def on_startup():
    init_db()


if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
