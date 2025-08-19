from contextlib import asynccontextmanager
from fastapi import FastAPI
from api.db.db import Base, engine
from api.router.user import router as user_router
from api.router.workout import router as workout_router
from api.router.nutrition import router as nutrition_router
from api.router.progress import router as progress_router
from api.router.lang import router as chat_router



async def init_models():
    async with engine.begin() as conn:
        # Create all tables in the database
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def lifespan(app: FastAPI):

        
    await init_models()
    yield

app=FastAPI(lifespan=lifespan)



@app.get("/health")
def check_status():
    return {
        "success":True
    }

app.include_router(user_router)
app.include_router(workout_router)
app.include_router(nutrition_router)
app.include_router(progress_router)
app.include_router(chat_router)

