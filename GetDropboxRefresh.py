from dropbox import DropboxOAuth2FlowNoRedirect
from utils.settings import settings

# Замените на свои значения из Dropbox App Console
APP_KEY = settings.dropbox_key
APP_SECRET = settings.dropbox_secret

# Настройка OAuth-потока
auth_flow = DropboxOAuth2FlowNoRedirect(APP_KEY, APP_SECRET, token_access_type='offline')

# Шаг 1: Получить URL для авторизации
authorize_url = auth_flow.start()
print("1. Перейдите по ссылке и авторизуйтесь:", authorize_url)
print("2. После авторизации скопируйте код из адресной строки.")

# Шаг 2: Ввести код авторизации
auth_code = input("Введите код авторизации: ").strip()

# Шаг 3: Получить access token и refresh token
try:
    result = auth_flow.finish(auth_code)
    print("\nAccess Token:", result.access_token)  # Временный (обычно на 4 часа)
    print("Refresh Token:", result.refresh_token)  # Долгоживущий (сохраните его!)
    print("Expires At:", result.expires_at)
except Exception as e:
    print("Ошибка:", e)