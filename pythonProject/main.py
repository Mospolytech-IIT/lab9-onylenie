from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from models import Base, User, Post
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

Base.metadata.create_all(bind=engine)
app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Главная страница
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request, db: Session = Depends(get_db)):
    users = db.query(User).all()
    posts = db.query(Post).all()
    return templates.TemplateResponse("index.html", {"request": request, "users": users, "posts": posts})


# Создание нового пользователя
@app.post("/users/create", response_class=RedirectResponse)
def create_user(username: str = Form(...), email: str = Form(...), db: Session = Depends(get_db)):
    user = User(username=username, email=email,password="passwsord")
    db.add(user)
    db.commit()
    return RedirectResponse("/", status_code=302)


# Удаление пользователя
@app.post("/users/delete/{user_id}", response_class=RedirectResponse)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return RedirectResponse("/", status_code=302)


# Создание нового поста
@app.post("/posts/create", response_class=RedirectResponse)
def create_post(title: str = Form(...), content: str = Form(...), user_id: int = Form(...),
                db: Session = Depends(get_db)):
    post = Post(title=title, content=content, user_id=user_id)
    db.add(post)
    db.commit()
    return RedirectResponse("/", status_code=302)


# Удаление поста
@app.post("/posts/delete/{post_id}", response_class=RedirectResponse)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
    return RedirectResponse("/", status_code=302)


@app.post("/users/update/{user_id}")
def update_user(user_id: int, username: str = Form(None), email: str = Form(None), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if username:
        user.username = username
    if email:
        user.email = email

    db.commit()
    db.refresh(user)
    return RedirectResponse("/", status_code=302)


@app.post("/posts/update/{post_id}")
def update_post(post_id: int, title: str = Form(None), content: str = Form(None), db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if title:
        post.title = title
    if content:
        post.content = content

    db.commit()
    db.refresh(post)
    return RedirectResponse("/", status_code=302)
