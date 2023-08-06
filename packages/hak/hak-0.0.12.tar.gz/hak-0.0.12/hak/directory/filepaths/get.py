from os import listdir
from os import remove
from os.path import isdir

from hak.directory.make import f as mkdir
from hak.directory.remove import f as remove_dir
from hak.file.save import f as save
from hak.string.print_and_return_false import f as pf

def f(root, filepaths=[], condition=lambda x: True):
  for item in listdir(root):
    _pi = root+'/'+item
    if isdir(_pi): f(_pi, filepaths, condition)
    if condition(item): filepaths.append(_pi)
  return filepaths

temp_dir_0 = './_list_filepaths'
temp_dir_1 = f'{temp_dir_0}/_'
temp_files_and_content = [
  (f'{temp_dir_0}/foo.py', 'foo'),
  (f'{temp_dir_0}/xyz.txt', 'xyz'),
  (f'{temp_dir_1}/abc.txt', 'abc'),
  (f'{temp_dir_1}/bar.py', 'bar'),
]

def up():
  for temp_dir in [temp_dir_0, temp_dir_1]: mkdir(temp_dir)
  for (filename, content) in temp_files_and_content: save(filename, content)

def dn():
  for (filename, _) in temp_files_and_content: remove(filename)
  remove_dir(temp_dir_1)
  remove_dir(temp_dir_0)

def t():
  up()
  y = set([
    f'{temp_dir_1}/abc.txt',
    f'{temp_dir_1}/bar.py',
    f'{temp_dir_1}',
    f'{temp_dir_0}/xyz.txt',
    f'{temp_dir_0}/foo.py'
  ])
  z = set(f(temp_dir_0))
  dn()
  return y == z or pf([f'y: {y}', f'z: {z}'])
