from .. import models, schemas, oauth2
from fastapi import  Depends, APIRouter, status , HTTPException
from sqlalchemy.orm import Session
from ..database import get_db



router = APIRouter(
    prefix="/comment" , tags=["Comments"]
    )


@router.post("/{id}", response_model=schemas.CommentOut, status_code=status.HTTP_201_CREATED)
def create_comment(id : int, 
                   comment: schemas.CommentCreate, 
                   db: Session = Depends(get_db), 
                   current_user: int = Depends(oauth2.get_current_user)):
    
    if not db.query(models.Post).filter(models.Post.id == id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    new_comment = models.Comment(post_id=id, **comment.model_dump(), owner_id=current_user.id)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


@router.delete("/{id_post}/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(id: int, 
                   id_post: int,
                   db: Session = Depends(get_db),
                   current_user: int = Depends(oauth2.get_current_user)):
    
    comment_query = db.query(models.Comment).filter(
        models.Comment.id == id,
        models.Comment.post_id == id_post  # Użycie id_post do weryfikacji
    )
    
    comment = comment_query.first()
    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"comment with id: {id} does not exist")
    
    if comment.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    comment_query.delete(synchronize_session=False)
    db.commit()
    
    