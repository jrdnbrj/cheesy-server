# GraphQL
from starlette.graphql import GraphQLApp

# Schema Definition
from src.schema import schema

# FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# .env
from decouple import config

# mongoengine
from mongoengine import connect


app = FastAPI()

app.add_route("/gql", GraphQLApp(schema=schema))

connect(host=config('MONGO_SRV'))

# https://fastapi.tiangolo.com/tutorial/cors/
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
