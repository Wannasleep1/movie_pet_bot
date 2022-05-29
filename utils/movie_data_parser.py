def movie_data_parser(data, page):
    result = ""
    elem_num = (page-1) * 20 + 1
    for elem in data:
        string = (f"{elem_num}. ID: {elem['filmId']}; "
                  f"Название: {elem['nameRu']}; "
                  f"Год выпуска: {elem['year']}; "
                  f"Жанры: {', '.join([item['genre'] for item in elem['genres']])}; "
                  f"Длительность: {elem['filmLength']}\n\n")
        result += string
        elem_num += 1

    return result

