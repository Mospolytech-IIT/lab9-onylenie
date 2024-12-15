from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

DATABASE_URL = "postgresql://postgres:admin@localhost/test"
engine = create_engine(DATABASE_URL, echo=True)

Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)

    posts = relationship('Post', back_populates='user', cascade="all, delete")

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship('User', back_populates='posts')

    def __repr__(self):
        return f"<Post(title='{self.title}', user_id={self.user_id})>"


# Напишите программу, которая добавляет в таблицу Users несколько записей
# с разными значениями полей username, email и password.
def add_users():
    users = [
        User(username="user1", email="mail1@mail.ru", password="password1"),
        User(username="user2", email="mail2@mail.ru", password="password2"),
        User(username="user3", email="mail3@mail.ru", password="password3"),
    ]
    session.add_all(users)
    session.commit()
    print("Пользователи добавлены!")


# Напишите программу, которая добавляет в таблицу Posts несколько записей,
# связанных с пользователями из таблицы Users.
def add_posts():
    posts = [
        Post(title="Пост 1", content="Текст первого поста 1", user_id=1),
        Post(title="Пост 2", content="Текст второго поста 2", user_id=2),
        Post(title="Пост 3", content="Текст третьего поста 3", user_id=1),
    ]
    session.add_all(posts)
    session.commit()
    print("Посты добавлены!")


# Напишите программу, которая извлекает все записи из таблицы Users.
def get_all_users():
    users = session.query(User).all()
    for user in users:
        print(user)


# Напишите программу, которая извлекает все записи из таблицы Posts,
# включая информацию о пользователях, которые их создали.
def get_all_posts_with_users():
    posts = session.query(Post).all()
    for post in posts:
        user = session.query(User).filter(User.id == post.user_id).first()
        print(f"{post} написан пользователем {user.username}")


# Напишите программу, которая извлекает записи из таблицы Posts,
# созданные конкретным пользователем.
def get_posts_by_user(username):
    user = session.query(User).filter(User.username == username).first()
    if user:
        posts = session.query(Post).filter(Post.user_id == user.id).all()
        for post in posts:
            print(post)
    else:
        print(f"Пользователь {username} не найден.")


# Напишите программу, которая обновляет поле email у одного из пользователей.
def update_user_email(user_id, new_email):
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        user.email = new_email
        session.commit()
        print(f"Email пользователя {user.username} обновлен на {new_email}")
    else:
        print("Пользователь не найден.")


# Напишите программу, которая обновляет поле content у одного из постов.
def update_post_content(post_id, new_content):
    post = session.query(Post).filter(Post.id == post_id).first()
    if post:
        post.content = new_content
        session.commit()
        print(f"Содержимое поста '{post.title}' обновлено!")
    else:
        print("Пост не найден.")


# Напишите программу, которая удаляет один из постов.
def delete_post(post_id):
    post = session.query(Post).filter(Post.id == post_id).first()
    if post:
        session.delete(post)
        session.commit()
        print(f"Пост '{post.title}' удален!")
    else:
        print("Пост не найден.")


# Напишите программу, которая удаляет пользователя и все его посты.
def delete_user_with_posts(user_id):
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        session.delete(user)
        session.commit()
        print(f"Пользователь '{user.username}' и все его посты удалены!")
    else:
        print("Пользователь не найден.")


if __name__ == "__main__":
    add_users()
    add_posts()

    print("\nВсе пользователи:")
    get_all_users()

    print("\nВсе посты с информацией о пользователях:")
    get_all_posts_with_users()

    print("\nПосты пользователя user1:")
    get_posts_by_user("user1")

    print("\nОбновление email пользователя:")
    update_user_email(1, "new_user1@mail.com")

    print("\nОбновление содержимого поста:")
    update_post_content(1, "Обновленный текст первого поста")

    print("\nУдаление поста:")
    delete_post(1)

    print("\nУдаление пользователя и его постов:")
    delete_user_with_posts(2)
