from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
from pydantic import BaseModel

app = FastAPI()

middleware = {
    'allow_origins': ['*'],
    'allow_credentials': True,
    'allow_methods': ['*'],
    'allow_headers': ['*'],
}

app.add_middleware(CORSMiddleware, **middleware)



class Duration(BaseModel):
    zweck: str
    start: str
    end: str
    priority: int


class Object(BaseModel):
    object: str
    duration: List[Duration]


class Priority(BaseModel):
    value: int
    prio: str
    color: str


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/Objects")
async def get_objects():
    with open('./Objects.json', 'r') as f:
        data = json.load(f)

    return data


@app.post("/Object/new")
async def create_object(new_object: Object):
    with open('./Objects.json', 'r') as f:
        data = json.load(f)

    data['objects'].append(new_object.dict())
    with open('./Objects.json', 'w') as f:
        json.dump(data, f)

    return data


@app.get("/Priorities")
async def get_priorities():
    with open('./Priority.json', 'r') as f:
        data = json.load(f)

    return data


@app.post("/Priority/new")
async def create_priority(new_priority: Priority):
    with open('./Priority.json', 'r') as f:
        data = json.load(f)

    data['priorities'].append(new_priority.dict())
    with open('./Priority.json', 'w') as f:
        json.dump(data, f)

    return data


@app.post("/Duration/new/{booking_object}")
async def create_duration(booking_object: str, new_duration: Duration):
    with open('./Objects.json', 'r') as f:
        data = json.load(f)
        for DataObject in data["objects"]:
            print(DataObject)
            if DataObject["object"] == booking_object:
                DataObject["duration"].append(new_duration.dict())
    with open('./Objects.json', 'w') as f:
        json.dump(data, f)

    return data
