from hak.directory.make import f as mkdir
from hak.file.save import f as save
from string import ascii_lowercase as az
from hak.directory.remove import f as rmdir
from os import listdir
from hak.file.remove import f as remove
from hak.string.print_and_return_false import f as pf
from os.path import isfile

r = './temp'
up = lambda: [mkdir(r), *[save(f'{r}/{_}.txt', _) for _ in az]]
dn = lambda: rmdir(r)

f = lambda x: [
  remove(f'{r}/{filename}')
  for filename
  in listdir(x)
  if isfile(f'{r}/{filename}')
]

def t():
  up()
  α = len(listdir(r))
  f(r)
  ω = len(listdir(r))
  result = all([α>ω, ω==0])
  dn()
  return result or pf([f'α: {α}', f'ω: {ω}'])
