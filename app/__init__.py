from flask import Flask

app=Flask(__name__)

USERS = [] #list for users
EXPRS = [] #list for obj of type expressions
QUEST = [] #list of questions
from app import views_all
from app import models
from app import views