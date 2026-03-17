import threading
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import core.graph as gm
from core.graph import parse, validate, parameter_graph

""" Вкладка график с параметром """
class TabParameter(ctk.CTkFrame):
    def __init__(self, parent, cfg: dict):
        super().__init__(parent, fg_color='transparent')
        self.cfg = cfg
        self.functions = []
        self.param_a = None
        self.param_b = None
        self._build_ui()

    def _build_ui(self):
        # === ЛЕВАЯ ПАНЕЛЬ ===
        panel = ctk.CTkFrame(self, width=270)
        panel.pack(side='left', fill='y', padx=(10, 4), pady=10)
        panel.pack_propagate(False)

        # --- поле ввода функции ---
        ctk.CTkLabel(panel, text='f(x, a) =', anchor='w').pack(fill='x', padx=12, pady=(18, 2))
        self.func_entry = ctk.CTkEntry(panel, placeholder_text='a*sin(x)')
        self.func_entry.pack(fill='x', padx=12, pady=(0, 6))

        # --- поле ввода значений параметра ---
        ctk.CTkLabel(panel, text='Значения параметра a:', anchor='w').pack(fill='x', padx=12, pady=(0, 2))
        self.params_entry = ctk.CTkEntry(panel, placeholder_text='0.5 1 2 3')
        self.params_entry.pack(fill='x', padx=12, pady=(0, 10))

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

        # --- кнопка для добавления графика + очистка ---
        btn_row = ctk.CTkFrame(panel, fg_color='transparent')
        btn_row.pack(fill='x', padx=12, pady=(6, 4))
        self.add_btn = ctk.CTkButton(btn_row, text='➕ Добавить', command=self._add_function)
        self.add_btn.pack(side='left', expand=True, fill='x', padx=(0, 4))
        self.clear_btn = ctk.CTkButton(btn_row, text='🗑 Очистить',
                                       fg_color='gray40', hover_color='gray30',
                                       command=self._clear)
        self.clear_btn.pack(side='left', expand=True, fill='x')

        # --- кнопка построить ---
        self.build_btn = ctk.CTkButton(panel, text='📊 Построить', command=self._build)
        self.build_btn.pack(fill='x', padx=12, pady=(4, 4))

        # --- сброс вида просмотра графика ---
        self.reset_btn = ctk.CTkButton(panel, text='🏠 Сбросить вид',
                                       fg_color='gray40', hover_color='gray30',
                                       command=self._reset_view)
        self.reset_btn.pack(fill='x', padx=12, pady=(0, 8))

        # --- вывод добавленных функций ---
        ctk.CTkLabel(panel, text='Добавлено:', anchor='w').pack(fill='x', padx=12, pady=(4, 2))
        self.list_box = ctk.CTkScrollableFrame(panel, height=120)
        self.list_box.pack(fill='x', padx=12, pady=(0, 6))

        self.status = ctk.CTkLabel(panel, text='', wraplength=240,
                                   font=ctk.CTkFont(size=12), text_color='gray')
        self.status.pack(padx=12, pady=4)

        # === ПРАВАЯ ПАНЕЛЬ ===
        graph_frame = ctk.CTkFrame(self)
        graph_frame.pack(side='right', fill='both', expand=True, padx=(4, 10), pady=10)

        self.fig, self.ax = plt.subplots(figsize=(6, 5), tight_layout=True)
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

        self.toolbar = NavigationToolbar2Tk(self.canvas, graph_frame)
        self.toolbar.update()

    # метод _add_function -> отдает переменные для дальнейшего построения
    def _add_function(self):
        func_raw = self.func_entry.get().strip()
        params_raw = self.params_entry.get().strip()
        # --- вывод ошибок ---
        if not func_raw:
            self._set_status('⚠ Введите функцию', 'orange')
            return
        if not validate(func_raw):
            self._set_status('❌ Синтаксическая ошибка', 'red')
            return

        # отрезок берём один раз — при добавлении первой функции
        if not self.functions:
            try:
                self.param_a = float(self.a_entry.get())
                self.param_b = float(self.b_entry.get())
            except ValueError:
                self._set_status('❌ Неверный формат отрезка', 'red')
                return
            if self.param_b <= self.param_a:
                self._set_status('❌ b должно быть больше a', 'red')
                return

        if 'a' in func_raw and params_raw:
            try:
                params = list(set(float(p) for p in params_raw.split()))
                if not params:
                    raise ValueError
            except ValueError:
                self._set_status('❌ Неверный формат параметров', 'red')
                return
        else:
            params = [None]

        self.functions.append({
            'func': parse(func_raw),
            'func_raw': func_raw,
            'params': params
        })
        self._refresh_list()
        self._set_status(f'✅ Добавлено: {len(self.functions)} функц.', 'green')

    # метод _refresh_list -> перезапись всех добавленных функций в list_box
    def _refresh_list(self):
        # winfo_children() -> список всех дочерних виджетов фрейма
        for w in self.list_box.winfo_children():
            w.destroy() # удаляет виджет из памяти и экрана
        for fn in self.functions:
            if fn['params'] == [None]: # при отсутствии параметров
                text = f"• {fn['func_raw']}"
            else: # при наличии параметров
                text = f"• {fn['func_raw']}  |  a = {', '.join(str(p) for p in fn['params'])}"
            ctk.CTkLabel(self.list_box, text=text, anchor='w',
                         font=ctk.CTkFont(size=12)).pack(fill='x', pady=1)

    # метод _clear -> очистка списка функций
    def _clear(self):
        self.functions = []
        self.param_a = None
        self.param_b = None
        self._refresh_list()
        self._set_status('Список очищен', 'gray')

    # метод _build -> построение функции/-ий
    def _build(self):
        if not self.functions:
            self._set_status('⚠ Сначала добавьте функции', 'orange')
            return

        color_mode = self.cfg.get('color_mode', 'all_different')
        a, b = self.param_a, self.param_b

        self._set_status('⏳ Строю...', 'gray')
        self.build_btn.configure(state='disabled')

        def worker():
            try:
                parameter_graph(self.ax, color_mode, self.functions, a, b)
                self.canvas.draw()
                self.toolbar.update()
                self._set_status('✅ Готово', 'green')
            except Exception as e:
                self._set_status(f'❌ {e}', 'red')
            finally:
                self.build_btn.configure(state='normal')

        threading.Thread(target=worker, daemon=True).start()

    def _reset_view(self):
        self.toolbar.home()

    def _set_status(self, text, color='gray'):
        self.status.configure(text=text, text_color=color)