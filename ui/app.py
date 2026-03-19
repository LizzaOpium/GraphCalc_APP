# вместо базового Tkinter лучше использовать customtkinter
import os

import customtkinter as ctk
from core.config import load, save, resource_path
from ui.tab_graph import TabGraph
from ui.tab_info import TabInfo
from ui.tab_parameter import TabParameter
from ui.tab_dichotomy import TabDichotomy
from ui.tab_settings import TabSettings

# названия вкладок
TAB_NAMES = ['📊 График', '📈 Параметр', '↕️ Дихотомия', '⚙️ Настройки', 'ℹ️ Информация']


""" Создание класса App, т.е. системного окна """
class App(ctk.CTk):
    # вызов ctk.CTk
    def __init__(self):
        # инициализация окна
        super().__init__()
        # чтение настроек с диска, из config.json подгружается конфиг, который уже дальше применяется в CTk
        self.cfg = load()

        ctk.set_appearance_mode(self.cfg.get('theme', 'dark')) # применение темы, если нет - берем 'dark'
        ctk.set_default_color_theme('blue') # базовая тема

        self.title('GraphCalc') # название окна приложения
        self.geometry(f'{self.cfg["window_width"]}x{self.cfg["window_height"]}') # размер окна из конфиг-файла
        self.minsize(800, 520) # минимальный размер окна

        # создаем вкладки через CTKTabview
        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(fill='both', expand=True, padx=8, pady=8)

        # создаем вкладки по именам
        for name in TAB_NAMES:
            self.tabs.add(name)

        # содержимое для вкладок
        TabGraph(self.tabs.tab('📊 График'), self.cfg).pack(fill='both', expand=True)
        TabParameter(self.tabs.tab('📈 Параметр'), self.cfg).pack(fill='both', expand=True)
        TabDichotomy(self.tabs.tab('↕️ Дихотомия'), self.cfg).pack(fill='both', expand=True)
        TabSettings(self.tabs.tab('⚙️ Настройки'), self.cfg).pack(fill='both', expand=True)
        TabInfo(self.tabs.tab('ℹ️ Информация'), self.cfg).pack(fill='both', expand=True)

        try:
            self.tabs.set(TAB_NAMES[self.cfg.get('last_tab', 0)])
        except Exception:
            pass # ошибка -> приложение открывает пустую вкладку

        # закрытие окна при вызове метода _on_close
        self.protocol('WM_DELETE_WINDOW', self._on_close)

    def _set_icon(self):
        icon = resource_path('assets/GRAPH2.ico')
        if os.path.exists(icon):
            self.wm_iconbitmap(icon) # иконка процесса

    # закрытие окна, с сохранением последних параметров
    def _on_close(self):
        self.cfg['window_width'] = self.winfo_width()
        self.cfg['window_height'] = self.winfo_height()
        try:
            self.cfg['last_tab'] = TAB_NAMES.index(self.tabs.get())
        except ValueError:
            pass # для неопределенной вкладки не обновляем конфиг

        # сохранение конфига + полный выход
        save(self.cfg)
        self.destroy()