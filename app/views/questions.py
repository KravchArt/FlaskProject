from app import app,USERS,QUEST, models
from flask import request, Response, url_for
import json
from http import HTTPStatus
import random

@app.post('/questions/create')
def create_question():
    data = request.get_json()
    title = data['title']
    description = data['description']
    question_type = data['type']
    question_id = len(QUEST)
    if question_type == 'ONE-ANSWER':
        answer = data['answer'] #exp string
        if not models.One_answer.is_valid1(answer):
            return Response(status=HTTPStatus.BAD_REQUEST)
        question = models.One_answer(question_id, title, description, answer, reward=1)
    elif question_type =='MULTIPLE-CHOICE':
        choices = data['choices'] #list
        answer = data ['answer'] #exp number
        if  not models.MultipleChoice.is_valid2(answer, choices):
            return Response(status=HTTPStatus.BAD_REQUEST)
        question = models.MultipleChoice(question_id, title, description, answer, choices, reward=1)
    else:
        return Response("Question must be ONE-ANSWER or MULTIPLE-CHOICE", status=HTTPStatus.BAD_REQUEST)
    QUEST.append(question)
    return Response(
        json.dumps(
            {
                "id": question_id,
                "title": question.title,
                "description": question.description,
                "type": question_type,
                "answer": question.answer

            }

        ),
        status= HTTPStatus.CREATED,
        mimetype="application/json"

    )

@app.get("/questions/random")
def get_random_question():
    if len(QUEST) == 0:
        return Response(f"""No questions in database, <a href="{url_for("create_question")}"> please add some </a>""", status=HTTPStatus.NOT_FOUND )
    question_id = random.randint(0, len(QUEST)-1)
    question = QUEST[question_id]
    return Response(
        json.dumps(
            {
                "id": question_id,
                "reward": question.reward

            }

        ),
        status = HTTPStatus.OK,
        mimetype="application/json"

    )

@app.post("/questions/<int:question_id>/solve")
def solve_question(question_id):
    data = request.get_json()
    user_id = data['user_id']
    user_answer = data['user_answer']
    if not models.User.is_valid_id(user_id):
        return Response(status=HTTPStatus.NOT_FOUND)
    if not models.Question.is_valid_id(question_id):
        return Response(status=HTTPStatus.NOT_FOUND)
    question = QUEST[question_id]
    user = USERS[user_id]
    if isinstance(question, models.MultipleChoice):
        if not isinstance(user_answer, int):
            return Response("Answer must be int", status = HTTPStatus.BAD_REQUEST)
    if isinstance(question, models.One_answer):
        if not isinstance(user_answer, str):
            return Response("Answer must be str", status = HTTPStatus.BAD_REQUEST)
    if user_answer == question.answer:
        user.increase_score(question.reward)
        result = 'correct'
        reward = question.reward
    else:
        result = 'wrong'
        reward = 0
    user.solve(question,user_answer)
    return Response(json.dumps(
        {
            "question_id": question_id,
            "result": result,
            "reward": reward
        }
        ),  status = HTTPStatus.OK,
            mimetype = "application/json")