import pymongo

from model.chicken_farm import createChickenFarmModel, updateChickenFarmModel


class MongoDB:
    def __init__(self, host, port, user, password, auth_db, db, collection):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.auth_db = auth_db
        self.db = db
        self.collection = collection
        self.connection = None

    def _connect(self):
        client = pymongo.MongoClient(
            host=self.host,
            port=self.port,
            username=self.user,
            password=self.password,
            authSource=self.auth_db,
            authMechanism="SCRAM-SHA-1",
        )
        db = client[self.db]
        self.connection = db[self.collection]

    def find(self, sort_by, order):
        mongo_results = self.connection.find({})  # ค้นหาทั้งหมด
        if sort_by is not None and order is not None:
            mongo_results.sort(sort_by, self._get_sort_by(order))

        return list(mongo_results)

    def _get_sort_by(self, sort: str) -> int:
        return pymongo.DESCENDING if sort == "desc" else pymongo.ASCENDING

    def find_one(self, id):
        return self.connection.find_one({"_id": id})  # เลือก id ที่เจอก่อน

    def create(
        self, chicken_farm: createChickenFarmModel
    ):  # เป็นการ insert ค่าลง mongodb
        chicken_farm_dict = chicken_farm.dict(exclude_unset=True)

        insert_dict = {**chicken_farm_dict, "_id": chicken_farm_dict["id"]}

        inserted_result = self.connection.insert_one(insert_dict)

        chicken_farm_id = str(inserted_result.inserted_id)

        return chicken_farm_id

    def update(self, chicken_farm_id, update_chicken_farm: updateChickenFarmModel):
        updated_result = self.connection.update_one(
            # เที่ยบกับการ update ใน mongo
            {"id": chicken_farm_id},  # query
            {  # update_data
                "$set": chicken_farm.dict(exclude_unset=True)  # แปลงให้เป็น dict
            },
        )
        return [
            chicken_farm_id,
            updated_result.modified_count,
        ]  # modified_count คือ เมื่อเรา update ค่าแล้วมันมีการเปลี่ยนแปลงค่าหรือไม่

    def delete(self, chicken_farm_id):
        deleted_result = self.connection.delete_one({"id": chicken_farm_id})
        return [
            chicken_farm_id,
            deleted_result.deleted_count,
        ]  # เช็คว่ามีการลบจริงหรือไม่ ถ้าใช่เป็น 1 ถ้าไม่เป็น 0
