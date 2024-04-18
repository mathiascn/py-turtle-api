from typing import Optional

from pydantic import BaseModel


class Turtle(BaseModel):
    id: Optional[int] = None
    label: str
    current_script: str
    coordinate_x: Optional[int] = None
    coordinate_y: Optional[int] = None
    coordinate_z: Optional[int] = None
    status: Optional[str] = None
    fuel_lvl: Optional[int] = None

    class Config:
        orm_mode = True