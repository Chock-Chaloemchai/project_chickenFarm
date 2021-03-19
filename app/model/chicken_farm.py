from typing import Optional, List
from pydantic import BaseModel, Field


# เป็นการสร้าง require ที่เป็น templace ว่าต้องใส่ให้ครบทุกตัว
class createChickenFarmModel(BaseModel):
    id: str = Field(
        min_length=3, max_length=3
    )  # lengthต้องเท่ากับ 3 คำจำกัดความคือ Field
    type_chicken: str
    amount: int
    date_put_down: str
    age_month: int
    amount_food_kg: float
    amount_water_liter: float
    temperature: str
    last_date_disinfectant: str
    latitude: float
    longitude: float


class updateChickenFarmModel(BaseModel):
    amount: Optional[int]
    age_month: Optional[int]
    amount_food_kg: Optional[float]
    amount_water_liter: Optional[float]
    temperature: Optional[str]
