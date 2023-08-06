from hak.string.print_and_return_false import f as pf
from hak.string.colour.bright.cyan import f as cy
from hak.string.colour.bright.blue import f as bl
from hak.string.colour.bright.magenta import f as mg

f = lambda x: len(x.split('\n')[-1])

def t():
  x = "abc\ndefg\nhijklm"
  y = 6
  z = f(x)
  return y == z or pf([
    'y != z',
    f'x: {cy(x)}',
    f'[y]: {bl([y])}',
    f'[z]: {mg([z])}'
  ])
