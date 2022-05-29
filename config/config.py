from environs import Env

env = Env()
env.read_env()

TOKEN = env.str('TOKEN')
API_KEY = env.str('API_KEY')
ADMINS = env.list('ADMINS', delimeter=',')
BASE_URL = "https://kinopoiskapiunofficial.tech/api/"
HEADERS = {
    "X-API-KEY": API_KEY,
}