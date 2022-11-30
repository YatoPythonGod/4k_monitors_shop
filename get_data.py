import requests
import asyncio
from bs4 import BeautifulSoup
from copy import deepcopy


def get_data_url():
    for i in range(1, 58):
        if i % 10 == 0:
            asyncio.sleep(2)
        response = requests.get(f'https://4k-monitor.ru/catalog/for-gamers/&tab=list?PAGEN_1={i}')
        print(f'Страница {i} загружена')
        content = response.text
        soup = BeautifulSoup(content, "lxml")
        monitors = soup.find_all("div", class_="card-l--box")
        prices = soup.find("div", class_="row").find_all("div", class_="card--price with-old")
        prices_list = [int(price.text.strip()[:-2].replace(" ", '')) if price.text.strip() else 0 for price in prices]

        pattern = {"Полное наименование": "-", "Диагональ": 0.0, "Соотношение сторон": "-",
                   "Максимальное разрешение": "-", "Тип матрицы": "-", "Максимальная частота обновления (FPS, Гц)": 0,
                   "Цена": 0, "Бренд": "-", "Ссылка": "-"}

        for j, monitor in enumerate(monitors):
            monitor_dict = deepcopy(pattern)
            monitor_dict["Полное наименование"] = monitor.find("a", {'class': "card-l--title"}).text
            monitor_dict["Ссылка"] = "https://4k-monitor.ru" + monitor.find('a', href=True, class_="card-l--title")[
                'href']

            statistic = monitor.find("div").text

            for el in statistic.strip().split('\n'):
                if el.split(':')[0] in monitor_dict:
                    key = el.split(':')[0]
                    if key == 'Диагональ':
                        diagonal = el.split(' ')[1][:-1]
                        monitor_dict[key] = float(diagonal) if float(diagonal) % 1 != 0 else int(diagonal)
                    elif key == 'Максимальная частота обновления (FPS, Гц)':
                        monitor_dict[key] = int(el.split(' ')[-1])
                    else:
                        monitor_dict[key] = el.split(' ')[-1].upper()

            monitor_dict["Цена"] = prices_list[j]
            start = monitor_dict["Полное наименование"].rfind('р') + 2 if 'Apple' not in monitor_dict[
                "Полное наименование"] else monitor_dict["Полное наименование"].find('р') + 2

            if not monitor_dict["Полное наименование"][start].isalpha():
                start += 1
            end = monitor_dict["Полное наименование"].find(' ', start)
            monitor_dict["Бренд"] = monitor_dict["Полное наименование"][start:end].capitalize()
            if monitor_dict["Максимальное разрешение"] == '-':
                if "Full HD" in monitor_dict["Полное наименование"]:
                    monitor_dict["Максимальное разрешение"] = '1920×1080'
            yield monitor_dict


