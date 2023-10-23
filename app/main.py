from fastapi import FastAPI, HTTPException, Depends
import sqlalchemy
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from app.model import SessionLocal, add_restaurant, get_all_restaurants

app = FastAPI()

dbEngine = sqlalchemy.create_engine(
    'sqlite:////home/stephen/db1.db')  # ensure this is the correct path for the sqlite file.


class InfoBase(BaseModel):
    voto_medio: Optional[float] = None
    tipo_piatto_principale: Optional[str] = None
    prezzo_piatto_principale: Optional[float] = None
    voto_piatto_principale: Optional[float] = None
    distanza_dal_centro: Optional[float] = None


class Info(InfoBase):

    class Config:
        orm_mode = True


class RestaurantBase(BaseModel):
    name: str
    type: str
    address: str
    info: Optional[InfoBase] = None


class Restaurant(RestaurantBase):

    class Config:
        orm_mode = True


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    # redirect to docs
    return RedirectResponse("/docs")


@app.post("/restaurants/import")
async def save_list(source: list[Restaurant],  session: Session = Depends(get_db)):
    try:
        for i in source:
            add_restaurant(session, i.name, i.type, i.address, i.info)
        return {"message": f"Operation Completed"}
    except Exception as ex:
        print(ex)
        session.rollback()
        raise HTTPException(status_code=400, detail="Error occurred")
    finally:
        session.close()


@app.get("/restaurants", response_model=list[Restaurant])
def get_restaurants(session: Session = Depends(get_db)):
    try:
        result = get_all_restaurants(session)
        return result
    except Exception as ex:
        print(ex)
        raise HTTPException(status_code=500, detail="Error occurred")

