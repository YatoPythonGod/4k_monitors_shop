from aiogram import types, executor, Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils.markdown import hbold, hlink

from config import TOKEN_API
from keyboards import *
import sqlite_db
from get_data import get_data_url

bot = Bot(token=TOKEN_API, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
count = 0

all_criteria = sqlite_db.get_criteria()
user_filters = {}


class UserStates(StatesGroup):
    price_state = State()
    diagonal_state = State()
    frequency_state = State()
    resolution_state = State()
    matrix_state = State()
    brand_state = State()


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message, state: FSMContext):
    global user_filters
    global count
    global all_criteria
    count = 0
    user_filters = {}
    if state:
        await state.finish()
    await bot.send_message(chat_id=message.chat.id,
                           text='🖥4k-monitor приветствует тебя!')
    await bot.send_message(chat_id=message.chat.id,
                           text='Сканирую сайт, это может занять несколько минут!\nДождитесь сообщение о готовности! ')
    if not sqlite_db.checking_dv_today():
        await sqlite_db.create_db()
        sqlite_db.insert_varible_into_table(get_data_url())

    if not all_criteria:
        all_criteria = sqlite_db.get_criteria()

    await bot.send_message(chat_id=message.chat.id,
                           text='🔥🔥🔥Промокод: YATO10🔥🔥🔥')
    await message.answer(text='👌База обновлена! Настройте фильтры:',
                         reply_markup=filter_keyboard())


@dp.callback_query_handler(text='clear', state='*')
async def cmd_cancel(call: types.CallbackQuery, state: FSMContext):
    if not sqlite_db.checking_dv_today():
        return await bot.send_message(chat_id=call.message.chat.id, text='Необходимо просканиовать сайт сегодня!',
                                      reply_markup=restart_keyboard())
    global user_filters
    user_filters = {}
    if state:
        await state.finish()
    return await call.answer('Вы отменили все фильтры!', show_alert=True)


@dp.callback_query_handler(text='set_price', state=None)
async def cmd_set_price(call: types.CallbackQuery, state: FSMContext):
    if not sqlite_db.checking_dv_today():
        return await bot.send_message(chat_id=call.message.chat.id, text='Необходимо просканиовать сайт сегодня!',
                                      reply_markup=restart_keyboard())
    if state:
        await state.finish()
    await UserStates.price_state.set()
    global all_criteria

    await call.answer(
        f'Цены в нашем магазине вырируются от {all_criteria["Цена"][0]} до {all_criteria["Цена"][1]} ₽ \n '
        f'Введите цену «от» и «до» через дефис:', show_alert=True)


@dp.callback_query_handler(text='show', state=None)
async def cmd_show(callback: types.CallbackQuery, state: FSMContext):
    if not sqlite_db.checking_dv_today():
        return await bot.send_message(chat_id=callback.message.chat.id, text='Необходимо просканиовать сайт сегодня!',
                                      reply_markup=restart_keyboard())
    global count
    global user_filters
    global all_criteria

    if state:
        await state.finish()

    data = sqlite_db.get_db_data(10, count, user_filters) if user_filters else sqlite_db.get_db_data(10, count,
                                                                                                     all_criteria)

    for index, monitor in enumerate(data):
        card = f'{hlink(monitor.get("Полное наименование"), monitor.get("Ссылка"))}\n' \
               f'{hbold("Диагональ: ")}{monitor.get("Диагональ")}"\n' \
               f'{hbold("Соотношение сторон: ")}{monitor.get("Соотношение сторон")}\n' \
               f'{hbold("Максимальное разрешение: ")}{monitor.get("Максимальное разрешение")}\n' \
               f'{hbold("Тип матрицы: ")}{monitor.get("Тип матрицы")}\n' \
               f'{hbold("Максимальная частота обновления: ")}{monitor.get("Максимальная частота обновления (FPS, Гц)")} Гц\n' \
               f'{hbold("Цена: ")}{monitor.get("Цена")} ₽'
        count = monitor.get("rowid")
        await callback.message.answer(card)
    if len(data) == 0:
        count = 0
        return await callback.message.answer(f'По заданным фильтрам ничего не удалось найти 🤷‍♂️\n {user_filters}',
                                             reply_markup=its_all_keyboard())
    elif 0 < len(data) < 10:
        count = 0
        return await callback.message.answer('Это все мониторы по заданным фильтрам! Промокод 👉 YATO10',
                                             reply_markup=its_all_keyboard())
    await callback.message.answer('Показать 10 следующих? Промокод 👉 YATO10', reply_markup=show_keyboard())


