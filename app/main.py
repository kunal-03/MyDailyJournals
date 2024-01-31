from fastapi import FastAPI
from .routers import journal, user, auth, vote
from .db.database import engine
from .models import models

models.Base.metadata.create_all(bind=engine)



app = FastAPI()

app.include_router(journal.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


