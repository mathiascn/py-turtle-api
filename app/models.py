from sqlalchemy import Column, Integer, String, DateTime, text, event

from .db import Base, SessionLocal

class Turtles(Base):
    __tablename__ = "turtles"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    label = Column(String(255), nullable=False, unique=True)
    coordinate_x = Column(Integer, nullable=True)
    coordinate_y = Column(Integer, nullable=True)
    coordinate_z = Column(Integer, nullable=True)
    status = Column(String(255), nullable=True)
    current_script = Column(String(255), nullable=False)
    fuel_lvl = Column(Integer, nullable=False)
    date_update = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


# @event.listens_for(Turtles.__table__, 'after_create')
# def initial_data(target, connection, **kwargs):
#     data = [
#         {"label": "test", "coordinate_x": -1, "coordinate_y": -1, "coordinate_z": -1, "status": "testing", "fuel_lvl": 50}
#     ]

#     session = SessionLocal(bind=connection)
#     session.add_all([Turtles(**entry) for entry in data])
#     session.commit()
#     session.close()