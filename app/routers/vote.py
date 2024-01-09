from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from ..db.database import get_db
from typing import List, Optional
from ..models import models,schema
from ..utils import oauth2

router = APIRouter(prefix='/vote', tags=['Vote'])

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schema.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    vote_found = vote_query.first()
    if (vote.dir == 1):
        if vote_found:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user with id {current_user.id} has already voted for this journal")
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added the vote."}
    else:
        if not vote_found:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote does not exist.")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully deleted the vote."}