@dp.callback_query_handler(text='get_more', state=None)
async def cmd_get_more(callback: types.CallbackQuery, state: FSMContext):
    if not sqlite_db.checking_dv_today():
        return await bot.send_message(chat_id=callback.message.chat.id, text='Необходимо просканиовать сайт сегодня!',
                                      reply_markup=restart_keyboard())
    if state:
        await state.finish()
    global count
    global user_filters
    data = sqlite_db.get_db_data(10, count, user_filters) if user_filters else sqlite_db.get_db_data(10, count,
                                                                                                     all_criteria)

    for index, monitor in enumerate(data):
        card = f'{hlink(monitor.get("Полное наименование"), monitor.get("Ссылка"))}\n' \
               f'{hbold("Диагональ: ")}{monitor.get("Диагональ")}"\n' \
               f'{hbold("Соотношение сторон: ")}{monitor.get("Соотношение сторон")}\n' \
               f'{hbold("Максимальное разрешение: ")}{monitor.get("Максимальное разрешение")}\n' \
               f'{hbold("Тип матрицы: ")}{monitor.get("Тип матрицы")}\n' \
               f'{hbold("Максимальная частота обновления: ")}{monitor.get("Максимальная частота обновления (FPS, Гц)")} Гц\n' \
               f'{hbold("Цена: ")}{monitor.get("Цена")} ₽'
        count = monitor.get("rowid")

        await callback.message.answer(card)

    if len(data) < 10:
        count = 0
        return await callback.message.answer('Это все мониторы по заданным фильтрам! Промокод 👉 YATO10',
                                             reply_markup=its_all_keyboard())
    await callback.message.answer('Показать 10 следующих? Промокод 👉 YATO10', reply_markup=show_keyboard())


@dp.callback_query_handler(text='set_diagonal', state=None)
async def cmd_set_diagonal(call: types.CallbackQuery, state: FSMContext):
    if not sqlite_db.checking_dv_today():
        return await bot.send_message(chat_id=call.message.chat.id, text='Необходимо просканиовать сайт сегодня!',
                                      reply_markup=restart_keyboard())
    if state:
        await state.finish()
    await UserStates.diagonal_state.set()
    global all_criteria

    await call.answer(
        f'Размеры мониторов в нашем магазине варируются от {all_criteria["Диагональ"][0]} до {all_criteria["Диагональ"][1]} дюймов\n '
        f'Введите диагональ монитора «от» и «до» через дефис:', show_alert=True)


@dp.callback_query_handler(text='set_frequency', state=None)
async def cmd_set_frequency(call: types.CallbackQuery, state: FSMContext):
    if not sqlite_db.checking_dv_today():
        return await bot.send_message(chat_id=call.message.chat.id, text='Необходимо просканиовать сайт сегодня!',
                                      reply_markup=restart_keyboard())
    if state:
        await state.finish()
    await UserStates.frequency_state.set()
    global all_criteria

    await call.answer(
        f'Частота кадров мониторов варируется от {all_criteria["Частота кадров"][0]} до {all_criteria["Частота кадров"][1]} Герц\n '
        f'Введите частоту кадров монитора «от» и «до» через дефис:', show_alert=True)


@dp.callback_query_handler(text='set_resolution', state=None)
async def cmd_set_resolution(callback: types.CallbackQuery, state: FSMContext):
    if not sqlite_db.checking_dv_today():
        return await bot.send_message(chat_id=callback.message.chat.id, text='Необходимо просканиовать сайт сегодня!',
                                      reply_markup=restart_keyboard())
    if state:
        await state.finish()
    await UserStates.resolution_state.set()
    await callback.message.answer('Выберете разрешение:', reply_markup=resolution_keyboard())


@dp.callback_query_handler(text='set_matrix', state=None)
async def cmd_set_matrix(callback: types.CallbackQuery, state: FSMContext):
    if not sqlite_db.checking_dv_today():
        return await bot.send_message(chat_id=callback.message.chat.id, text='Необходимо просканиовать сайт сегодня!',
                                      reply_markup=restart_keyboard())
    if state:
        await state.finish()
    await UserStates.matrix_state.set()
    await callback.message.answer('Выберете тип матрицы:', reply_markup=matrix_keyboard())


@dp.callback_query_handler(text='set_brand', state=None)
async def cmd_set_brand(callback: types.CallbackQuery, state: FSMContext):
    if not sqlite_db.checking_dv_today():
        return await bot.send_message(chat_id=callback.message.chat.id, text='Необходимо просканиовать сайт сегодня!',
                                      reply_markup=restart_keyboard())
    if state:
        await state.finish()
    await UserStates.brand_state.set()
    await callback.message.answer('Выберете марку монитора:', reply_markup=brand_keyboard())


