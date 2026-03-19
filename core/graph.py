import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import re

# --- логарифм по основанию base ---
def make_logn(base):
    return lambda x: np.log(x) / np.log(base)

# --- получение словаря ---
def get_dict(x, expression=''):
    bases = re.findall(r'log(\d+\.?\d*)', expression)
    extra = {f'log{i}': make_logn(float(i)) for i in bases}
    return {
        'x': x, 'X': x,
        'sin': np.sin, 'cos': np.cos, 'tan': np.tan,
        'exp': np.exp, 'log': np.log, 'sqrt': np.sqrt,
        'abs': np.abs, 'pi': np.pi, 'e': np.e, 'a': 0,
        **extra
    }

# --- перевод синтаксиса ---
def parse(expr):
    # игнорирование регистра
    for fn in ['sin', 'cos', 'tan', 'exp', 'sqrt', 'abs', 'ln', 'log']:
        expr = re.sub(fn, fn, expr, flags=re.IGNORECASE)
    # исправление степени
    expr = expr.replace('^', '**')
    # исправление регистра x, a
    expr = expr.replace('X', 'x')
    expr = expr.replace('A', 'a')
    # исправление дробной части
    expr = expr.replace(',', '.')
    # исправление модуля
    expr = re.sub(r'\|([^|]+)\|', r'abs(\1)', expr)
    # исправление логарифма (промежуточное)
    expr = expr.replace('ln(', 'log(')
    expr = re.sub(r'log(\d+\.?\d*)\(', r'LOGN_\1_(', expr)
    expr = re.sub(r'(\d\.?\d*)(LOGN_)', r'\1*\2', expr)
    # исправление произведения
    expr = re.sub(r'(\d)(a)(?![a-z])', r'\1*\2', expr)
    expr = re.sub(r'(\d)(x)', r'\1*\2', expr)
    expr = re.sub(r'(a)(x)', r'\1*\2', expr)
    expr = re.sub(r'(\d\.?\d*)(sin|cos|tan|exp|log|sqrt|abs)', r'\1*\2', expr)
    expr = re.sub(r'(\d)\(', r'\1*(', expr)
    # исправление логарифма (окончательное)
    expr = re.sub(r'LOGN_(\d+\.?\d*)_\(', r'log\1(', expr)
    return expr

# --- глобальные переменные модуля ---
func = 'x'
c = None

# перевод функции из строки - в собственно функцию (по словарю)
def function(x):
    try:
        return eval(func, get_dict(x, func))
    except:
        return np.nan

"""валидация функции (нахождения значения функции)"""
def validate(expression):
    try:
        parsed = parse(expression)
        result = eval(parsed.lower(), get_dict(1.0, parsed) | {'a': 1.0})
        if not isinstance(result, (int, float, np.floating)):
            return False
        return True
    except:
        return False

def build_axes(ax):
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.axhline(y=0, color='black', linewidth=1)
    ax.axvline(x=0, color='black', linewidth=1)
    ax.grid(True, alpha=0.3)

def compute_y(x_arr):
    y = []
    for xi in x_arr:
        try:
            y.append(float(np.real(function(xi))))
        except:
            y.append(np.nan)
    return np.array(y, dtype=float)

#===ДИХОТОМИЯ===========================================================================================================

def dichotomy(a, b, mode='max'):
    global c
    eps = 1e-6
    r = eps / 2

    if a > b:
        c = None
        return '❌ Ошибка: интервал задан некорректно.\na должно быть меньше b'
    if a == b:
        c = None
        return '❌ Ошибка: интервал задан двумя совпадающими точками.'
    if np.isnan(function(a)) and np.isnan(function(b)):
        c = None
        return f'❌ Ошибка: функция не определена на отрезке ({a}; {b})'

    segments = 1000
    step = (b - a) / segments
    best_c = None
    best_val = float('-inf') if mode == 'max' else float('inf')

    for i in range(segments):
        seg_a = a + i * step
        seg_b = seg_a + step

        if np.isnan(function(seg_a)) and np.isnan(function(seg_b)):
            continue

        local_a, local_b = seg_a, seg_b
        while abs(local_b - local_a) > eps:
            mid = (local_a + local_b) / 2
            if mode == 'max':
                if function(mid - r) > function(mid + r):
                    local_b = mid
                else:
                    local_a = mid
            else:
                if function(mid - r) < function(mid + r):
                    local_b = mid
                else:
                    local_a = mid

        local_c = (local_a + local_b) / 2
        local_val = function(local_c)

        if np.isnan(local_val) or np.isinf(local_val):
            continue

        if mode == 'max' and local_val > best_val:
            best_val = local_val
            best_c = local_c
        elif mode == 'min' and local_val < best_val:
            best_val = local_val
            best_c = local_c

    c = best_c
    if c is None:
        label = 'максимум' if mode == 'max' else 'минимум'
        return f'❌ Ошибка: не удалось найти {label} на отрезке ({a}; {b})'

    label = 'x_max' if mode == 'max' else 'x_min'
    return f'f({label}) = {round(function(c), 4)},  {label} = {round(c, 4)}'

#===ГРАФИКИ=============================================================================================================

""" График + отметка прямыми максимума/минимума """
def graph(ax, a, b):
    if c is None:
        return

    x = np.linspace(a, b, 1000)
    y = compute_y(x)

    ax.clear()
    build_axes(ax)

    fc = function(c)
    if np.isfinite(fc):
        ax.axhline(y=fc, color='blue', linestyle='--', linewidth=0.8)
    ax.axvline(x=c, color='blue', linestyle='--', linewidth=0.8)
    ax.plot(x, y, label='f(x)', color='red', linestyle='solid')
    ax.set_title('График f(x)')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_xlim(a, b)
    ax.autoscale(axis='y')
    ax.legend(fontsize=8)


""" Простой график """
def simple_graph(ax, a, b):
    x = np.linspace(a, b, 1000)
    y = compute_y(x)

    ax.clear()
    build_axes(ax)

    ax.plot(x, y, label='f(x)', color='red', linestyle='solid')
    ax.set_title('График f(x)')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_xlim(a, b)
    ax.autoscale(axis='y')
    ax.legend(fontsize=8)

""" График с параметром """
def parameter_graph(ax, color_mode, functions, x_a, x_b):
    global func

    x = np.linspace(x_a, x_b, 1000)

    ax.clear()
    build_axes(ax)

    palette = plt.cm.tab10.colors
    color_index = 0

    if color_mode == 'by_parameter':
        all_params = []
        for fn_data in functions:
            for a_val in fn_data['params']:
                if a_val not in all_params:
                    all_params.append(a_val)
        colors = {a_val: palette[idx % len(palette)] for idx, a_val in enumerate(all_params)}

    for fn_data in functions:
        fn = fn_data['func']
        params = fn_data['params']
        func = fn

        for a_val in params:
            y = []
            for xi in x:
                try:
                    d = get_dict(xi, fn)
                    if a_val is not None:
                        d['a'] = a_val
                    result = eval(fn, d)
                    y.append(float(np.real(result)))
                except:
                    y.append(np.nan)

            y = np.array(y, dtype=float)

            label = f'f(x, {a_val})' if a_val is not None else 'f(x)'

            if color_mode == 'by_parameter':
                color = colors[a_val]
            else:
                color = palette[color_index % len(palette)]

            ax.plot(x, y, label=label, color=color)
            color_index += 1

    ax.set_xlim(x_a, x_b)
    ax.autoscale(axis='y')
    ax.legend(fontsize=8)
    ax.set_xlabel('x')
    ax.set_ylabel('y')