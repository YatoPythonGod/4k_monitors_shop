# 4k-monitor_bot

Предсталяю вашему вниманию telegram-бота для поиска мониторов с сайта: https://4k-monitor.ru/

Бот написан на языке python с использованием асинхронного фреймворка для Telegram Bot API - aiogram.
Для парсинга сайта используется библиотека - Beautiful Soup. 
Хранение и выдача информации реализовано через фреймворк SQLite.

Данный проект несет только информативный характер и разработан в рамках программы обучения GeekBrains.

Любая публикация и монетизация данного проекта запрещена!
_ _ _
## Установка
Для установки бота на свое устройтво необходимо:
1. Скачать данный проект > [Скачать](https://github.com/YatoPythonGod/4k_monitors_shop/archive/refs/heads/main.zip);
2. Активировать вирутальное окружение;
```
python -m venv venv
source venv/bin/activate
```
3. Установить необходимой модули из файла - _requirements.txt_.
```
pip install -r requirements.txt
```
_ _ _
## Описание
__/start__ - активирует бота.

После активации бота, происходит считывание информации с сайта  - https://4k-monitor.ru/.
Обновление занимает около 2 минут и происходит ежедневно. Все дальнейшее взаимодействие происходит через инлайн клавиатуру.

По завершению обновления, пользователю предалается настроить фильтры для подброа мониторов:

![filters.png](/RM_screenshots/filters.png)

- __Цена__ - пользователь может ввести цену от и до через дефис, при этом пользователь получает уведомление о минимальной и максимальной цене
- __Диагональ__ - пользователь может ввести диагональ от и до через дефис
- __Разрешение__ - при нажатии кнопки появляется инлайн клавиатура, в которой можно выбрать необходимые разрешения экрана
- __Тип матрицы__ - при нажатии кнопки появляется инлайн клавиатура, в которой можно выбрать необходимые типы матриц
- __Частота обновеления__ - пользователь может ввести частоту обновления экрана от и до через дефис
- __Марка__ - при нажатии кнопки появляется инлайн клавиатура, в которой можно выбрать необходимые марки
- __Показать мониторы__ - выводит мониторы по заданным фильтрам, вывод производится по 10 мониторов, далее пользователь может вывести следующие мониторы или вернуться обратно к фильтрам
- __Сбросить фильтры__ - производит сброс всех фильтров

### Формат вывода мониторов
Каждый монитор выводится отдельным сообщением и содержит следующу информацию:

- __Название монитора__ (+ссылка на монитор которая зашита в название)
- Диагональ
- Соотношение сторон
- Максимальное разрешение
- Тип матрицы
- Максимальная частота обновления
- Цена

![monitor_info.png](/RM_screenshots/monitor_info.png)




## Разработка

Над проектом работал студент факултета GeekBrains "Разработчик - Программист"  
- Юркин Сергей : [YATO](https://github.com/YatoPythonGod)

- По вопросам сотрудничества пишите в [_Telegram_](https://t.me/Sergeyiidf)


## Спасибо за внимание!

Благодарю за внимание! А ткаже предлагаю посетить шоурум магазина [4k-monitor](https://4k-monitor.ru/) по адресу: [г. Москва, Спартаковский пер., д.2, стр.1, вход 4, офис 3](https://4k-monitor.ru/about/contacts/)

Высококвалифицированные специалисты помогут вам подобрать монитор под ваши потребности, а также вы вживую сможете его протестировать на самых топовых девайсах.

![4k_monitor.png](/RM_screenshots/4k_monitor.png)

