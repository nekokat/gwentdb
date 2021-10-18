from fromfile import import_file
import table as tb
import pivot as pv


def run() -> None:
    """Run script and import"""
    import_from = int(input("Import from\n(default = 1)\n\n1 - html\n2 - csv\n") or 1)
    rows = import_file(import_from)
    if rows != []:
        tb.write(rows[::-1])
        pv.update_all(rows)


if __name__ == "__main__":
    run()
