from aiogram import F
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
import keyboards as kb
from aiogram import Router
from aiogram.fsm.context import FSMContext
import sys
import models

router = Router()


class ChangeAccessState(StatesGroup):
    get_user_id_state = State()


@router.message(F.text == "/admin")
async def admin_kb(message: Message):
    if models.check_access(message.from_user.id) in ("Owner", "Admin"):
        await message.answer("Админ меню", reply_markup=kb.admins_kb)


@router.message(F.text == "/give_vip")
async def change_access(message: Message, state: FSMContext):
    telegram_id = message.from_user.id
    if models.check_access(telegram_id) in ("Admin", "Owner"):
        await message.answer("Введите айди пользователя")
        await state.set_state(ChangeAccessState.get_user_id_state)


@router.message(ChangeAccessState.get_user_id_state, F.text)
async def change_user_access(message: Message, state: FSMContext):
    telegram_id = message.text
    models.change_access(telegram_id, "Vip")
    await message.answer("Вы успешно поменяли группу пользователя, на Vip")
    await state.clear()


@router.message(F.text == "/check_access")
async def check_access(message: Message):
    await message.answer(models.check_access(message.from_user.id))


@router.message(F.text == "/kill")
async def kill_process(message: Message):
    if models.check_access(message.from_user.id) in "Owner":
        await message.answer("Отключаюсь(..")
        sys.exit()
    else:
        await message.answer("У вас нет доступа к этой команде")
