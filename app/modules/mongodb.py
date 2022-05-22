import re
import resource
import pymongo
from pymongo import MongoClient

cluster = "mongodb+srv://atlas-techno:Atlas132@cluster0.wts6q.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(cluster)

AtlasDB = client["AtlasDB"]

users = AtlasDB["users"]

def create_workspace(id,name,region):
    try:
        schema = {
            "_id":f"{id}",
            "workspaces":[
                {
                    "name":f"{name}",
                    "region":f"{region}",
                    "vpcs":[]
                }
            ]
        }
        user = users.insert_one(schema)
        return user
    except: 
        schema = {
            "$push":
            {
                "workspaces": 
                {
                    "name":f"{name}",
                    "region":f"{region}"
                }
            }
        }
        user = users.find_one_and_update({"_id":f"{id}"},schema)
        return user


def create_vpc(id,workspace,resource_name,cidr_block):
    user = users.find_one_and_update(
            {
            "_id":f"{id}",
            "workspaces.name":f"{workspace}",
            },
            {
                "$push": {
                    "workspaces.$.vpcs":
                        {
                            "resource_name":f"{resource_name}",
                            "cidr_block":f"{cidr_block}",
                            "subnets":[]
                        }
                }
            }
        )
    return user

def create_subnet(id,workspace,resource_name,vpc_name,cidr_block):
    user = users.find_one(
        {
            "_id":f"{id}",
            "workspace.name":f"{workspace}"   
        },
        {
            "$push": 
            {
                "workspaces.$.vpcs.$[vpc].subnets":
                {
                    "resource_name":f"{resource_name}",
                    "cidr_block":f"{cidr_block}"
                }
            }
        },
        {
            "arrayFilters": 
            [
                {
                    "vpc.resource_name":f"{vpc_name}"
                }
            ] 
        }
    )

    print(user)

# workspaces.name='workspace'.subnet='subnet'