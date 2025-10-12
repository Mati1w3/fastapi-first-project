from .database import Base 
from sqlalchemy import TIMESTAMP, Column, Integer, String, Boolean, text, ForeignKey, func
from sqlalchemy.orm import relationship

class Post(Base):
    
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="True", nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), 
        nullable=False, server_default=func.now())
    
    owner_id = Column(Integer, ForeignKey("users.id", 
                                          ondelete="CASCADE"), 
                                          nullable=False)
    
    owner = relationship("User")
    comments = relationship("Comment", cascade="all, delete-orphan") 
class User(Base):
    
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), 
        nullable=False, server_default=func.now())
    
class Vote(Base):
    
    __tablename__ = "votes"

    post_id = Column(Integer, ForeignKey("posts.id", 
                                         ondelete="CASCADE"), 
                                         primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", 
                                         ondelete="CASCADE"), 
                                         primary_key=True)
    
class Comment(Base):
    
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, nullable=False)
    content = Column(String, nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id", 
                                         ondelete="CASCADE"), 
                                         nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", 
                                          ondelete="CASCADE"), 
                                          nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), 
        nullable=False, server_default=func.now())