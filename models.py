import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.elements import collate


database_path = "postgresql://postgres:(password)@localhost:5432/hoa"

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    db.app = app
    db.init_app(app)
    db.create_all()

class Resident(db.Model):
    __tablename__ = 'resident'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    hoa_group = Column(String)
    

class BoardInfo(db.Model):
    __tablename__ = 'board'

    id = Column(Integer, primary_key=True)   
    name = Column(String)
    board_code = Column(String)
    public_code = Column(String)
    board_memeber = db.relationship('BoardMember', backref='board_member', lazy=True)
    expense_list_id = db.relationship('ExpensesItem', backref='expense', lazy=True)

class BoardMember(db.Model):
    __tablename__  = 'board_member'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    board_group_id = Column(db.ForeignKey('board.id'))

class ExpensesItem(db.Model):
    __tablename__ = 'expenses'

    id = Column(Integer, primary_key=True)
    expense_list_id = Column(db.ForeignKey('board.id'))
    expense_item = Column(String)
    expense_amount = Column(Integer)

class HoaUpdates(db.Model):
    __tablename__ = 'updates'

    hoa_update_id = Column(Integer, primary_key=True)
    hoa_group = Column(Integer)
    subject = Column(String)
    message = Column(String)

