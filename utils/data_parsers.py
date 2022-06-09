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


def movies_data_parser(data, page):
    result = ""
    elem_num = (page - 1) * 10 + 1
    for elem in data:
        string = (f"<b>{elem_num}.</b> <em>ID: {elem['kinopoiskId']}</em>; "
                  f"<u>Название</u>: {elem['nameRu']}; "
                  f"<u>Год выпуска</u>: {elem['year']}; "
                  f"<u>Жанры</u>: {', '.join([item['genre'] for item in elem['genres']])}\n\n")
        result += string
        elem_num += 1

    return result


def parse_single_movie(data):
    dur_hours = data["filmLength"] // 60
    dur_minutes = data["filmLength"] % 60

    text = (f"<u>Название</u>: {data['nameRu']}\n"
            f"<u>Название (ориг.)</u>: {'Отсутствует' if not data['nameOriginal'] else data['nameOriginal']}\n"
            f"<u>Описание</u>: {data['description']}\n"
            f"<u>Год выпуска</u>: {data['year']}\n"
            f"<u>Длительность</u>: {dur_hours}:{dur_minutes}\n"
            f"<u>Жанры</u>: {', '.join([item['genre'] for item in data['genres']])}\n"
            f"<u>Страны</u>: {', '.join([item['country'] for item in data['countries']])}\n"
            f"<u>Оценка на Kinopoisk</u>: {data['ratingKinopoisk']}\n"
            f"<u>Оценка на IMDB</u>: {data['ratingImdb']}")

    return text
