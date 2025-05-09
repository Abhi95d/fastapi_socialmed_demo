from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. database import get_db
from .. import models, schemas, utils, oauth2
from typing import Optional, List
from sqlalchemy import func

router = APIRouter(prefix= "/posts",
                   tags=['Posts'])




@router.get("/", response_model = List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
              limit: int = 10, skip: int = 10, search: Optional[str] = ""):
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all() #Use this if you want to design ur app such a way that only posts of current user is to be shown.
    # cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall()
    # return posts
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote,models.Vote.post_id == models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts

@router.post("/",status_code= status.HTTP_201_CREATED, response_model = schemas.Post)
def create_posts(post:schemas.PostCreate, db: Session = Depends(get_db),
                  current_user: int = Depends(oauth2.get_current_user)):
    # return{"data" : posts}):
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) RETURNING * """,(post.title,post.content,post.published))
    # new_posts = cursor.fetchone()
    # conn.commit()
    # return {"data": new_posts}
    print(current_user)
    new_post = models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post



@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id : int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s  """, (id,))
    # test_posts = cursor.fetchone()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()


    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return  {'message' : f'message with id: {id} was not found'}
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                             detail= f'message with id: {id} was not found')
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                          detail =  "Not authorized to perform requested action")

    return post


@router.delete("/{id}", status_code=status.HTTP_404_NOT_FOUND)
def delete_post(id:int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    # cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (id,))
    # deleted_posts = cursor.fetchone()
    # conn.commit()

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")
    
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #      detail =  "Not authorized to perform requested action")
    
    post_query.delete(synchronize_session = False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{id}", response_model = schemas.Post)
def update_post(id:int, updated_post:schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *",
    #                 (post.title, post.content, post.published, str(id)))
    # updated_posts = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()
    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {id} not found")
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                          detail =  "Not authorized to perform requested action") 
    
    
    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return  post_query.first()



        
