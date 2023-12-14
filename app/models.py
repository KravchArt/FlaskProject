import re
from app import USERS, EXPRS, QUEST
from abc import ABC, abstractmethod


class User:
    def __init__(self, id, first_name, last_name, phone, email, score=0):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        self.score = score
        self.history = []

    @staticmethod
    def is_valid_email(email):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        return (re.fullmatch(regex, email))

    @staticmethod
    def is_valid_phone(phone):
        regex = '^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$'
        return (re.fullmatch(regex, phone))

    @staticmethod
    def is_valid_id(user_id):
        if user_id < 0 or user_id >= len(USERS):
            return False
        return True

    def increase_score(self, amount=1):
        self.score += amount
    def repr(self):
        return f"{self.id} {self.first_name} {self.last_name}"

    def solve(self, task, user_answer):
        if not isinstance(task, Question) and not isinstance(task, Expression):
            return
        result = task.to_dict()
        result['user_answer'] = user_answer
        if user_answer == task.answer:
            result['reward'] = task.reward
        else:
            result['reward'] = 0
        self.history.append([result])


    def __lt__(self, other):
        return self.score < other.score

    def to_dict(self):
        return dict({

            "first_name": self.first_name,
            "last_name": self.last_name,
            "score": self.score
        })

    @staticmethod
    def get_leaderboard():
        return [user.to_dict() for user in sorted(USERS, reverse=True)]
class Expression:
    def __init__(self, id, operation, *values, reward=None):
        self.id = id
        self.operation = operation
        self.values = values
        self.answer = self.__evaluate()
        if reward is None:
            reward = len(values) - 1
        self.reward = reward

    def __evaluate(self):
        return eval(self.to_string())

    @staticmethod
    def is_valid_id(expr_id):
        return 0 <= expr_id < len(EXPRS)

    def to_string(self):
        expr_str = str(self.values[0])
        for value in self.values[1:]:
            expr_str = expr_str + ' ' + self.operation + ' ' + str(value)
        return expr_str
    def repr(self):
        return f" {self.id}: {self.to_string()} = {self.answer}"
    def to_dict(self):
        return dict({

            "id": self.id,
            "operation": self.operation,
            "values": self.values,
            "string_expression": self.to_string()
        })


class Question(ABC):
    def __init__(self, id, title, description, reward=None):
        self.id = id
        self.title = title
        self.description = description
        if reward is None:
            reward = 1
        self.reward = reward

    @property
    @abstractmethod
    def answer(self):
        pass
    def repr(self):
        return f"{self.title}"
    @staticmethod
    def is_valid_id(question_id):
        return len(QUEST) > question_id >= 0

class One_answer(Question):

    def __init__(self, id, title, description, answer, reward=None):
        super().__init__(id, title, description, reward)
        if self.is_valid1(answer):
            self._answer = answer
        else:
            self._answer = None

    @property
    def answer(self):
        return self._answer

    @answer.setter
    def answer(self, value: str):
        if self.is_valid1(value):
            self._answer = value

    @staticmethod
    def is_valid1(answer):
        return isinstance(answer, str)
    def to_dict(self):
        return dict({
            "title":self.title,
            "description": self.description,
            "type": "ONE-ANSWER",
            "answer": self._answer

        })


class MultipleChoice(Question):
    def __init__(self, id, title, description, answer:int, choices:list, reward=None):
        super().__init__(id, title, description, reward)
        if self.is_valid2(answer, choices):
            self._answer = answer
            self.choices = choices
        else:
            self._answer = None
            self.choices = None

    @property
    def answer(self):
        return self._answer

    @answer.setter
    def answer(self, value: int):
        if self.is_valid2(value, self.choices ):
            self._answer = value

    @staticmethod
    def is_valid2(answer, choices):
        if not isinstance(answer, int) or isinstance(choices, list) != 'list':
            return False
        if answer < 0 or answer >= len(choices):
            return False
        return True

    def to_dict(self):
        return dict({
            "title":self.title,
            "description": self.description,
            "type": "MULTIPLE-CHOICE",
            "choices": self.choices,
            "answer": self._answer

        })
