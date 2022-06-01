from config.config import BASE_URL


suffixes = {
    "movies_top": "v2.2/films/top",
}


def get_api_url(func_name):
    result = BASE_URL + suffixes[func_name]
    return result
