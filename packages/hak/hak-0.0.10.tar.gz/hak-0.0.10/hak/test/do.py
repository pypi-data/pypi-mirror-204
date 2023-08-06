from time import time
from hak.test.passed.handle import f as hp
from hak.dict.test_durations.to_tuple_list_sorted_by_duration import f as srt
from hak.list.strings.filepaths.py.testables.get import f as list_testables
from os.path import getmtime

# ------------------------------------------------------------------------------
# from hak.test.make_Pi_to_test import f as make_Pi_t
_Pi = ['./a.py', './b.py', './c.py']
_test_all  = False
_prev = {'./b.py': 32481.8, './c.py': 32497.3}
_last_mods = {'./a.py': 97551.0, './b.py': 32481.8, './c.py': 32497.3}

def make_Pi_t(_Pi, test_all, prev, last_mods): return (
  _Pi.copy() if test_all else [
    _pi for _pi in _Pi if (
      (prev[_pi] if _pi in prev else 0)
      !=
      (last_mods[_pi] if _pi in last_mods else 0)
    )
  ]
) or _Pi.copy()

# ------------------------------------------------------------------------------

from hak.file.pickle.load_if_exists import f as load_pickle
from hak.file.remove import f as remove
from hak.file.pickle.save import f as save
from hak.list.strings.filepaths.py.to_filepath_file_content_dict import f as pyfiles_to_dict
from hak.string.contains.function.test import f as has_t
from hak.string.contains.function.run import f as has_f

# ------------------------------------------------------------------------------
# from hak.test.pi_test_failed import f as _pi_test_failed
from importlib import import_module
_pi_test_failed = lambda x: not import_module(x.replace('/','.').replace('..','')[:-3]).t()
# ------------------------------------------------------------------------------

from hak.test.failed.handle import f as  hf
from hak.string.colour.bright.red import f as danger
from hak.string.colour.dark.yellow import f as warn

def f(test_all=False, t_0=time()):
  _Pi = list_testables()
  try: prev = load_pickle('./last_modified.pickle') or set()
  except EOFError as eofe: remove('./last_modified.pickle'); prev = set()
  last_mods = {py_filename: getmtime(py_filename) for py_filename in _Pi}
  save(last_mods, './last_modified.pickle')
  _Pi_fail = set()
  _A = [_[0] for _ in srt(last_mods)[::-1]]
  _B = set(make_Pi_t(_Pi, test_all, prev, last_mods) + list(_Pi_fail))
  _Pi_t = [a for a in _A if a in _B]
  pyfile_data = pyfiles_to_dict(_Pi_t)
  max_len = 0
  for _pi_index, _pi in enumerate(_Pi_t):
    content = pyfile_data[_pi]
    _m = ' '.join([
      f'[{(100*(_pi_index+1)/len(_Pi_t)):> 6.2f} % of',
      f'{_pi_index+1}/{len(_Pi_t)} files.] Checking {_pi}'
    ])
    max_len = max(max_len, len(_m))
    # print(f'{_m:<{max_len}}', end='\r')
    print(f'{_m:<{max_len}}')
    if not has_t(content): return hf(_Pi_fail, _pi, danger(" has no ")+warn('t()'))
    if not has_f(content): return hf(_Pi_fail, _pi, danger(" has no ")+warn('f()'))
    if _pi_test_failed(_pi): return hf(_Pi_fail, _pi, '')
  return hp(t_0, _Pi_t)
