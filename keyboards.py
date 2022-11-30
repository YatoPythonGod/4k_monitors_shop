from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from sqlite_db import get_criteria


def filter_keyboard() -> InlineKeyboardMarkup:
    filter_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('💸 Цена', callback_data='set_price'),
         InlineKeyboardButton('⚙ Диагональ', callback_data='set_diagonal'),
         InlineKeyboardButton('⚙ Разрешение', callback_data='set_resolution')],
        [InlineKeyboardButton('⚙ Тип матрицы', callback_data='set_matrix'),
         InlineKeyboardButton('⚙ Частота обновления экрана', callback_data='set_frequency'),
         InlineKeyboardButton('⚙ Марка', callback_data='set_brand')],
        [InlineKeyboardButton('🖥 Показать мониторы', callback_data='show'),
         InlineKeyboardButton('❌ Сбросить все фильтры', callback_data='clear')]
    ])

    return filter_kb


def resolution_keyboard() -> InlineKeyboardMarkup:
    resolution_list = get_criteria()['Разрешение']
    resolution_kb = InlineKeyboardMarkup()
    row_button = []
    for i, el in enumerate(resolution_list, start=1):
        if i % 3 == 0:
            resolution_kb.add(*row_button)
            row_button = []
        row_button.append(InlineKeyboardButton(el, callback_data=el))
    resolution_kb.insert(InlineKeyboardButton('🔙 Вернуться к фильтрам', callback_data='back_to_filters'))
    return resolution_kb


def matrix_keyboard() -> InlineKeyboardMarkup:
    matrix_list = get_criteria()['Тип матрицы']
    matrix_kb = InlineKeyboardMarkup()
    row_button = []
    for i, el in enumerate(matrix_list, start=1):
        if i % 3 == 0:
            matrix_kb.add(*row_button)
            row_button = []
        row_button.append(InlineKeyboardButton(el, callback_data=el))
    matrix_kb.insert(InlineKeyboardButton('🔙 Вернуться к фильтрам', callback_data='back_to_filters'))
    return matrix_kb


def brand_keyboard() -> InlineKeyboardMarkup:
    brand_list = get_criteria()['Бренд']
    brand_kb = InlineKeyboardMarkup()
    row_button = []
    for i, el in enumerate(brand_list, start=1):
        if i % 3 == 0:
            brand_kb.add(*row_button)
            row_button = []
        row_button.append(InlineKeyboardButton(el, callback_data=el))
    brand_kb.insert(InlineKeyboardButton('🔙 Вернуться к фильтрам', callback_data='back_to_filters'))
    return brand_kb


def show_keyboard() -> InlineKeyboardMarkup:
    show_kb = InlineKeyboardMarkup().add(InlineKeyboardButton('⏭ Еще', callback_data='get_more'),
                                         InlineKeyboardButton('🔙 Вернуться к фильтрам',
                                                              callback_data='back_to_filters'))

    return show_kb


def its_all_keyboard() -> InlineKeyboardMarkup:
    its_all_kb = InlineKeyboardMarkup().add(InlineKeyboardButton('🔙 Вернуться к фильтрам', callback_data='back_to_filters'))

    return its_all_kb


def restart_keyboard() -> InlineKeyboardMarkup:
    restart_kb = InlineKeyboardMarkup().add(
        InlineKeyboardButton('🔄 Сканировать сайт', callback_data='restart'))

    return restart_kb
