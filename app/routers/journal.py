from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from ..db.database import get_db
from typing import List, Optional
from ..models import models,schema
from ..utils import oauth2


router = APIRouter(prefix='/journals', tags=['Journals'])


@router.get('/', response_model=List[schema.Journal])
def get_journal(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, offset: int = 0, search: Optional[str] = "" ):
    posts = db.query(models.Journals).filter(models.Journals.title.contains(search)).limit(limit).offset(offset).all()
    return posts

@router.post('/',status_code=status.HTTP_201_CREATED, response_model=schema.Journal)
def create_journal(journal: schema.JournalCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    print(current_user)
    new_journal = models.Journals(owner_id=current_user.id ,**journal.model_dump())
    db.add(new_journal)
    db.commit()
    db.refresh(new_journal)
    return new_journal

@router.get('/{id}', response_model=schema.Journal)
def get_journal(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    journal = db.query(models.Journals).filter(models.Journals.id==id).first()
    if not journal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} was not found")
    if journal.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")

    return journal

@router.put('/{id}', status_code=status.HTTP_201_CREATED, response_model=schema.Journal)
def update_post(id: int, update_journal : schema.JournalCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    journal_query = db.query(models.Journals).filter(models.Journals.id==id)
    journal = journal_query.first()
    if not journal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Journal with {id} does not exist")
    if journal.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    journal_query.update(update_journal.model_dump(), synchronize_session=False)
    db.commit()
    return journal_query.first()

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_journal(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    journal_query = db.query(models.Journals).filter(models.Journals.id == id)
    journal = journal_query.first()
    if journal == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Journal with {id} does not exist")
    if journal.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    journal_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)