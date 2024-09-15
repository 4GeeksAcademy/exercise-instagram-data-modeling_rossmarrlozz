import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import relationship, declarative_base
from eralchemy2 import render_er

Base = declarative_base()

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    firstname = Column(String)
    lastname = Column(String)
    email = Column(String, nullable=False)

    posts = relationship('Post', back_populates='user')
    comments = relationship('Comment', back_populates='author')

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email,
            'posts': [post.to_dict() for post in self.posts],
            'comments': [comment.to_dict() for comment in self.comments]
        }

class Follower(Base):
    __tablename__ = 'follower'
    user_from_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    user_to_id = Column(Integer, ForeignKey('user.id'), primary_key=True)

    user_from = relationship('User', foreign_keys=[user_from_id])
    user_to = relationship('User', foreign_keys=[user_to_id])

    def to_dict(self):
        return {
            'user_from_id': self.user_from_id,
            'user_to_id': self.user_to_id
        }

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    user = relationship('User', back_populates='posts')
    comments = relationship('Comment', back_populates='post')
    media = relationship('Media', back_populates='post')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'comments': [comment.to_dict() for comment in self.comments],
            'media': [m.to_dict() for m in self.media]
        }

class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    comment_text = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)

    author = relationship('User', back_populates='comments')
    post = relationship('Post', back_populates='comments')

    def to_dict(self):
        return {
            'id': self.id,
            'comment_text': self.comment_text,
            'author_id': self.author_id,
            'post_id': self.post_id
        }

class Media(Base):
    __tablename__ = 'media'
    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    url = Column(String, nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)

    post = relationship('Post', back_populates='media')

    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'url': self.url,
            'post_id': self.post_id
        }

## Draw from SQLAlchemy base

try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
