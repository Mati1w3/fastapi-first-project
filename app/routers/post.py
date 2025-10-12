from app.routers import user
from .. import models, schemas, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session, joinedload, contains_eager
from ..database import get_db
from typing import List, Optional
from sqlalchemy import func, select, literal_column



router = APIRouter(
    prefix="/posts" , tags=["Posts"]
    )

"""
C-create - post - @app.post("/posts") 
R-read - get - @app.get("/posts")
R-read one - get - @app.get("/posts/{id}")
U-update - put/patch - @app.put("/posts/{id}")
D-delete - delete - @app.delete("/posts/{id}")
"""

# ------------------------------------Fucntions--------------------------------------------

#get posts raw sql:
@router.get("/", response_model=list[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), 
              current_user: int = Depends(oauth2.get_current_user), 
              limit: int = 10, 
              skip: int = 0, search: Optional[str] = ""):
              
    #cursor.execute('SELECT * FROM posts')
    #posts = cursor.fetchall()
    # posts = db.query(models.Post).filter(
    #     models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    results = db.query(models.Post, func.count(models.Vote.post_id).label("likes")).options(
        joinedload(models.Post.comments)
    ).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True
    ).group_by(
        models.Post.id
    ).filter(
        models.Post.title.contains(search)
    ).limit(limit).offset(skip).all()
    
   
    return [
        {
            "Post": post_orm_object,
            "likes": likes_count,
            "comments_count": len(post_orm_object.comments),
            "comments": post_orm_object.comments
        } 
        for post_orm_object, likes_count in results
    ]
     
    
    



#get one post
@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, 
             db: Session = Depends(get_db), 
             current_user: int = Depends(oauth2.get_current_user)):
    
    # cursor.execute('SELECT * FROM posts WHERE id = %s', (str(id)))
    # post = cursor.fetchone()
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    results = db.query(models.Post, func.count(models.Vote.post_id).label("likes")).options(
        joinedload(models.Post.comments)
    ).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True
    ).group_by(
        models.Post.id 
    ).filter(
        models.Post.id == id
    ).first()

    
    if results == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    post_orm_object, likes_count = results 
    comments_list = post_orm_object.comments
    comments_count_final = len(comments_list)
    return {
        "Post": post_orm_object,
        "likes": likes_count,
        "comments_count": comments_count_final,
        "comments": post_orm_object.comments
    }
  
#create post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, 
                 db: Session = Depends(get_db), 
                 current_user: int = Depends(oauth2.get_current_user)
                 ):
    
    #cursor.execute('INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *', (post.title, post.content, post.published))
    #new_post = cursor.fetchone()
    #conn.commit()

    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

#update post
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, 
                post: schemas.PostCreate, 
                db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)):
    
    # cursor.execute('UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *', (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()


    updated_post = db.query(models.Post).filter(models.Post.id == id)

    
    if updated_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")
    
    updated_post.update(post.model_dump(), synchronize_session=False)

    db.commit()

    return updated_post.first()


#delete post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, 
                db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)):
    
    # cursor.execute('DELETE FROM posts WHERE id = %s RETURNING *', (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()
    

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()
# ------------------------------------Fucntions_end--------------------------------------------