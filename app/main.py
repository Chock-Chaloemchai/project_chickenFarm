import uvicorn
from fastapi import FastAPI, Path, Query, HTTPException
from starlette.responses import JSONResponse
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware

from database.mongodb import MongoDB
from config.development import config

from model.chicken_farm import createChickenFarmModel, updateChickenFarmModel

mongo_config = config["mongo_config"]
mongo_db = MongoDB(
    mongo_config["host"],
    mongo_config["port"],
    mongo_config["user"],
    mongo_config["password"],
    mongo_config["auth_db"],
    mongo_config["db"],
    mongo_config["collection"],
)

mongo_db._connect()  # (เชื่อมต่อ mongo)

app = FastAPI()

app.add_middleware(  # ดักเพื่อไม่ให้คนอื่นเข้ามา แต่อันนี้ใส่ * ไว้คือเข้าได้ทุกคน
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")  # get เป็นการค้นหา
def index():
    return JSONResponse(content={"message": "Chicken farm Info"}, status_code=200)


@app.get("/chickenfarms/")  # get เป็นการค้นหา("/students/") คือนักเรียนทุกคน
def get_chicken_farm(
    sort_by: Optional[str] = None,
    order: Optional[str] = Query(
        None, min_length=3, max_length=4
    ),  # ให้ใส่อย่างน้อย 3 แต่ห้ามเกิน 4
):

    try:
        result = mongo_db.find(sort_by, order)
    except:
        raise HTTPException(status_code=500, detail="Something went wrong !!")

    return JSONResponse(
        content={"status": "OK", "data": result},
        status_code=200,
    )


@app.get(
    "/chickenfarms/{chicken_farm_id}"
)  # path parametor #get เป็นการค้นหา("/students/") คือนักเรียนตาม id ของแต่ละคน
def get_chicken_farm_id(
    chicken_farm_id: str = Path(None, min_length=3, max_length=3)
):  # ใส่ค่าต้องเท่ากับ 10 ใช้ Path
    try:
        result = mongo_db.find_one(chicken_farm_id)  # หา id ที่เรากำหนด
    except:
        raise HTTPException(
            status_code=500, detail="Something went wrong !!"
        )  # server error(500)

    if result is None:
        raise HTTPException(
            status_code=404, detail="Chicken farm Id not found !!"
        )  # ถ้าไม่เจอ id ที่กำหนด Userใส่ค่าผิด (404)

    return JSONResponse(
        content={"status": "OK", "data": result},
        status_code=200,
    )


@app.post("/chickenfarms")
def create_house(chicken_farm: createChickenFarmModel):
    try:
        chicken_farm_id = mongo_db.create(chicken_farm)
    except:
        raise HTTPException(status_code=500, detail="Something went wrong !!")

    return JSONResponse(
        content={
            "status": "ok",
            "data": {
                "chicken_farm_id": chicken_farm_id,
            },
        },
        status_code=201,  # createใช้ 201 serchใช้ 200
    )


@app.patch(
    "/chickenfarms/{chicken_farm_id}"
)  # path จะ update ค่าบางตัว (put จะเปลี่ยนค่าทั้ง collection)
def update_house(
    update_chicken_farm: updateChickenFarmModel,
    chicken_farm_id: str = Path(
        None, min_length=10, max_length=10
    ),  # ให้ใส่ค่าเท่ากับ 10 ถ้าไม่เท่าจะ error
):
    try:
        updated_chicken_farm_id, modified_count = mongo_db.update(
            chicken_farm_id, update_chicken_farm
        )
    except:
        raise HTTPException(status_code=500, detail="Something went wrong !!")

    if modified_count == 0:  # ค่าเป็น 0 fild(ค่าที่ใส่) ผิด
        raise HTTPException(
            status_code=404,
            detail=f"Chicken farm ID: {updated_chicken_farm_id} is not update want fields",
        )

    return JSONResponse(
        content={
            "status": "ok",
            "data": {
                "chicken_farm_id": updated_chicken_farm_id,
                "modified_count": modified_count,
            },
        },
        status_code=201,
    )


@app.delete("/chickenfarms/{chicken_farm_id}")
def delete_house_by_id(chicken_farm_id: str = Path(None, min_length=10, max_length=10)):
    try:
        deleted_chicken_farm_id, deleted_count = mongo_db.delete(
            chicken_farm_id
        )  # เรียกใช้ mongo medthod delets
    except:
        raise HTTPException(status_code=500, detail="Something went wrong !!")

    if deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail=f"Chicken farm ID: {deleted_chicken_farm_id} is not Delete",  # บอกว่าลบไม่ได้
        )

    return JSONResponse(
        content={
            "status": "ok",
            "data": {
                "chicken_farm_id": deleted_chicken_farm_id,
                "deleted_count": deleted_count,
            },
        },
        status_code=200,
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=3001, reload=True)
