from aiogram import Dispatcher, types, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from bot.models import FieldOfLaw,StatementsOfClaim,Regulations
from django.conf import settings


available_buttons_1 = ["Да", "Нет", "Назад"]
available_buttons_2 = ["Да", "Нет"]

dict_legal_flag = {}
dict_question = {}

my_bot = Bot(token=settings.TOKEN)


class SearchApplication(StatesGroup):
    waiting_for_legal_flag = State()
    waiting_for_answering_questions = State()
    waiting_for_verification_statement = State()


async def start(message: types.Message):
    await message.answer("Опишите тезисами необходимую Вам область права:")
    await SearchApplication.waiting_for_legal_flag.set()


async def legal_flag_check(message: types.Message, state: FSMContext):
    flag = 0
    data = message.text.lower()
    for i in FieldOfLaw.objects.all():
        for word in i.theses.split(', '):
            if data.find(word) != -1:
                flag = i.id
    if flag != 0:
        dict_legal_flag[message.from_user.id] = flag
        dict_question[message.from_user.id] = 0
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for name in available_buttons_1:
            keyboard.add(name)
        data = Regulations.objects.filter(legal_flag=flag)[dict_question.get(message.from_user.id)]
        await message.answer(data.question, reply_markup=keyboard)
        await SearchApplication.waiting_for_answering_questions.set()
    else:
        await message.answer('Данную область права я пока не поддерживаю')
        await state.finish()


async def answering_questions(message: types.Message, state: FSMContext):
    if message.text not in available_buttons_1:
        await message.answer("Пожалуйста, используя клавиатуру ниже.")
        return
    flag = dict_legal_flag.get(message.from_user.id)
    question_number = dict_question.get(message.from_user.id)
    try:
        if message.text == 'Нет':
            data = Regulations.objects.filter(legal_flag=flag)[question_number]
            if data.main_question != 0:
                question_number += data.main_question+1
                dict_question.update({message.from_user.id: question_number})
                data = Regulations.objects.filter(legal_flag=flag)[question_number]
                await message.answer(data.question)
            else:
                question_number += 1
                dict_question.update({message.from_user.id: question_number})
                data = Regulations.objects.filter(legal_flag=flag)[question_number]
                await message.answer(data.question)

        if message.text == 'Да':
            data = Regulations.objects.filter(legal_flag=flag)[question_number]
            if data.main_question == 0:
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                for name in available_buttons_2:
                    keyboard.add(name)
                question_number = Regulations.objects.filter(legal_flag=flag)[question_number].id
                dict_question.update({message.from_user.id: question_number})
                await message.answer("Мы нашли нужное исковое заявление, скачать?", reply_markup=keyboard)
                await SearchApplication.waiting_for_verification_statement.set()
            else:
                question_number += 1
                dict_question.update({message.from_user.id: question_number})
                data = Regulations.objects.filter(legal_flag=flag)[question_number]
                await message.answer(data.question)

        if message.text == 'Назад':
            if question_number == 0:
                await message.answer("Действие отменено",reply_markup=types.ReplyKeyboardRemove())
                await state.finish()
            await message.answer(Regulations.objects.filter(legal_flag=flag)[question_number].question)
            question_number -= 1
            dict_question.update({message.from_user.id: question_number})
    except IndexError:
        await message.answer('Это пока все вопросы из моей базы', reply_markup=types.ReplyKeyboardRemove())
        await message.answer('Возможно Ваша конкретная проблема сложнее, обратитесь к юристу')
        await state.finish()


async def verification_statement(message: types.Message, state: FSMContext):
    if message.text not in available_buttons_2:
        await message.answer("Пожалуйста, используя клавиатуру ниже.")
        return
    question_id = dict_question.get(message.from_user.id)
    data = StatementsOfClaim.objects.get(regulations__id=question_id)
    del dict_legal_flag[message.from_user.id]
    del dict_question[message.from_user.id]

    if message.text == 'Нет':
        await message.answer("Вам необходимо оформить заявление: " + data.title, reply_markup=types.ReplyKeyboardRemove())
        await state.finish()

    if message.text == 'Да':
        file = open(data.document.path, 'rb')
        await my_bot.send_document(message.from_user.id, file, caption='Этот файл специально для Вас! '+ data.title)
        await message.answer("После оформление документов вам необходимо: " + data.action_algorithm, reply_markup=types.ReplyKeyboardRemove())
        await state.finish()


def register_handlers_legal(dp: Dispatcher):
    dp.register_message_handler(start, commands="questions", state="*")
    dp.register_message_handler(legal_flag_check, state=SearchApplication.waiting_for_legal_flag)
    dp.register_message_handler(answering_questions, state=SearchApplication.waiting_for_answering_questions)
    dp.register_message_handler(verification_statement, state=SearchApplication.waiting_for_verification_statement)

