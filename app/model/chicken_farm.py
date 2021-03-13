from typing import Optional, List
from pydantic import BaseModel, Field


# เป็นการสร้าง require ที่เป็น templace ว่าต้องใส่ให้ครบทุกตัว
class createChickenFarmModel(BaseModel):
    id: str = Field(
        min_length=3, max_length=3
    )  # lengthต้องเท่ากับ 10 คำจำกัดความคือ Field
    type_chicken: str
    amount: int
    date_put_down: str
    age_mount: int
    amount_food_kg: float
    amount_water_liter: float
    temperature: str
    last_date_disinfectant: str


class updateChickenFarmModel(BaseModel):
    amount: int
    age_mount: int
    amount_food_kg: float
    amount_water_liter: float
    temperature: str
    last_date_disinfectant: str
