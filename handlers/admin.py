from aiogram import F
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
import json_support
import keyboards as kb
from aiogram import Router
from aiogram.fsm.context import FSMContext
import sys

json_data = "user_list.json"
push_data = "users_time.json"
admins = "admins.json"
router = Router()


class AdminAddStatus(StatesGroup):
    id_add = State()
    group_add = State()


@router.message(F.text == "/kill")
async def kill_process(message: Message):
    admin_data = json_support.read_inf(admins)
    user_id = f"{message.from_user.id}"
    if user_id in admin_data.keys():
        await message.answer("Вы вырубили бота")
        sys.exit()
    else:
        await message.answer("Че пишешь, напиши /help, если хочешь кнопки, то пиши /start.")


@router.message(F.text == '/add_admin')
async def add_admin(message: Message, state: FSMContext):
    admin_data = json_support.read_inf(admins)
    user_id = f"{message.from_user.id}"
    if user_id in admin_data.keys():
        if admin_data[user_id] not in "Owner":
            await message.answer("У вас недостаточно прав")
        else:
            await message.answer("Введите телеграм айди пользователя")
            await state.set_state(AdminAddStatus.id_add)
    else:
        await message.answer("Че пишешь, напиши /help, если хочешь кнопки, то пиши /start.")

@router.message(AdminAddStatus.id_add, F.text)
async def id_add(message: Message, state: FSMContext):
    user_id = message.text
    data = json_support.read_inf(admins)
    us = {}
    us = {user_id: "Admin"}
    data.update(us)
    json_support.write_inf(data, admins)
    print(data)

@router.message()
async def echo(message: Message):
    await message.answer("Че пишешь, напиши /help, если хочешь кнопки, то пиши /start.")
