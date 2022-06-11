from aiogram.utils import markdown as md


def movies_top_data_parser(data, page):
    result = ""
    elem_num = (page - 1) * 20 + 1
    for elem in data:
        string = (f"<b>{elem_num}</b>. <em>ID: {elem['filmId']}</em>; "
                  f"<u>Название</u>: {elem['nameRu']}; "
                  f"<u>Год выпуска</u>: {elem['year']}; "
                  f"<u>Жанры</u>: {', '.join([item['genre'] for item in elem['genres']])}\n\n")
        result += string
        elem_num += 1

    return result


def movies_data_parser(data, page, elems_on_page=10):
    result = ""
    elem_num = (page - 1) * elems_on_page + 1
    for elem in data:
        string = (f"<b>{elem_num}.</b> <em>ID: {elem['kinopoiskId']}</em>; "
                  f"<u>Название</u>: {elem['nameRu']}; "
                  f"<u>Год выпуска</u>: {elem['year']}; "
                  f"<u>Жанры</u>: {', '.join([item['genre'] for item in elem['genres']])}\n\n")
        result += string
        elem_num += 1

    return result


def parse_single_movie(data):
    dur_hours = None
    dur_minutes = None
    if data["filmLength"]:
        dur_hours = data["filmLength"] // 60
        dur_minutes = data["filmLength"] % 60
    duration = f"{dur_hours}:{dur_minutes}" if dur_hours else "Отсутствует"

    text = (f"<u>Название</u>: {data['nameRu']}\n"
            f"<u>Название (ориг.)</u>: {'Отсутствует' if not data['nameOriginal'] else data['nameOriginal']}\n"
            f"<u>Описание</u>: {data['description']}\n"
            f"<u>Год выпуска</u>: {data['year']}\n"
            f"<u>Длительность</u>: {duration}\n"
            f"<u>Жанры</u>: {', '.join([item['genre'] for item in data['genres']])}\n"
            f"<u>Страны</u>: {', '.join([item['country'] for item in data['countries']])}\n"
            f"<u>Оценка на Kinopoisk</u>: {data['ratingKinopoisk']}\n"
            f"<u>Оценка на IMDB</u>: {data['ratingImdb']}")

    return text
