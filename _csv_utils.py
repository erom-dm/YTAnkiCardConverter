import csv
import os
from pprint import pprint
from _helper import FIELD_NAMES


class TableIO:
    def __init__(self, file_name: str):
        self._file_name = file_name
        self._field_names = FIELD_NAMES
        self._file_exists = (
            os.path.exists(self._file_name) and os.path.getsize(self._file_name) > 0
        )

    def readRows(self):
        if not self._file_exists:
            return []
        with open(self._file_name, mode="r", encoding="utf-8", newline="") as infile:
            reader = csv.DictReader(infile)
            result = []
            for row in reader:
                result.append(row)
            return result

    def writeRows(self, rows_to_write: dict[str]):
        with open(self._file_name, mode="a", encoding="utf=8", newline="") as outfile:
            writer = csv.DictWriter(outfile, self._field_names)
            if not self._file_exists:
                writer.writeheader()
            pprint(rows_to_write)
            writer.writerows(rows_to_write)
        print(f"Succesfully appended {len(rows_to_write)} rows to {self._file_name}")
