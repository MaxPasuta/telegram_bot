
from .models import Regulations


class Regulation():
    # конструктор
    def __init__(self, question, legal_flag, main_question):
        self.question = question  # устанавливаем вопрос
        self.main_question = main_question  # устанавливаем вопрос

    def display_info(self):
        print("Привет, меня зовут", self.name)


def questions(self, flag):
    pass


