from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import schemas, database, models, oauth2
from sqlalchemy.orm import Session


router = APIRouter(prefix = "/vote", tags=['Vote'])


# Add or remove a vote made by a user to a particular post
@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    # Store the post that the user wants to vote on
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    # If post does not exist, throw HTTP 404
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Post with id {vote.post_id} does not exist")

    # Searches if the user has already liked the post
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)

    # Stores the posts
    found_vote = vote_query.first()
    
    # If user wants to vote on a post
    if (vote.direction == 1):

        # If post exist, then user has already voted on it
        if found_vote:
            raise HTTPException(status_code = status.HTTP_409_CONFLICT, 
                                detail=f"User {current_user.id} has already voted on post {vote.post_id}")
        
        # Adds the user's vote
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()

        return {"Message" : "Successfully added vote."}
    
    # If user wants to delete their vote
    else:

        # If user has not voted on the post
        if not found_vote:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Vote does not exist.")

        # If user has voted on the post, delete it
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"Message" : "Successfully deleted vote."}
         