from .. import models,schemas
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from ..database import get_db

router=APIRouter(prefix="/posts",tags=['Post'])

my_posts=[{"title":"title of post 1","content":"content of post 1","id":1},
          {"title":"favourite food","content":"i like pizza","id":2}] 


@router.get("/",response_model=list[schemas.Post])
def get_posts(db:Session=Depends(get_db)):
    #cursor.execute("""SELECT * FROM posts""")
    #posts=cursor.fetchall()
    posts=db.query(models.Post).all()
    return posts
    
    

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_post(post:schemas.PostCreate,db:Session=Depends(get_db)):
   #cursor.execute("""INSERT INTO posts(title,content,published) VALUES(%s,%s,%s) RETURNING * """,
                #(post.title,post.content,post.published))
   #new_post=cursor.fetchone()
   #conn.commit()
   #print(new_post)
   
   new_post=models.Post(**post.dict())
   db.add(new_post)
   db.commit()
   db.refresh(new_post)
   return new_post


@router.get("/{id}",response_model=schemas.Post)
def get_post(id:int,db:Session=Depends(get_db)):
    #cursor.execute("""SELECT * FROM posts WHERE id= %s""",str(id))
    #test_post=cursor.fetchone()
    #print(test_post)
    post=db.query(models.Post).filter(models.Post.id==id).first()
    print(post)
   
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Error 404 Not Found")
    return post


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session=Depends(get_db)):
    #cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING * """,str(id))
    #deleted_post=cursor.fetchone()
    #conn.commit()
    post=db.query(models.Post).filter(models.Post.id==id).first()
    print(post)
    
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The post with id:{id} do not found")
    
    db.delete(post)
    db.commit()

@router.put("/{id}",response_model=schemas.Post)
def update_post(id:int,post:schemas.PostCreate,db:Session=Depends(get_db)):
   
   #cursor.execute("""UPDATE posts SET title=%s,content=%s,published=%s WHERE id=%s RETURNING *""",
   #(chinmay.title,chinmay.content,chinmay.published,str(id)))
   #updated_post=cursor.fetchone()
   #print(updated_post)
   #conn.commit()
   updated_post=db.query(models.Post).filter(models.Post.id==id)
   
   if updated_post.first()==None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                           detail="the passed id number doesn't exist")
       
   updated_post.update({"title":"lionel messi","content":"football player"},synchronize_session=False)
   db.commit()    
   
   return updated_post.first()