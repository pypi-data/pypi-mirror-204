from hak.directory.make import f as mkdirine
from hak.file.save import f as save
from hak.directory.remove import f as rmdir
from hak.string.print_and_return_false import f as pf
from os.path import getmtime
from hak.directory.filepaths.get import f as get_filepaths
from time import sleep

def f(x):
  filepaths = get_filepaths(x, [])
  latest = {'filepath': '', 'time': 0}
  for filepath in filepaths:
    last_modified_time = getmtime(filepath)
    if last_modified_time > latest['time']:
      latest = {'filepath': filepath, 'time': last_modified_time}
  return latest['filepath']

def up():
  x = {}
  x['dir_name'] = './test_directory_get_most_recently_modified'
  
  # Create test directory
  mkdirine(x['dir_name'])

  # create old file
  x['old_file_content'] = 'ABC'
  x['old_file_path'] = f"{x['dir_name']}/old_file.txt"
  save(x['old_file_path'], x['old_file_content'])

  sleep(1)

  # create new file
  x['new_file_content'] = 'XYZ'
  x['new_file_path'] = f"{x['dir_name']}/new_file.txt"
  save(x['new_file_path'], x['new_file_content'])

  return x

dn = lambda x: rmdir(x['dir_name'])

def t():
  x = up()
  y = x['new_file_path']
  z = f(x['dir_name'])
  dn(x)
  return y == z or pf([f'x: {x}', f'y: {y}', f'z: {z}'])
