from random import randrange
from typing import Optional
from fastapi import FastAPI,Response,status,HTTPException,Depends
from fastapi.params import Body
import psycopg2 
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models,schemas,utils
from .database import engine,get_db
from .routers import post,user,auth


models.Base.metadata.create_all(engine)

app=FastAPI()


while True:
    try:
        conn=psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='Chinmay@123',
        cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print("Database connection successfully")
        break

    except Exception as error:
        print("Database conenction failed")
        print("error:", error)
        time.sleep(2)
    
my_posts=[{"title":"title of post 1","content":"content of post 1","id":1},
          {"title":"favourite food","content":"i like pizza","id":2}]   

def find_post(id):
    for p in my_posts:
        if p['id']==id:
            return p
         
 
def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id']==id:
            return i
        
app.include_router(post.router)
app.include_router(user.router)  
app.include_router(auth.router)   


@app.get("/")
def read_root():
    return {"Hello": "Welcome to my the world of Chinmay Chatterjee"}

 
    


    