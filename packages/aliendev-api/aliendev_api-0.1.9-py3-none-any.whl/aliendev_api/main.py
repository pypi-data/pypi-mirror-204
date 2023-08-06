from bson.objectid import ObjectId
from aliendev_api.config import mongo
from pydantic import BaseModel, Field
from enum import Enum
import os, json

def _case(param: str):
    splitter = param.lower().replace(" ", "-")
    return splitter


method_name = ["GET", "POST", "PUT", "DELETE"]

class ParamType(Enum):
    param = 'Param'
    body = 'Body'

class ParamData(BaseModel):
    key: str = Field(..., example="name")
    data_type: str = Field(..., example="string|int|any")
    required: bool


class ApiGateway:
    def __init__(self, title) -> None:
        self.username = ""
        self.account_id= ""
        self.title = title
        self.stack_name = _case(title)
        self.endpoint = []
        print("Deploying API Gateway 🤩")
        home_folder = os.path.expanduser("~")
        path = f'{home_folder}/.aliendev'
        if not os.path.exists(path+"/config.json"):
            print("Please Login first 😊")
        else:
            with open(path+"/config.json", "r") as file:
                json_file = json.load(file)
                self.username = json_file.get("username")
                self.account_id = json_file.get("_id")

    def addMethod(self, method, prefix, param_type:ParamType, data:ParamData):
        """
        Args:
            method (string): "GET|POST|PUT|DELETE"
            prefix (string): "/test-get"
            param_type (ParamType): "param|body"
            data (ParamData): [
                        {
                        "key": "name",
                        "data_type": "string",
                        "required": true
                        },
                        {
                        "key": "age",
                        "data_type": "int",
                        "required": false
                        }
                    ]
        """
        if method in method_name:
            endpoint = {
                "method": method,
                "prefix": prefix,
                "param_type":param_type,
                "data":data
            }
            self.endpoint.append(endpoint)

    def build(self):
        objId = ObjectId()
        result_data = {
            "_id": str(objId),
            "account_id":self.account_id,
            "username": self.username,
            "title": self.title,
            "stack_name": self.stack_name,
            "endpoint": self.endpoint
        }
        client, db = mongo.connect()
        with client:
            finder = db['gateway'].find_one(
                {"$and": [{"username": self.username}, {"stack_name": self.stack_name}]})
            if finder:
                newvalues = {"$set": {"endpoint": self.endpoint}}
                db['gateway'].update_one({"_id": finder['_id']}, newvalues)
            else:
                db['gateway'].insert_one(result_data)
        print("API Gateway has deployed 🎉")
        return result_data
