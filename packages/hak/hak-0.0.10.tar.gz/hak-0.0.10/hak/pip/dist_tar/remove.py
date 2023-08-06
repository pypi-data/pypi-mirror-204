from os.path import exists

from hak.directory.make import f as mkdir
from hak.directory.empty import f as empty_directory
from hak.directory.remove import f as rmdirie
from hak.file.save import f as save
from hak.string.print_and_return_false import f as pf

from copy import deepcopy

def f(x):
  x = deepcopy(x)
  root = x['root'] if 'root' in x else '.'
  return empty_directory(root)

def up():
  temp_root = './_dist_tars_remove'
  mkdir(temp_root)
  filename = f'{temp_root}/junk.tar'
  save(filename, 'junk')
  return {'filename': filename, 'root': temp_root}

dn = lambda x: rmdirie(x['root'])

def t():
  x = up()
  f(x)
  if not exists(x['filename']): return pf(f'not exists({x["filename"]})')
  dn(x)
  if exists(x["root"]): return pf(f'exists({x["root"]})')
  return True
