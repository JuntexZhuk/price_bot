from aiogram import F
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
import steammarket as sm
from data import json_support, case_translation
import keyboards as kb
from aiogram import Router
from aiogram.fsm.context import FSMContext
import models
from data.config import cases as constcases

router = Router()
json_data = "user_list.json"


@router.message(F.text == '/cases')
async def cases(message: Message):
    x = ''
    user_id = f"{message.from_user.id}"
    data = json_support.read_inf(json_data)
    if user_id in data.keys() and len(data[user_id]) > 0:
        for case in data[user_id]:
            case_price = sm.get_item(730, case, currency='RUB')
            case = case_translation.case_translation(case)
            x = f"{x + case}: {str(case_price['lowest_price'])} \n"
        await message.answer(f"Цены на ваши кейсы:\n{x}")
        models.get_prices(constcases)
    else:
        await message.answer("Вы не добавили кейсы.")


@router.message(F.text == "/add_case")
async def item_list(message: Message):
    await message.answer("Какой кейс вы хотите добавить?:", reply_markup=kb.cases)


@router.callback_query()
async def answer(callback: CallbackQuery):
    user_id = callback.message.chat.id
    user_id = f"{user_id}"
    case = case_translation.case_translation(callback.data)
    await callback.message.answer(f"Вы добавили {case}.")
    data = json_support.read_inf(json_data)
    cases_list = []
    if user_id in data.keys():
        cases_list = data[user_id]
    else:
        pass
    if callback.data not in cases_list or user_id not in data.keys():
        cases_list.append(callback.data)
        c = {user_id: cases_list}
        data.update(c)
        json_support.write_inf(data, json_data)
        print(f"{user_id},{callback.message.chat.first_name} add {case}")
    else:
        pass


@router.message(F.text == '/clear')
async def clear(message: Message):
    data = json_support.read_inf(json_data)
    user_id = f"{message.from_user.id}"
    del data[user_id]
    json_support.write_inf(data, json_data)
    await message.answer("Локальный список ваших кейсов успешно очищен.")


@router.message(F.text == "/start")
async def start(message: Message):
    telegram_id = message.from_user.id
    nickname = message.from_user.username
    models.add_user(telegram_id, nickname)
    await message.answer("Ну привет", reply_markup=kb.main_kb)


@router.message(F.text == "/help")
async def help_func(message: Message):
    await message.answer("Помогите...")


@router.message(F.text == "/vip")
async def get_vip(message: Message):
    if models.check_access(message.from_user.id) in ("Vip", "Admin", "Owner"):
        await message.answer("Вип меню", reply_markup=kb.users_vip_kb)
    else:
        await message.answer("У вас нет доступа к это команде")


@router.message()
async def echo(message: Message):
    await message.answer("Че пишешь, напиши /help, если хочешь кнопки, то пиши /start.")
