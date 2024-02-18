from pymongo import MongoClient

from scripts.logging.log_module import logger as log

class MongoUtility():
    
    def __init__(self, mongo_host: str, mongo_port: str) -> None:
        try:
            self.mongo_connection = MongoClient(f"mongodb://{mongo_host}:{mongo_port}/")
        except Exception as e:
            log.error(str(e))


    def check_table_existence(self, db_name: str, collection_name: str) -> bool:
        try:
            collection_list = self.mongo_connection[db_name].list_collection_names()
            if collection_name in collection_list:
                return True
            return False
        except Exception as e:
            log.error(str(e))
            return False

    
    def fetch_all(self, db_name: str, collection_name: str) -> list:
        final_data = list()
        try:
            collection = self.mongo_connection[db_name][collection_name]
            data = collection.find()
            final_data = list(data)
        except Exception as e:
            log.error(str(e))
        return final_data
    

    def fetch_using_query(
        self, 
        db_name: str,
        collection_name: str,
        query: dict,
        limit = None,
        sort: str = None,
        sort_order: int = -1
    ) -> list: 
        
        final_list = list()
        try:
            collection = self.mongo_connection[db_name][collection_name]
            if sort:
                if limit:
                    data = collection.find(query).sort(sort, sort_order).limit(limit)
                else:
                    data = collection.find(query).sort(sort, sort_order)
            else:
                if limit:
                    data = collection.find(query).limit(limit)
                else:
                    data = collection.find(query)
            final_list = list(data)
        except Exception as e:
            log.error(str(e))
        return final_list


    def insert(
        self,
        db_name: str,
        collection_name: str,
        insert_dict: dict,
    ) -> bool:
        try:
            status = self.mongo_connection[db_name][collection_name]
            if status:
                return True
            else:
                return False
        except Exception as e:
            log.error("Error while inserting data: " + str(e))
            return False
    

    def bulk_insert(
        self,
        db_name: str,
        collection_name: str,
        dict_list: str = []
    ) -> bool:
        try:
            status = self.mongo_connection[db_name][collection_name].insert_many(dict_list)
            if status:
                return True
            else:
                return False
        except Exception as e:
            log.error("Error while bulk insert: " + str(e))
            return False
    

    def update_one(
        self,
        db_name: str,
        collection_name: str,
        update_query: dict,
        update_dict: dict
    ) -> bool:
        try:
            status = self.mongo_connection[db_name][collection_name].update_one(
                update_query,
                {"$set": update_dict}
            )
            if status:
                return True
            else:
                return False
        except Exception as e:
            log.error(str(e))
            return False
        
    
    def count(
        self, 
        db_name: str,
        collection_name: str,
        count_query: dict
    ) -> int:
        try:
            count = self.mongo_connection[db_name][collection_name].count_documents(count_query)
            return count
        except Exception as e:
            log.error(str(e))
            return 0
        

    def delete_collection(
        self,
        db_name: str,
        collection_name: str
    ):
        try:
            self.mongo_connection[db_name][collection_name].drop()
        except Exception as e:
            log.error(str(e))
        