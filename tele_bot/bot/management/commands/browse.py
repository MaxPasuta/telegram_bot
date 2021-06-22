from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from bot.models import FieldOfLaw,StatementsOfClaim,Regulations
from django.conf import settings
from aiogram import Dispatcher, types, Bot

available_buttons = ["Да", "Нет"]

my_bot = Bot(token=settings.TOKEN)


class RequestApplication(StatesGroup):
    waiting_for_input = State()
    waiting_for_confirmation = State()


async def start(message: types.Message):
    await message.answer("Введите название искового заявления")
    await RequestApplication.waiting_for_input.set()


async def search(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in available_buttons:
        keyboard.add(name)
    data = message.text
    flag = 0
    for i in StatementsOfClaim.objects.all():
        if i.title.lower() == data.lower():
            await state.update_data(document_id=i.id)
            await RequestApplication.waiting_for_confirmation.set()
            flag = 1
            await message.answer("Вы имеете ввиду: " + i.title + ' ? ', reply_markup=keyboard)
    if flag == 0:
        await message.answer("К сожалению такого искового заявление в моей базе нет")
        await state.finish()


async def output(message: types.Message, state: FSMContext):
    if message.text not in available_buttons:
        await message.answer("Пожалуйста, используя клавиатуру ниже.")
        return

    if message.text == 'Да':
        document = await state.get_data()
        data = StatementsOfClaim.objects.get(id=document['document_id'])
        file = open(data.document.path, 'rb')
        await my_bot.send_document(message.from_user.id, file, caption='Этот файл специально для Вас!' + data.title, reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
    if message.text == 'Нет':
        await message.answer("К сожалению больше исковых заявлений по вашему запросу в моей базе нет", reply_markup=types.ReplyKeyboardRemove())
        await state.finish()


def register_handlers_browse(dp: Dispatcher):
    dp.register_message_handler(start, commands="browse", state="*")
    dp.register_message_handler(search, state=RequestApplication.waiting_for_input)
    dp.register_message_handler(output, state=RequestApplication.waiting_for_confirmation)