@dp.callback_query_handler(text='back_to_filters', state=UserStates.brand_state)
async def brand_to_filters(callback: types.CallbackQuery, state: FSMContext):
    if not sqlite_db.checking_dv_today():
        return await bot.send_message(chat_id=callback.message.chat.id, text='Необходимо просканиовать сайт сегодня!',
                                      reply_markup=restart_keyboard())
    if state:
        await state.finish()
    global user_filters
    if "Бренд" in user_filters:
        user_filters["Бренд"] = set(user_filters["Бренд"])
        await callback.message.answer(f'Выбранные марки мониторов: {", ".join(user_filters["Бренд"])}',
                                      reply_markup=filter_keyboard())
    else:
        await callback.message.answer(f'Фильтр марки мониторов не установлен', reply_markup=filter_keyboard())


@dp.callback_query_handler(text='back_to_filters', state=UserStates.matrix_state)
async def matrix_to_filters(callback: types.CallbackQuery, state: FSMContext):
    if not sqlite_db.checking_dv_today():
        return await bot.send_message(chat_id=callback.message.chat.id, text='Необходимо просканиовать сайт сегодня!',
                                      reply_markup=restart_keyboard())
    if state:
        await state.finish()
    global user_filters
    if "Тип матрицы" in user_filters:
        user_filters["Тип матрицы"] = set(user_filters["Тип матрицы"])
        await callback.message.answer(f'Выбранные типы матриц: {", ".join(user_filters["Тип матрицы"])}',
                                      reply_markup=filter_keyboard())
    else:
        await callback.message.answer(f'Фильтр на тип матрицы монитора не установлен', reply_markup=filter_keyboard())


@dp.callback_query_handler(text='back_to_filters', state=UserStates.resolution_state)
async def res_to_filters(callback: types.CallbackQuery, state: FSMContext):
    if not sqlite_db.checking_dv_today():
        return await bot.send_message(chat_id=callback.message.chat.id, text='Необходимо просканиовать сайт сегодня!',
                                      reply_markup=restart_keyboard())
    if state:
        await state.finish()
    global user_filters
    if "Разрешение" in user_filters:
        user_filters["Разрешение"] = set(user_filters["Разрешение"])
        await callback.message.answer(f'Выбранные разрешения: {", ".join(user_filters["Разрешение"])}',
                                      reply_markup=filter_keyboard())
    else:
        await callback.message.answer(f'Фильтр на разрешение монитора не установлен', reply_markup=filter_keyboard())


@dp.callback_query_handler(text='back_to_filters', state=None)
async def show_to_filters(callback: types.CallbackQuery, state: FSMContext):
    if not sqlite_db.checking_dv_today():
        return await bot.send_message(chat_id=callback.message.chat.id, text='Необходимо просканиовать сайт сегодня!',
                                      reply_markup=restart_keyboard())
    if state:
        await state.finish()

    global count
    global user_filters
    count = 0
    filters = "\n".join([f'{hbold(k)}: {v}' for k, v in user_filters.items()])
    await callback.message.answer(f'Текущие фильтры: \n{filters}')
    await callback.message.answer(text='Не забудьте обновить фильтры!\nИ воспользоваться промокодом: YATO10',
                                  reply_markup=filter_keyboard())


@dp.callback_query_handler(state=UserStates.brand_state)
async def get_brand_filters(callback: types.CallbackQuery, state: FSMContext):
    global user_filters
    brand_choise = user_filters.get("Бренд", set())
    brand_choise.add(f'"{callback.data}"')
    user_filters["Бренд"] = brand_choise

    await callback.message.answer(f'Марка монитора {callback.data} добавлена в фильтр')


@dp.callback_query_handler(state=UserStates.matrix_state)
async def get_matrix_filters(callback: types.CallbackQuery, state: FSMContext):
    global user_filters
    matrix_choise = user_filters.get("Тип матрицы", set())
    matrix_choise.add(f'"{callback.data}"')
    user_filters["Тип матрицы"] = matrix_choise

    await callback.message.answer(f'Тип матрицы {callback.data} добавлен в фильтр')


@dp.callback_query_handler(state=UserStates.resolution_state)
async def get_resolution_filters(callback: types.CallbackQuery, state: FSMContext):
    global user_filters
    res_choise = user_filters.get("Разрешение", set())
    res_choise.add(f'"{callback.data}"')
    user_filters["Разрешение"] = res_choise

    await callback.message.answer(f'Разрешение {callback.data} добавлено в фильтр')


