import requests
import pandas as pd
import glob
import os.path
from datetime import datetime
from io import StringIO

# Айди областей, отсортированных по украинскому алфавиту
provinces = [25, 27, 26, 12, 3, 4, 8, 22, 23, 24, 10, 9, 11, 13, 14, 15, 16, 17, 18, 19, 20, 21, 6, 1, 2, 7, 5]


def download_data(original_id):
    # Дефолтная ссылка для скачивания данных с форматированным provinceID
    url = f'https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?' \
          f'country=UKR' \
          f'&provinceID={original_id}' \
          f'&year1=1981' \
          f'&year2=2021' \
          f'&type=Mean'

    # Получаем данные и заменяем тег <br><tt><pre> на перенос строки
    response = requests.get(url).text.replace("<br><tt><pre>", "\n")

    # Считываем дата фрейм из нашей строки, игнорируем первую, последнюю строку и последнюю пустую колонку
    df = pd.read_csv(StringIO(response), index_col=0, skiprows=1, skipfooter=1, engine='python',
                     usecols=range(7), names=['year', 'week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI'])
    # Удаляем строки с значением '-1' (данных за эту неделю нет)
    df = df.drop(df[df.SMN == -1].index)

    # Получение текущего времени и его форматирование через паттерн
    current_datetime = datetime.now().strftime("%d.%m.%Y %H-%M-%S")
    df.to_csv(f'province{provinces[original_id]}_{current_datetime}.csv')


def read_dir(path):
    appended_data = []
    # Получаем все файлы по поттерну из указанной папки
    for path in glob.glob(os.path.join(path, "province*.csv")):
        df = pd.read_csv(path)
        # Парсим номер области из названия файла и устанавливаем это значение в колонке
        df['province'] = int(os.path.basename(path).split("_")[0].replace("province", ""))
        # Сохраняем полученный фрейм
        appended_data.append(df)
    # Создаем один фрейм из всего списка
    return pd.concat(appended_data)


def get_extrema_vhi(df, province, year):
    # Фильтруем значения по указанной области и году и получаем VHI
    vhi = df[(df['province'] == province) & (df['year'] == year)]['VHI']
    print(vhi.tolist())
    # Вычисляем минимум
    print("min", vhi.min())
    # Вычисляем максимум
    print("max", vhi.max())


def get_vhi(df, province):
    # Фильтруем значения по указанной области
    df = df[df['province'] == province]
    print(df['VHI'].tolist())
    return df


def get_year(df):
    # Получаем уникальные значения year
    print(df['year'].unique().tolist())


def check_middle_dry(df, province):
    df = get_vhi(df, province)
    # Фильтруем значения где VHI лежит в диапазоне от 15 до 35
    get_year(df[(df['VHI'] < 35) & (df['VHI'] > 15)])


def check_extreme_dry(df, province):
    df = get_vhi(df, province)
    # Фильтруем значения где VHI меньше 15
    get_year(df[(df['VHI'] < 15)])


# Скачиваем данные на каждый регион
for i in range(len(provinces)):
    download_data(i)

df = read_dir("D:\Projects\python\lab1")
get_extrema_vhi(df, 2, 2009)
check_middle_dry(df, 2)
check_extreme_dry(df, 2)
