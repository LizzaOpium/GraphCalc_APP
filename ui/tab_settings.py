import customtkinter as ctk
from core.config import save

""" Вкладка настройки """
class TabSettings(ctk.CTkFrame):
    def __init__(self, parent, cfg: dict):
        super().__init__(parent, fg_color='transparent')
        self.cfg = cfg
        self._build_ui()

    # --- метод _build_ui -> строит интерфейс
    def _build_ui(self):
        inner = ctk.CTkFrame(self, width=400) # -> внутренний фрейм с фиксированной шириной
        inner.pack(anchor='n', padx=40, pady=30, fill='x')

        # --- заголовок ---
        ctk.CTkLabel(inner, text='Настройки', font=ctk.CTkFont(size=18, weight='bold'),
                     anchor='w').pack(fill='x', padx=16, pady=(16, 14))

        # --- диапазон по умолчанию ---
        ctk.CTkLabel(inner, text='Диапазон построения по умолчанию',
                     anchor='w').pack(fill='x', padx=16, pady=(0, 4))
        row = ctk.CTkFrame(inner, fg_color='transparent')
        row.pack(fill='x', padx=16, pady=(0, 12))
        ctk.CTkLabel(row, text='a =', width=28).pack(side='left')
        self.a_entry = ctk.CTkEntry(row, width=80)
        self.a_entry.insert(0, str(self.cfg['range_a']))
        self.a_entry.pack(side='left', padx=(4, 16))
        ctk.CTkLabel(row, text='b =', width=28).pack(side='left')
        self.b_entry = ctk.CTkEntry(row, width=80)
        self.b_entry.insert(0, str(self.cfg['range_b']))
        self.b_entry.pack(side='left', padx=4)

        # --- тема ---
        ctk.CTkLabel(inner, text='Тема оформления', anchor='w').pack(fill='x', padx=16, pady=(0, 4))
        self.theme_var = ctk.StringVar(value=self.cfg.get('theme', 'dark'))
        theme_row = ctk.CTkFrame(inner, fg_color='transparent')
        theme_row.pack(fill='x', padx=16, pady=(0, 12))
        for label, val in [('Тёмная', 'dark'), ('Светлая', 'light'), ('Системная', 'system')]:
            ctk.CTkRadioButton(theme_row, text=label, variable=self.theme_var,
                               value=val).pack(side='left', padx=(0, 16))

        # --- режим цвета графика с параметром ---
        ctk.CTkLabel(inner, text='Цвет графика с параметром',
                     anchor='w').pack(fill='x', padx=16, pady=(0, 4))
        self.color_var = ctk.StringVar(value=self.cfg.get('color_mode', 'all_different'))
        color_row = ctk.CTkFrame(inner, fg_color='transparent')
        color_row.pack(fill='x', padx=16, pady=(0, 20))
        ctk.CTkRadioButton(color_row, text='Все разные', variable=self.color_var,
                           value='all_different').pack(side='left', padx=(0, 16))
        ctk.CTkRadioButton(color_row, text='По значению параметра', variable=self.color_var,
                           value='by_parameter').pack(side='left')

        # --- кнопка сохранить ---
        self.save_btn = ctk.CTkButton(inner, text='💾 Сохранить', command=self._save)
        self.save_btn.pack(fill='x', padx=16, pady=(0, 8))

        self.status = ctk.CTkLabel(inner, text='', font=ctk.CTkFont(size=12), text_color='gray')
        self.status.pack(padx=16, pady=(0, 16))

    # метод _save -> передает данные из введенных настроек и сохраняет их в cfg
    def _save(self):
        # --- вывод ошибок ---
        try:
            a = float(self.a_entry.get())
            b = float(self.b_entry.get())
        except ValueError:
            self.status.configure(text='❌ Неверный формат диапазона', text_color='red')
            return
        if b <= a:
            self.status.configure(text='❌ b должно быть больше a', text_color='red')
            return

        # --- сохранение в cfg настроек ---
        self.cfg['range_a'] = a
        self.cfg['range_b'] = b
        self.cfg['theme'] = self.theme_var.get()
        self.cfg['color_mode'] = self.color_var.get()

        ctk.set_appearance_mode(self.cfg['theme'])
        save(self.cfg)
        self.status.configure(text='✅ Сохранено', text_color='green')