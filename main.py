from support import log, import_file
import table as tb

def run():
  print('Import from\n(default = 1)\n\n1 - html\n2 - csv\n')
  import_from = int(input() or 1)

  rows = import_file(import_from)
  
  if rows != []:
    tb.update(rows[0]) if import_from == 1 else None
    tb.write(rows[::-1])
  
  log(len(rows))
  
if __name__ == "__main__":
  run()