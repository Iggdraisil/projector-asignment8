import csv
import itertools
import os
import random
import secrets
from functools import cache

from cache import AsyncLRU
from fastapi import FastAPI, Depends
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorDatabase,
    AsyncIOMotorCollection,
)

app = FastAPI()

DOCS_NUM = 100000


def chunked_iterable(iterable, size):
    it = iter(iterable)
    while True:
        chunk = tuple(itertools.islice(it, size))
        if not chunk:
            break
        yield chunk


@AsyncLRU(maxsize=1)
async def mongo_db() -> AsyncIOMotorDatabase:
    return AsyncIOMotorClient(
        os.environ.get("MONGODB_HOST", "localhost"),
        int(os.environ.get("MONGODB_PORT", "27017")),
    ).test_database


@cache
def new_cities() -> list[dict]:
    result = []
    with open("cities-new.csv") as cities:
        reader = csv.reader(cities, delimiter=';')
        field_names = next(reader)
        for record in chunked_iterable(reader, 10000):
            result += [dict(zip(field_names, [safe_int(value) for value in item])) for item in record]
    return result


async def mongo_db_dep() -> AsyncIOMotorDatabase:
    return await mongo_db()


def safe_int(value: str) -> str | int:
    try:
        return int(value)
    except ValueError:
        return value


@app.on_event('startup')
async def load_mongo():
    db = await mongo_db()
    collection: AsyncIOMotorCollection = db.foo_collection
    await collection.drop()
    with open("cities.csv") as cities:
        reader = csv.reader(cities, delimiter=';')
        field_names = next(reader)
        for record in chunked_iterable(reader, 10000):
            await collection.insert_many(
                [dict(zip(field_names, [safe_int(value) for value in item])) for item in record])


@app.get("/test")
async def say_hello(
        population: int,
        mongo: AsyncIOMotorDatabase = Depends(mongo_db_dep, use_cache=True),
):
    result = await touch_mongo(mongo, population)
    return result


async def touch_mongo(mongo, population):
    collection: AsyncIOMotorCollection = mongo.foo_collection
    result = await collection.aggregate([
        {
            "$match": {
                "Population": {
                    "$gt": population * 0.9,
                    "$lt": population * 1.1,
                }
            },
        },
        {
            "$group": {
                "_id": {"Country Code": "$Country Code"},
                "totalPopulation": {"$sum": "$Population"},
                "averageHeight": {"$avg": "$DIgital Elevation Model"}
            }
        }
    ]).to_list(None)
    new_city = random.choice(new_cities())
    new_city['_id'] = secrets.token_urlsafe(23)
    await collection.insert_one(new_city)
    return result
