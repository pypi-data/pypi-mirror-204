import pymongo

from robot.api.logger import info
from robot.api.deco import keyword
from robot.api import Error


class ViaMongo():
    ### Return conncection with mongoDB ###
    @keyword(name="Mongo Connect To Database")
    def mongo_connect_to_database(self, strConnction:str):
        try:
            return pymongo.MongoClient(strConnction)
        except Exception as e:
            raise Error(e)

    ### Returns a disconnection with the server ###
    @keyword(name="Mongo Disconnect To Database")
    def mongo_disconnect_to_database(self, client):
        try:
            client.close()
            info("Connection has closed sucess")
        except Exception as e:
            raise Error(e)

    ### Returns one json or list the json result ###
    @keyword(name="Mongo Find All")
    def mongo_find_all(self, client, baseName:str, collectionName:str):
        try:
            lstItems = []

            dataBase = client[baseName]

            collection = dataBase[collectionName]

            result = collection.find()

            for item in result:
                lstItems.append(item)

            return lstItems
        except Exception as e:
            raise Error(e)

    ### Returns one json or list the json result by parameter or list empty with not be result###
    @keyword(name="Mongo Find By Parameter")
    def mongo_find_by_parameter(self, client, baseName:str, collectionName:str, query:dict):
        try:
            lst_result = []

            dataBase = client[baseName]

            collection = dataBase[collectionName]

            result = collection.find(query)

            for item in result:
                lst_result.append(item)
            
            return lst_result
        except Exception as e:
            raise Error(e)
