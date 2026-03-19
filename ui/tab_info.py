import customtkinter as ctk

APP_VERSION = '1.0.1'
APP_AUTOR = 'Alexey Popov AKA Onemoretime'

class TabInfo(ctk.CTkFrame):
    def __init__(self, parent, cfg: dict):
        super().__init__(parent, fg_color='transparent')
        self.cfg = cfg
        self._build_ui()

    def _build_ui(self):
        # --- скроллбар ---
        scroll = ctk.CTkScrollableFrame(self)
        scroll.pack(fill = 'both', expand=True, padx=10, pady=10)

        # === НАСТРОЙКИ ПОЛОЖЕНИЯ ТЕКСТА ===

        # --- заголовок ---
        def heading(content):
            ctk.CTkLabel(
                scroll, text = content,
                font = ctk.CTkFont(size = 15, weight = 'bold'),
                anchor = 'w'
            ).pack(fill = 'x', padx = 16, pady = (20, 6))

        # --- обычный текст ---
        def text(content, color=None, bold=False, italic=False):
            weight = 'bold' if bold else 'normal'
            slant = 'italic' if italic else 'roman'
            lbl = ctk.CTkLabel(
                scroll, text=content,
                font=ctk.CTkFont(size=13, weight=weight, slant=slant),
                anchor='w', justify='left',
                wraplength=700
            )
            if color:
                lbl.configure(text_color=color)
            lbl.pack(fill='x', padx=16, pady=(0, 4))

        # --- таблица с колонками ---
        def table(rows: list, col1='Ввод', col2='Описание', col1_width=220):
            frame = ctk.CTkFrame(scroll, fg_color='transparent')
            frame.pack(fill='x', padx=16, pady=(4, 10))

            # --- вывод заголовка ---
            header = ctk.CTkFrame(frame, fg_color=('gray75', 'gray28'))
            header.pack(fill='x')
            ctk.CTkLabel(
                header, text=col1,
                font=ctk.CTkFont(size=12, weight='bold'),
                width=col1_width, anchor='w'
            ).pack(side='left', padx=10, pady=5)
            ctk.CTkLabel(
                header, text=col2,
                font=ctk.CTkFont(size=12, weight='bold'),
                anchor='w'
            ).pack(side='left', padx=10, pady=5)

            # --- строки с чередующимся фоном ---
            for idx, (left, right) in enumerate(rows):
                bg = ('gray88', 'gray22') if idx % 2 == 0 else ('gray93', 'gray19')
                row_f = ctk.CTkFrame(frame, fg_color=bg)
                row_f.pack(fill='x')
                ctk.CTkLabel(
                    row_f, text=left,
                    font=ctk.CTkFont(family='Courier', size=12),
                    width=col1_width, anchor='w'
                ).pack(side='left', padx=10, pady=4)
                ctk.CTkLabel(
                    row_f, text=right,
                    font=ctk.CTkFont(size=12),
                    anchor='w', justify='left',
                    wraplength=460
                ).pack(side='left', padx=10, pady=4)

        # --- горизонтальная линия, граница секции ---
        def divider():
            ctk.CTkFrame(scroll, height=1, fg_color='gray35').pack(
                fill='x', padx=16, pady=(10, 0))

        # === ИНФОРМАЦИЯ ПО ПРОГРАММЕ ===

        ctk.CTkLabel(
            scroll, text='GraphCalc',
            font=ctk.CTkFont(size=24, weight='bold'),
            anchor='w'
        ).pack(fill='x', padx=16, pady=(18, 2))

        ctk.CTkLabel(
            scroll, text=f'Версия {APP_VERSION}',
            font=ctk.CTkFont(size=12),
            text_color='gray', anchor='w'
        ).pack(fill='x', padx=16, pady=(0, 6))

        ctk.CTkLabel(
            scroll, text=f'Автор {APP_AUTOR}',
            font=ctk.CTkFont(size=12),
            text_color='gray', anchor='w'
        ).pack(fill='x', padx=16, pady=(0, 6))

        text('Приложение для построения графиков математических функций, '
             'семейств кривых с параметром и поиска экстремумов методом дихотомии.', italic=True)

        divider()

        # === СИНТАКСИС ===

        heading('Синтаксис ввода функций')

        text('▶ Операции:')
        text('формат ввода', italic=True)
        table([
            ('x^2  или  x**2', 'возведение степень'),
            ('2f(x) или 2*f(x),', 'умножение'),
            ('|x|', 'модуль'),
            ('3,14 или 3.14', 'запятая или точка как десятичный разделитель'),
            ('Sin(x), COS(x)', 'регистр не важен'),
        ])

        text('▶ Функции:')
        table([
            ('sin(x), cos(x), tan(x)', 'тригонометрия'),
            ('sqrt(x)', 'квадратный корень √x'),
            ('ln(x)  или  log(x)', 'натуральный логарифм'),
            ('logN(x)', 'логарифм по любому основанию N от x'),
            ('exp(x)', 'экспонента  eˣ'),
            ('pi', 'константа  π ≈ 3.14159'),
            ('e', 'константа  e ≈ 2.71828'),
        ])

        text('▶ Параметр:')
        table([
            ('a', 'свободный параметр, во вкладке График будет определен как 0'),
            ('2a', 'число перед a, автоматически определяется как 2*a'),
            ('a*x', 'явное умножение - тоже работает'),
        ])

        divider()

        # === ПРИМЕРЫ ===

        heading('Примеры выражений')

        text('▶ Примеры для выражений без параметра: f(x)')

        table([
            ('sin(x)', 'синус'),
            ('cos(x) + sin(x)', 'сумма синуса и косинуса'),
            ('x^2 - 3x + 2', 'парабола'),
            ('|x|', 'модуль'),
            ('1/x', 'гипербола'),
            ('sqrt(x)', 'квадратный корень'),
            ('exp(-x^2)', 'колокол Гаусса'),
            ('ln(x)', 'натуральный логарифм'),
            ('log2(x)', 'логарифм по основанию 2'),
            ('sin(x)/x', 'sinc-функция - кардинальный синус'),
            ('x^3 - 3x', 'кубическая'),
            ('|x^2 - 4|', 'модуль параболы'),
        ], col1='Выражение', col2='Что строит', col1_width=200)

        text('▶ Примеры с параметром: f(x, a) (ввод значений - через пробел: 0 1 2 3):')

        table([
            ('a*sin(x)', 'синус с разной амплитудой'),
            ('sin(a*x)', 'синус с разной частотой'),
            ('x^2 + a', 'парабола со сдвигом по Y'),
            ('(x-a)^2', 'парабола со сдвигом по X'),
            ('a*x', 'прямые с разным наклоном'),
            ('exp(-a*x^2)', 'Гауссова функция'),
        ], col1='Выражение', col2='Что строит', col1_width=200)

        ctk.CTkLabel(
            scroll, text=f'• Сделано специально для проекта ученика ГБОУ МО СП ФМЛ Попова Алексея Евгеньевича',
            font=ctk.CTkFont(size=12, slant='italic'),
            text_color='gray', anchor='w'
        ).pack(fill='x', padx=16, pady=(0, 6))

        # нижний отступ
        ctk.CTkLabel(scroll, text='').pack(pady=8)

