from support import log, from_file
import table as tb

def run():
  print('Import from\n(default = 1)\n\n1 - html\n2 - csv\n')
  import_from = int(input() or 1)

  lines = from_file(import_from)
  
  if lines != []:
    tb.update(lines[0]) if import_from == 1 else None
    tb.write(lines[::-1])
  
  log(len(lines))

run()