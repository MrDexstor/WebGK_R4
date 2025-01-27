import os

def generate_config():
    # Запрашиваем у пользователя необходимые значения
    develop_server_connect = input("Ваш сервер запущен на тестовой среде? (True/False): ").strip().lower() == 'true'
    bo_url_suffix = input("Введите номер ТОРГ (SAP) BackOffice (например, 'JH34'): ").strip()
    fs_dir_suffix = input("Введите имя для директории хранения файлов загрузок (например, 'uploads'): ").strip()

    # Создаем директорию для хранения файлов загрузок
    fs_dir_path = os.path.join(os.getcwd(), fs_dir_suffix)
    os.makedirs(fs_dir_path, exist_ok=True)

    # Формируем содержимое файла конфигурации
    config_content = f"""from WebGK.settings import BASE_DIR
# Настройки системы WebGK

# Режим локального тестового сервера
Develop_Server_Connect = {develop_server_connect}

# Ссылка на BackOffice
BO_Urls = 'http://bo-{bo_url_suffix}.x5.ru:8096'

# Дирректория для хранения файлов загрузок
FS_DIR = BASE_DIR / '{fs_dir_suffix}'

# Наименование рабочей сети WiFi
LAN_WIFI_SSID = '2xiaise3'

#ДАЛЕЕ НИЧЕГО НЕ МЕНЯЕМ!!!
# Обработчики настроек
def BO_Url():
    if Develop_Server_Connect:
        return 'http://127.0.0.1:8096'
    else:
        return BO_Urls
"""

    # Записываем содержимое в файл конфигурации
    with open('Core/config.py', 'w') as config_file:
        config_file.write(config_content)

    print("Файл конфигурации успешно создан.")
    print(f"Директория для хранения файлов загрузок успешно создана: {fs_dir_path}")

# Вызываем функцию для генерации конфигурации
generate_config()
