from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from .database import Base
from sqlalchemy.orm import relationship

class Post(Base):
     __tablename__ = "posts"

     id = Column(Integer, primary_key = True, nullable = False)
     title = Column(String, nullable = False)
     content = Column(String, nullable = False)
     published = Column(Boolean, server_default = 'TRUE', nullable = False) 
     created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default=text('now()'))
     owner_id = Column(Integer, ForeignKey("user.id", ondelete = "CASCADE"), nullable= False)

     owner = relationship("User")

class User(Base):
     __tablename__ = "user"
     id = Column(Integer, primary_key = True, nullable = False)
     email = Column(String, nullable = False, unique=True)
     password = Column(String, nullable = False, unique=True)
     created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default=text('now()'))

class Vote(Base):
     __tablename__ = "votes"
     user_id = Column(Integer, ForeignKey("user.id", ondelete = "CASCADE"), primary_key=True)
     post_id = Column(Integer, ForeignKey("posts.id", ondelete = "CASCADE"), primary_key=True)












   
# while True:
#     try:
#         conn = psycopg.connect("dbname=fastapi user=postgres password=bullpup195 host=localhost port=5432")
#         cursor = conn.cursor()
#         print("database connection was successfull")
#         break
#     except Exception as error:
#         print("connection to database failed")
#         print("error:", error)
#         time.sleep(2)