import numpy as np
import sys
from shutil import rmtree
from os import mkdir
from IPython.display import clear_output
from tqdm import tqdm
from re import search
import re
import importlib

class Task:
  def __init__(self, alias):
    self.alias = alias
    self.result = False
    self.error = set()
  
  def check_patt(self, pat, t):
    ret1 = {}
    for name in t.keys():
      ret1[name] = pat - set([p for p in pat if search(p, t[name])])
    return ret1

  def check_task(self, text):
    if self.alias:
      patterns = set(self.alias.keys())
      n_pat = len(patterns)
      ret = self.check_patt(patterns, text)
    else:
      ret = {name: set() for name in text.keys()}
    # print(ret)
    error = self.error
    for name in tqdm(text.keys(), desc='Проверка ячеек ', bar_format='{l_bar}{bar}  {n_fmt}/{total_fmt}'):
      jump = True
      print(ret[name])
      try:
        print(f'\nЯчейка \n\n{text[name]}')
        tmp_imp = importlib.import_module(name[:-3])
        if not ret[name]:
          try:
            self.run(tmp_imp, text[name])
            # print('\n Это правильное решение')
            self.result = True
          except ValueError as v:
            error.add(f'\n\nПопытка подачи неправильного значения {v}')
          except UnboundLocalError:
            error.add(f'\n\nИспользование переменной перед приравниванием')
          except TypeError as t:
            error.add(f'\n\nНеправильное использование типов данных: \n{t}')
          except NameError as n:
            # er = sys.exc_info()
            error.add(f'\n\nИспользование неправильного идентификатора: \n{n}')
          except AssertionError as a:
            error.add(f'\n\nОшибка кода: {a}')
          except Exception as e:
            error.add(str(e)+str(type(e)))
        else:
            error.add('\n\nНе использована необходимая функция '+f'{", ".join([self.alias[key] for key in ret[name]])}')
      except IndentationError:
        error.add(f'\n\nНеправильный отступ')
        jump = False
      except NameError as n1:
        jump = False
        error.add(f'\n\nЯчейка не содержит определения необходимой функции: \n{n1}')
      except AssertionError as a:
        error.add(f'\n\nОшибка кода: {a}')
        jump = False
      except SyntaxError:
        error.add(f'\n\nСинтаксическая ошибка')
        jump = False
      except ValueError:
        error.add(f'\n\nИспользовано неправильное значение')
        jump = False
      except AttributeError:
        error.add(f'\n\nИспользован неизвестный метод')
        jump = False
      if jump:
        del sys.modules[tmp_imp.__name__]
      print()
      print(self.error)
    print('\n\nЗадание выполнено' if self.result else '\n\n Задание не выполнено. Попробуйте снова')
    return self.result

class Task1(Task):
  def run(self, tmp, text):
    a1 = np.random.randint(1, 11, size=10)
    a2 = np.random.randint(1, 11, size=4)
    result = np.in1d(a1, a2)
    assert (tmp.check_arrays(a1, a2) == result).all(), 'Неправильный результат'
    assert len(tmp.check_arrays(a1, a2)) == 10, 'Неправильная длина результата'

class Task2(Task):
  def run(self, tmp, text):
    a1 = (2, 6)
    a2 = (-2, 6)
    result1 = (6.324555320336759, 1.2490457723982544)
    result2 = (6.324555320336759, 1.8925468811915387)
    assert tmp.find_angle(a1) == result1, 'Неправильный результат'
    assert tmp.find_angle(a2) == result2, 'Неправильный результат'
    assert len(tmp.find_angle(a1)) == 2, 'Неправильная длина результата'


class Task3(Task):
  def run(self, tmp, text):
    res = np.array([[1, 0, 0, 1, 0, 0, 1],
                  [0, 1, 0, 1, 0, 1, 0],
                  [0, 0, 1, 1, 1, 0, 0],
                  [1, 1, 1, 1, 1, 1, 1],
                  [0, 0, 1, 1, 1, 0, 0],
                  [0, 1, 0, 1, 0, 1, 0],
                  [1, 0, 0, 1, 0, 0, 1]])
    assert (tmp.my_array == res).all(), 'Неправильный результат'

class Task4(Task):
  def run(self, tmp, text):
    lang_list = ['Java', 'Python', 'PHP', 'JavaScript', 'C#', 'C++']
    assert tmp.programmingLanguages == lang_list, 'Неправильный список языков'
    assert len(tmp.popuratity) == 6, 'Неверная длина списка значений'
    assert len(tmp.colors) == 6, "Неверная длина списков цветов"

class Task5(Task):
  def run(self, tmp, text):
    assert tmp.x.max() < 101 or tmp.x.min() > -101, 'Неправильный отрезок значений'
    assert re.findall(r'\.plot\(.*=?x.*linestyle\s*=.*label\s*=', text) != 2, 'Неправильное число графиков'

def save_cells(cnt):
  text = {}
  ad = len((cnt[:-1])
  i = False
  s = 'import matplotlib.pyplot as plt\nimport numpy as np\n\n'
  for num, item in enumerate(cnt[:-1]):
    if item == '':
      continue
    text[f'tmp{num}.py'] = item
    with open(f'/content/tmp/tmp{num}.py', mode='w', encoding='utf8') as f:
      f.write('import matplotlib.pyplot as plt\nimport numpy as np\n\n' + item)
      s += text[f'tmp{num}.py'] + '\n'
      if i:
        with open(f'/content/tmp/tmp{num+ad}.py', mode='w', encoding='utf8') as f:
          f.write(s)
        text[f'tmp{num+ad}.py'] = s
      i = True
  return text

def Start(usr):
  sys.path.append('/content/tmp')
  mkdir('/content/tmp')
  # flag = False
  t = save_cells(usr.content['In'])
  tasks = [Task1(alias={r'def\s+check_arrays\s*\(': 'check_arrays'}),
           Task2(alias={r'def\s+find_angle\s*\(': 'find_angle'}),
           Task3(alias={r'my_array\s*=': 'my_array',
                        r'plt\.imshow\(': 'plt.imshow'}),
           Task4(alias={r'programmingLanguages\s*=': 'programmingLanguages',
                        r'popuratity\s*=': 'popuratity',
                        r'colors\s*=': 'colors',
                        r'plt.pie\s*\(': 'plt.pie'}),
           Task5(alias={r'x\s*=': 'x',
                        r'\.plot\(.*=?x.*linestyle\s*=.*label\s*=': 'plt.plot(x, y, linestyle="...", label="...")',
                        r'\.xlabel\([\'"]x[\'"]\)': 'plt.xlabel',
                        r'\.ylabel\([\'"]y[\'"]\)': 'plt.ylabel',
                        r'\.legend\(\)': 'plt.legend'})]
  res = [op.check_task(t) for op in tasks]
  clear_output()
  num = 0 
  for i in tqdm(res, desc='Задание ', bar_format='{l_bar}{bar}  {n_fmt}/{total_fmt}', colour='red' if not all(res) else 'green'):
    # print(tasks)
    num += 1
    print('\n\n', f'Задание {num}', 'выполнено' if i else 'сделано неправильно')
    if not i:
      print(', '.join(tasks[num-1].error))
  print('\n') 
  print('ДЗ выполнено' if all(res) else 'Исправьте ошибки и попробуйте снова')
  rmtree('/content/tmp')
  # In.clear()
  usr.content['In'].clear()