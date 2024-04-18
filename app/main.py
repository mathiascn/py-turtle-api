from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .schemas import Turtle
from .models import Base, Turtles
from .db import engine, get_db


app = FastAPI()
Base.metadata.create_all(bind=engine)


@app.get("/", tags=["Root"])
def read_root():
    return {"message": "The turtles are up to something..."}


@app.get("/turtles/{label}", response_model=Turtle, tags=["Turtles"])
def read_turtle(label: str, db: Session = Depends(get_db)):
    turtle = db.query(Turtles).filter(Turtles.label == label).first()
    if turtle is None:
        raise HTTPException(status_code=404, detail="Turtle not found")
    return turtle


@app.post("/turtles", response_model=Turtle, status_code=status.HTTP_201_CREATED, tags=["Turtles"])
def create_or_update_turtle(turtle_data: Turtle, db: Session = Depends(get_db)):
    db_turtle = db.query(Turtles).filter(Turtles.label == turtle_data.label).first()
    
    if db_turtle:
        for var, value in turtle_data.model_dump(exclude_unset=True).items():
            setattr(db_turtle, var, value)
        db.commit()
        db.refresh(db_turtle)
    else:
        db_turtle = Turtles(**turtle_data.model_dump(exclude_unset=True))
        db.add(db_turtle)
        db.commit()
        db.refresh(db_turtle)

    return db_turtle


@app.get("/turtles", response_model=list[Turtle], tags=["Turtles"])
def get_all_turtles(db: Session = Depends(get_db)):
    return db.query(Turtles).all()