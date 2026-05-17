import csv
import os
from pprint import pprint

class TableIO:
    def __init__(self, file_name: str):
        self._file_name = file_name
        self._field_names = ['word', "part of speech", "plural", "definitions", "examples" , "source"]

    def readTableRows(self):
        with open(self._file_name, mode="r", encoding="utf-8", newline="") as infile:
            reader = csv.DictReader(infile)
            result = []
            for row in reader:
                result.append(row)
            return result
                
    
    def writeTableRows(self, rows_to_write: dict[str]):
        file_exists = os.path.exists(self._file_name) and os.path.getsize(self._file_name) > 0
        with open(self._file_name, mode="a", encoding="utf=8", newline="") as outfile:
            writer = csv.DictWriter(outfile, self._field_names)
            if not file_exists:
                writer.writeheader()
            writer.writerows(rows_to_write)
        print(f"Succesfully appended {len(rows_to_write)} rows to {self._file_name}")
    

io = TableIO("test_write.csv")
test_write_dict=[
    {
        "word": "foo",
        "part of speech": "noun",
        "plural": "foos",
        "definitions": "foo?",
        "examples": "foo bar baz",
        "source": "some source"
    },
    {
        "word": "asd",
        "part of speech": "verb",
        "plural": "aasdsss",
        "definitions": "asd?",
        "examples": "asfas  barsadasd b dasdaaz",
        "source": "some source 2"
    },
    {
        "word": "mmm",
        "part of speech": "ddas",
        "plural": "f21312oos",
        "definitions": "fodasdo?",
        "examples": "foo eqw eqweqwe wqeqweq baz",
        "source": "some source 3"
    },
]
pprint(io.writeTableRows(test_write_dict), indent=2, width=40)