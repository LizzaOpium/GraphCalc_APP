import json
import os
import sys

# базовые настройки, вбиваются по дефолту
DEFAULTS = {
    'range_a': -20,
    'range_b': 20,
    'color_mode': 'all_different',
    'theme': 'dark',
    'window_width': 1100,
    'window_height': 680,
    'last_tab': 0,
}

def resource_path(relative_path): # иконка
    """
    Для режима разработки (IDE): в корне
    Для режима работы с файлом .exe: в директории с .exe-шником
    """
    if hasattr(sys, '_MEIPASS'):
        # в dist (рядом с .exe)
        return os.path.join(sys._MEIPASS, relative_path)
    else: # корень (рядом с main.py)
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', relative_path)

def get_config_path(): # конфиг-файл
    """
    Для режима разработки (IDE): в корне
    Для режима работы с файлом .exe: в директории с .exe-шником
    """
    if hasattr(sys, '_MEIPASS'):
        # в dist (рядом с .exe)
        return os.path.join(os.path.dirname(sys.executable), 'config.json')
    else:
        # корень (рядом с main.py)
        return os.path.join(os.path.dirname(__file__), '..', 'config.json')

# путь конфига
CONFIG_PATH = get_config_path()

# загрузка в словарь настроек
def load() -> dict: # функция возвращает -> словарь
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
            # слияние двух словарей: дата + дефолтные настройки
            return {**DEFAULTS, **data}
        except (json.JSONDecodeError, IOError): # IOError - ошибка записи файла
            pass
    return DEFAULTS.copy()

# сохранение конфига в новый словарь
def save(cfg: dict):
    to_save = {k: cfg[k] for k in DEFAULTS if k in cfg}
    try:
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            json.dump(to_save, f, indent=4, ensure_ascii=False)
    except IOError as e:
        print(f'Не удалось сохранить настройки: {e}')