from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

DATABASE_URL = "postgresql://postgres:admin@localhost/test"

engine = create_engine(DATABASE_URL, echo=True)

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)

    posts = relationship('Post', back_populates='user', cascade="all, delete")

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email})>"


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship('User', back_populates='posts')

    def __repr__(self):
        return f"<Post(title={self.title}, user_id={self.user_id})>"


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("Таблицы созданы!")