@dp.message_handler(state=UserStates.price_state)
async def get_price_filters(message: types.Message, state: FSMContext):
    global all_criteria
    global user_filters
    try:
        start_price = int(message.text.replace(' ', '').split('-')[0])
        finish_price = int(message.text.replace(' ', '').split('-')[1])
        if start_price >= finish_price or finish_price < all_criteria["Цена"][0]:
            return await bot.send_message(message.chat.id, f'🤯 В этом диапазоне 👉{start_price} - {finish_price}👈'
                                                           f' мы вряд ли сможем что-то найти. Задай цену от и до через дефис:')
        user_filters["Цена"] = [start_price, finish_price]

    except ValueError:
        return await bot.send_message(message.chat.id,
                                      f'❗️Некорректный ввод, цену необходимо вводить через дефис! 👉Пример: 20000-50000\n'
                                      f'Попробуй еще раз!')
    except Exception:
        return await bot.send_message(message.chat.id,
                                      f'❗️Некорректный ввод, цену необходимо вводить через дефис! 👉Пример: 20000-50000\n'
                                      f'Попробуй еще раз!')

    await bot.send_message(message.chat.id,
                           f'Цена зафиксирована: {user_filters["Цена"][0]} ₽  - {user_filters["Цена"][1]} ₽')

    return await state.finish()


@dp.message_handler(state=UserStates.diagonal_state)
async def get_diagonal_filters(message: types.Message, state: FSMContext):
    global all_criteria
    global user_filters
    try:
        start_diagonal = int(message.text.replace(' ', '').split('-')[0])
        finish_diagonal = int(message.text.replace(' ', '').split('-')[1])
        if start_diagonal > finish_diagonal or finish_diagonal < all_criteria["Диагональ"][0]:
            return await bot.send_message(message.chat.id,
                                          f'🤯 В этом диапазоне 👉{start_diagonal} - {finish_diagonal}👈'
                                          f' мы вряд ли сможем что-то найти. Задайте диагональ от и до через дефис:')
        user_filters['Диагональ'] = [start_diagonal, finish_diagonal]

    except ValueError:
        return await bot.send_message(message.chat.id,
                                      f'❗️Некорректный ввод, диагональ необходимо вводить через дефис! 👉Пример: 24-32\n'
                                      f'Попробуй еще раз!')
    except Exception:
        return await bot.send_message(message.chat.id,
                                      f'❗️Некорректный ввод, диагональ необходимо вводить через дефис! 👉Пример: 24-32\n'
                                      f'Попробуй еще раз!')

    await bot.send_message(message.chat.id,
                           f'Диагональ зафиксирована: {user_filters["Диагональ"][0]}"  - {user_filters["Диагональ"][1]}"')

    return await state.finish()


@dp.message_handler(state=UserStates.frequency_state)
async def get_frequency_filters(message: types.Message, state: FSMContext):
    global all_criteria
    global user_filters
    try:
        start_frequency = int(message.text.replace(' ', '').split('-')[0])
        finish_frequency = int(message.text.replace(' ', '').split('-')[1])
        if start_frequency > finish_frequency or finish_frequency < all_criteria["Частота кадров"][0]:
            return await bot.send_message(message.chat.id,
                                          f'🤯 В этом диапазоне 👉{start_frequency} - {finish_frequency}👈'
                                          f' мы вряд ли сможем что-то найти. Задайте частоту кадров от и до через дефис:')
        user_filters['Частота кадров'] = [start_frequency, finish_frequency]

    except ValueError:
        return await bot.send_message(message.chat.id,
                                      f'❗️Некорректный ввод, значения необходимо вводить через дефис! 👉Пример: 120-240\n'
                                      f'Попробуй еще раз!')
    except Exception:
        return await bot.send_message(message.chat.id,
                                      f'❗️Некорректный ввод, значения необходимо вводить через дефис! 👉Пример: 120-240\n'
                                      f'Попробуй еще раз!')

    await bot.send_message(message.chat.id,
                           f'Частота кадров монитора зафиксирована: {user_filters["Частота кадров"][0]}Гц  - {user_filters["Частота кадров"][1]}Гц')

    return await state.finish()


@dp.callback_query_handler(text='restart', state='*')
async def cmd_restart(callback: types.CallbackQuery, state: FSMContext):
    global user_filters
    global count
    global all_criteria
    count = 0
    user_filters = {}
    if state:
        await state.finish()
    await bot.send_message(chat_id=callback.message.chat.id,
                           text='🖥4k-monitor приветствует тебя!')
    await bot.send_message(chat_id=callback.message.chat.id,
                           text='Сканирую сайт, это может занять несколько минут!\nДождитесь сообщение о готовности! ')
    if not sqlite_db.checking_dv_today():
        await sqlite_db.create_db()
        sqlite_db.insert_varible_into_table(get_data_url())

    if not all_criteria:
        all_criteria = sqlite_db.get_criteria()

    await bot.send_message(chat_id=callback.message.chat.id,
                           text='🔥🔥🔥Промокод: YATO10🔥🔥🔥')
    await callback.message.answer(text='👌База обновлена! Настройте фильтры:',
                         reply_markup=filter_keyboard())


def main():
    executor.start_polling(dispatcher=dp,
                           skip_updates=True)
