from typing import List, Optional
from unittest import result
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter

from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0,
                search: Optional[str] = ""): # in query parameter ?limit=20
    #cursor.execute(""" SELECT * FROM posts """)
    #posts = cursor.fetchall()
    #print(posts)
    #print(limit)
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()
    #print(results)

    #return {"data": posts}
    #return posts
    return results

# @router.post("/createposts")
# def create_posts_without_pydantic(payload: dict = Body(...)):
#     print(payload)
#     return {"new_post": f"title: {payload['title']}; content: {payload['content']}."}

# # pydantic can be used with fastAPI to define a schema (a contract)
# # this helps to define a model that tells what data do we expect to receive
# # e.g. title to be string, content to be strong, publishedPost as boolean etc...

""" @router.post("/posts_old", status_code=status.HTTP_201_CREATED)
def create_posts_test_function(post: schemas.PostCreate): # Here, since we defined the model in pydattic, title and content are extracted and str type checked
    post_dict = post.dict()
    post_dict['id'] = random.randrange(0, 10000000000)
    my_posts.append(post_dict)
    return {"data": post_dict} """

# more recent
@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): # Here, since we defined the model in pydattic, title and content are extracted and str type checked
    # Using the %s for string, it sanitizes the input to avoid SQL injection attacks
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    # new method
    #print(post.dict())
    #print(**post.dict())
    print("user_id:", current_user.id)
    new_post = models.Post(owner_id=current_user.id, **post.dict()) #(title=post.title, content=post.content, published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # acts like RETURNING * 

    #return {"data": new_post} # this return causes an error 501 when response model is used. Removing "data" and returning only post fixes it.
    return new_post

# CRUD: CREATE (/posts), READ (GET, /posts/id), UPDATE (PUT, PATCH), DELETE (posts/id)
# plural is standard convension in CRUD

def get_post_by_id(id):
    for p in my_posts:
        if p["id"] == id:
            return p

get_by_id = lambda x: [p for p in my_posts if p["id"] == int(x)]

""" @router.get("/posts_old/{id}")
def get_posts_old(id: int, response: Response):
    post = get_post_by_id(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id '{id}' was not found")
        #response.status_code = status.HTTP_404_NOT_FOUND #404
    return {"post_detail": post} """

@router.get("/{id}", response_model=schemas.Post)
def get_posts(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    #cursor.execute(""" SELECT * FROM posts WHERE id = %s """, str(id)) # (str(id), )
    # post = cursor.fetchone()

    # using sqlalchemy
    post = db.query(models.Post).filter(models.Post.id == id).first()
    # print(post)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id '{id}' was not found")
        #response.status_code = status.HTTP_404_NOT_FOUND #404
    #return {"post_detail": post}    
    return post

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

""" 
@router.delete("/posts_old/{id}")
def delete_post_old(id: int):
    # deleting post
    # find index in array with the required ID
    # mypost.pop(index)
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id '{id}' does not exist")
    my_posts.pop(index)

    # return {"message": f"Post with the id '{id}' successfully deleted"}
    return Response(status_code=status.HTTP_204_NO_CONTENT) # to remove the error of content length as we returned a msg  """


@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", (str(id), ))
    #deleted_post = cursor.fetchone()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id '{id}' does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to performed requested action")

    post_query.delete(synchronize_session=False)
    db.commit()
    
    #conn.commit()

    # return {"message": f"Post with the id '{id}' successfully deleted"}
    return Response(status_code=status.HTTP_204_NO_CONTENT) # to remove the error of content length as we returned a msg 


""" # with PUT method, we must put all fields, even if only one needs to be updated
@router.put("/posts_old/{id}")
def update_post_old(id: int, post: schemas.PostUpdate): # the Post ensures the request comes with the right schema, 
    #we could have another class for Update but not necessary as fields are same as Post
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id '{id}' does not exist")
    
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict

    return {"data": post_dict}  """


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostUpdate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): 
    #cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    #update_post = cursor.fetchone()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id '{id}' does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to performed requested action")
    
    #conn.commit()

    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    #return {"data": post_query.first()} 
    return post_query.first()