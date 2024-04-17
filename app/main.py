from typing import Annotated, Optional

from pydantic import BaseModel
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .models import Base, Turtles
from .db import engine, SessionLocal


app = FastAPI()
Base.metadata.create_all(bind=engine)


class Turtle(BaseModel):
    id: Optional[int] = None
    label: str
    coordinate_x: Optional[int] = None
    coordinate_y: Optional[int] = None
    coordinate_z: Optional[int] = None
    status: Optional[str] = None
    fuel_lvl: Optional[int] = None

    class Config:
        orm_mode = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/")
def read_root():
    return {"message": "The turtles are up to something..."}


@app.get("/turtles/{turtle_id}", response_model=Turtle)
def read_turtle(turtle_id: int, db: Session = Depends(get_db)):
    turtle = db.query(Turtles).filter(Turtles.id == turtle_id).first()
    if turtle is None:
        raise HTTPException(status_code=404, detail="Turtle not found")
    return turtle


@app.post("/turtles", response_model=Turtle)
def create_turtle(turtle: Turtle, db: Session = Depends(get_db)):
    db_turtle = Turtles(**turtle.model_dump(exclude_unset=True))
    db.add(db_turtle)
    db.commit()
    db.refresh(db_turtle)
    return db_turtle


#uvicorn app.main:app --host 0.0.0.0 --port 8001