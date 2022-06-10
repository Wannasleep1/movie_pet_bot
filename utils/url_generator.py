from config.config import BASE_URL


suffixes = {
    "movies_top": "v2.2/films/top",
    "premieres": "v2.2/films/premieres",
    "base": "v2.2/films/",
    "countries_genres": "v2.2/films/filters",
}


def get_api_url(func_name, id_=None):
    result = BASE_URL + suffixes[func_name]
    if id_:
        result += id_
    return result
