from aiogram import F
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from misc import keyboards as kb
from aiogram import Router
from aiogram.fsm.context import FSMContext
import sys
from db import models

router = Router()


# test commit

class ChangeAccessState(StatesGroup):
    get_user_id_state = State()
    add_admin_id_state = State()
    delete_admin_state = State()
    del_item_state = State()


@router.message(F.text == "/admin")
async def admin_kb(message: Message):
    models.LogBase.add(message.from_user.id, message.from_user.username, "/admin")
    if models.Users.check_admin(message.from_user.id) is True:
        await message.answer("Админ меню", reply_markup=kb.owners_kb)


@router.message(F.text == "/give_vip")
async def change_access(message: Message, state: FSMContext):
    models.LogBase.add(message.from_user.id, message.from_user.username, "/give_vip")
    if models.Users.check_admin(message.from_user.id) is True:
        await message.answer("Введите айди пользователя.")
        await state.set_state(ChangeAccessState.get_user_id_state)
    else:
        await message.answer("У вас нет доступа к этой команде.")


@router.message(ChangeAccessState.get_user_id_state, F.text)
async def change_user_access(message: Message, state: FSMContext):
    try:
        telegram_id = int(message.text)
        user = models.Users.change_access(telegram_id, 1)
        if user is True:
            await message.answer("Вы успешно поменяли группу пользователя, на Vip.")
            await state.clear()
        else:
            await message.answer("Неверный телеграм айди.")
            await state.clear()
    except ValueError:
        await message.answer("Неверный телеграм айди.")
        await state.clear()


@router.message(F.text == "/kill")
async def kill_process(message: Message):
    models.LogBase.add(message.from_user.id, message.from_user.username, "/kill")
    if models.Users.check_owner(message.from_user.id) is True:
        await message.answer("Отключаюсь(..")
        sys.exit()
    else:
        await message.answer("У вас нет доступа к этой команде.")


@router.message(F.text == "/add_admin")
async def add_admin(message: Message, state: FSMContext):
    models.LogBase.add(message.from_user.id, message.from_user.username, "/add_admin")
    if models.Users.check_owner(message.from_user.id) is True:
        await message.answer("Введите айди пользователя.")
        await state.set_state(ChangeAccessState.add_admin_id_state)
    else:
        await message.answer("У вас нет доступа к этой команде.")


@router.message(ChangeAccessState.add_admin_id_state, F.text)
async def add_admin_state(message: Message, state: FSMContext):
    try:
        telegram_id = int(message.text)
        user = models.Users.change_access(telegram_id, 2)
        if user is True:
            await message.answer("Вы выдали админ доступ пользователю.")
            await state.clear()
        else:
            await message.answer("Неверный телеграм айди.")
            await state.clear()
    except ValueError:
        await message.answer("Неверный телеграм айди.")
        await state.clear()


@router.message(F.text == "/delete_admin")
async def delete_admin(message: Message, state: FSMContext):
    models.LogBase.add(message.from_user.id, message.from_user.username, "delete_admin")
    if models.Users.check_owner(message.from_user.id) is True:
        await message.answer("Введите айди пользователя.")
        await state.set_state(ChangeAccessState.delete_admin_state)
    else:
        await message.answer("У вас нет доступа к этой команде.")


@router.message(ChangeAccessState.delete_admin_state, F.text)
async def delete_admin_state(message: Message, state: FSMContext):
    try:
        telegram_id = int(message.text)
        user = models.Users.change_access(telegram_id, 0)
        if user is True:
            await message.answer("Вы удалили админ доступ у пользователя.")
            await state.clear()
        else:
            await message.answer("Неверный телеграм айди")
            await state.clear()
    except ValueError:
        await message.answer("Неверный телеграм айди.")
        await state.clear()


@router.message(F.text == "/admin_list")
async def admin_list(message: Message):
    models.LogBase.add(message.from_user.id, message.from_user.username, "admin_list")
    owners = models.session.query(models.Users).where(models.Users.group_id == 3)
    admins = models.session.query(models.Users).where(models.Users.group_id == 2)
    bot_message = 'Список Админов:\n\n'
    for admin in owners:
        x = f"@{admin.username}: {admin.telegram_id} Owner\n"
        bot_message += x
    for admin in admins:
        x = f"@{admin.username}: {admin.telegram_id} Admin\n"
        bot_message += x
    await message.answer(bot_message)


@router.message(F.text == "/del_item")
async def del_item(message: Message, state: FSMContext):
    if models.Users.check_admin(message.from_user.id) is True:
        await message.answer("Введите айди.хешнейм")
        await state.set_state(ChangeAccessState.del_item_state)
    else:
        await message.answer("У вас нет доступа.")


@router.message(ChangeAccessState.del_item_state, F.text)
async def del_item_state(message: Message, state: FSMContext):
    mes = message.text.split(".")
    hash_name = mes[1]
    try:
        telegram_id = int(mes[0])
        models.Items.delete_item(telegram_id, hash_name)
        await message.answer("Вы удалили предмет у пользователя.")
        await state.clear()
    except ValueError:
        await message.answer("Неверный ввод.")
        await state.clear()
