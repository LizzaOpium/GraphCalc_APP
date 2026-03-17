import threading
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import core.graph as gm
from core.graph import parse, validate, dichotomy, graph


""" Вкладка дихотомия """
class TabDichotomy(ctk.CTkFrame):

    # инициализация
    def __init__(self, parent, cfg: dict):
        super().__init__(parent, fg_color='transparent')
        self.cfg = cfg
        self._build_ui()

    def _build_ui(self):

        # === ЛЕВАЯ ПАНЕЛЬ ===
        panel = ctk.CTkFrame(self, width=240)
        panel.pack(side='left', fill='y', padx=(10, 4), pady=10)
        panel.pack_propagate(False)

        # --- поле ввода функции ---
        ctk.CTkLabel(panel, text='f(x) =', anchor='w').pack(fill='x', padx=12, pady=(18, 2))
        self.func_entry = ctk.CTkEntry(panel, placeholder_text='x^3 - 3*x')
        self.func_entry.pack(fill='x', padx=12, pady=(0, 10))

        # --- поле ввода отрезка ---
        ctk.CTkLabel(panel, text='Отрезок [a; b]', anchor='w').pack(fill='x', padx=12, pady=(0, 2))
        row = ctk.CTkFrame(panel, fg_color='transparent')
        row.pack(fill='x', padx=12, pady=(0, 10))
        self.a_entry = ctk.CTkEntry(row, placeholder_text='a', width=80)
        self.a_entry.insert(0, str(self.cfg['range_a']))
        self.a_entry.pack(side='left', padx=(0, 6))
        self.b_entry = ctk.CTkEntry(row, placeholder_text='b', width=80)
        self.b_entry.insert(0, str(self.cfg['range_b']))
        self.b_entry.pack(side='left')

        # --- кнопки максимум/минимум ---
        btn_row = ctk.CTkFrame(panel, fg_color='transparent')
        btn_row.pack(fill='x', padx=12, pady=(10, 4))
        self.max_btn = ctk.CTkButton(btn_row, text='⬆ Max',
                                     command=lambda: self._calc('max'))
        self.max_btn.pack(side='left', expand=True, fill='x', padx=(0, 4))
        self.min_btn = ctk.CTkButton(btn_row, text='⬇ Min',
                                     command=lambda: self._calc('min'))
        self.min_btn.pack(side='left', expand=True, fill='x')

        # --- кнопка сброса вида ---
        self.reset_btn = ctk.CTkButton(panel, text='🏠 Сбросить вид',
                                       fg_color='gray40', hover_color='gray30',
                                       command=self._reset_view)
        self.reset_btn.pack(fill='x', padx=12, pady=(0, 10))

        # --- вывод результата дихотомии ---
        ctk.CTkLabel(panel, text='Результат:', anchor='w').pack(fill='x', padx=12, pady=(4, 2))
        self.result_label = ctk.CTkLabel(
            panel, text='—',
            wraplength=210,
            font=ctk.CTkFont(family='Courier', size=13),
            anchor='w', justify='left'
        )
        self.result_label.pack(fill='x', padx=12, pady=(0, 6))

        self.status = ctk.CTkLabel(panel, text='', wraplength=210,
                                   font=ctk.CTkFont(size=12), text_color='gray')
        self.status.pack(padx=12, pady=4)

        # === ПРАВАЯ ПАНЕЛЬ ===
        graph_frame = ctk.CTkFrame(self)
        graph_frame.pack(side='right', fill='both', expand=True, padx=(4, 10), pady=10)

        # --- окно Matplotlib ---
        self.fig, self.ax = plt.subplots(figsize=(6, 5), tight_layout=True)
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

        # --- установка базового тулбара Matplotlib ---
        self.toolbar = NavigationToolbar2Tk(self.canvas, graph_frame)
        self.toolbar.update()

    # метод _calc вызывается при нажатии кнопки max/min, отдает в mode -> max / min
    def _calc(self, mode: str):
        func_raw = self.func_entry.get().strip()
        # --- вывод ошибок ---
        if not func_raw:
            self._set_status('⚠ Введите функцию', 'orange')
            return
        if not validate(func_raw):
            self._set_status('❌ Синтаксическая ошибка', 'red')
            return
        try:
            a = float(self.a_entry.get())
            b = float(self.b_entry.get())
        except ValueError:
            self._set_status('❌ Неверный формат отрезка', 'red')
            return
        if b <= a:
            self._set_status('❌ b должно быть больше a', 'red')
            return

        self._set_status('⏳ Считаю...', 'gray') # статус, чем занимается программа
        for btn in (self.max_btn, self.min_btn):
            btn.configure(state='disabled')

        # функция, работа дихотомии
        def worker():
            try:
                gm.func = parse(func_raw) # обработанная функция -> модуль graph
                result = dichotomy(a, b, mode=mode) # выполнение дихотомии -> result
                self.result_label.configure(text=result)
                if gm.c is not None:
                    # если дихотомия отработала -> рисует пунктиром отметку максимума/минимума
                    graph(self.ax, a, b)
                    self.canvas.draw()
                    self.toolbar.update()
                self._set_status('✅ Готово', 'green')
            except Exception as e:
                self._set_status(f'❌ {e}', 'red')
            finally:
                # разблокировка обеих кнопок, базовое состояние
                for btn in (self.max_btn, self.min_btn):
                    btn.configure(state='normal')

        # подключение параллельных вычислений (для многоядерных процессоров)
        threading.Thread(target=worker, daemon=True).start()

    def _reset_view(self):
        self.toolbar.home()

    def _set_status(self, text, color='gray'):
        self.status.configure(text=text, text_color=color)