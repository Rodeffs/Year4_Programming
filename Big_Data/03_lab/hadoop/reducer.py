#!/usr/bin/env python

import sys

prev_entry = None
result = 0

for line in sys.stdin:
    line = line.strip()
    entry, value = line.split(';')

    # Проверки, что вводимые данные можно преобразовать

    try:
        value = int(value)
    except ValueError:
        continue

    if entry is None:
        continue

    # Т.к. Hadoop по умолчанию сортирует вывод mapper, то можно сделать так

    if prev_entry != entry and prev_entry is not None:
        print(f"{prev_entry};{result}")
        result = 0

    prev_entry = entry
    result += value
