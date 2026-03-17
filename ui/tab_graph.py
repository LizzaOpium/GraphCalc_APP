import threading
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import core.graph as gm
from core.graph import parse, validate, simple_graph

""" Вкладка график """
class TabGraph(ctk.CTkFrame):
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
        self.func_entry = ctk.CTkEntry(panel, placeholder_text='sin(x)')
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

        # --- кнопка построить ---
        self.build_btn = ctk.CTkButton(panel, text='📊 Построить', command=self._build)
        self.build_btn.pack(fill='x', padx=12, pady=(10, 4))

        # кнопка сброса вида, возвращает исходный масштаб для просмотра графика
        self.reset_btn = ctk.CTkButton(panel, text='🏠 Сбросить вид',
                                       fg_color='gray40', hover_color='gray30',
                                       command=self._reset_view)
        self.reset_btn.pack(fill='x', padx=12, pady=(0, 4))

        self.status = ctk.CTkLabel(panel, text='', wraplength=210,
                                   font=ctk.CTkFont(size=12), text_color='gray')
        self.status.pack(padx=12, pady=6)

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

    # метод _build -> отдает переменные для дальнейшего построения
    def _build(self):
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

        self._set_status('⏳ Строю...', 'gray')
        self.build_btn.configure(state='disabled')

        def worker():
            try:
                gm.func = parse(func_raw)
                simple_graph(self.ax, a, b)
                self.canvas.draw()
                self.toolbar.update()  # сбрасываем историю навигации после нового построения
                self._set_status('✅ Готово', 'green')
            except Exception as e:
                self._set_status(f'❌ {e}', 'red')
            finally:
                self.build_btn.configure(state='normal')

        # подключение параллельных вычислений (для многоядерных процессоров)
        threading.Thread(target=worker, daemon=True).start()

    def _reset_view(self):
        self.toolbar.home()

    def _set_status(self, text, color='gray'):
        self.status.configure(text=text, text_color=color)