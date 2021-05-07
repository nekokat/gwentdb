from fromfile import import_file
import table as tb

def run():
  import_from = int(input('Import from\n(default = 1)\n\n1 - html\n2 - csv\n') or 1)

  rows = import_file(import_from)
  
  if rows != []:
    tb.update(rows[0]) if import_from == 1 else None
    tb.write(rows[::-1])
  
if __name__ == "__main__":
  run()