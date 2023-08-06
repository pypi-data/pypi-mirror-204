from os.path import exists
from os import mkdir as osmkdir
from re import L

from hak.directory.remove import f as remove
from hak.string.print_and_return_false import f as pf

from hak.nop import f as nop
# nop = lambda x=None: None # DELETE LINE

def f(x='./hak/classes'):
  if exists(x): return nop(x)
  try: osmkdir(x)
  except FileNotFoundError as fe:
    f('/'.join(x.split('/')[:-1]))
    f(x)

temp_path_0 = './temp_dir_make'
temp_path_1 = f'{temp_path_0}/_'

def dn():
  remove(temp_path_1)
  remove(temp_path_0)

def t():
  f(x=temp_path_1)
  result = exists(temp_path_1)
  dn()
  return result or pf(f'Failed to create temporary directory: {temp_path_1}')
