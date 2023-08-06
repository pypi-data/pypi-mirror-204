from sqlstrings.value_handling import read_val
from typing import Callable, Any
from pathlib import Path
from csv import reader
from sqlstrings.transact import insertion, update
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class CSVFile:
    """
    Class abstracts CSVFile loading to make iterating through rows easier.
    """

    def __init__(self, path: str | Path):
        """
        Constructs a new CSVFile object given the path of the csv file to load.
        :param path: The path of the csv file to load.
        """
        self.path = handle_path(path)
        self.reader = None
        self.header = None
        self.rows = None

    def __enter__(self):
        self.csv = open(self.path, 'rt')
        self.rows = reader(self.csv)
        self.header = self.rows.__next__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.csv.close()
        self.reader = None
        self.header = None
        self.rows = None


def handle_path(path: str | Path):
    if isinstance(path, str):
        path = Path(path).resolve()
    elif isinstance(path, Path):
        path = path.resolve()
    else:
        raise NotImplementedError()
    return path


def __row_to_header_row_dict(header: list[str], row: list[str]) -> dict[str:Any]:
    """
    Geven a csv files header and a row from that file, this function will output a dictionary 
    mapping each header title to its respective value.
    :param header: The header of the csv file.
    :param row: The row of the csv file.
    :return: row_dict The dictionary representing that row.
    """
    row_dict = {}
    for idx, value in enumerate(row):
        row_dict[header[idx]] = read_val(value.lstrip().rstrip())
    return row_dict


def csv_to_inserts(path: str | Path, table_name: str, insertion_func: Callable = insertion):
    """
    Converts a .csv file into a list of insert statement strings that can be executed in a SQL Database.
    :param path: The path of the file to convert.
    :param table_name: The name of the table in which to insert.
    :param insertion_func: The function to use to generate the insertion statements i.e. from postgre, or sql?
    :return: A list of insert strings.
    """
    with CSVFile(path) as f:
        for row in f.rows:
            # Create a dict with the names and values for insertion convertion
            yield insertion_func(table_name, __row_to_header_row_dict(f.header, row))


def csv_to_updates(path: str | Path, table_name: str, update_func: Callable = update):
    """
    A generator yielding the rows of a given csv file as updatet statements.
    :param path: The path of the csv file to target.
    :param table_name: The name of the table in the update statement.
    :update_func: The name of the function used to construct the update statement (varying by dialect).
    """
    with CSVFile(path) as f:
        for row in f.rows:
            # Create a dict with the column names and update values.
            yield update_func(table_name, __row_to_header_row_dict(f.header, row))

if __name__ == '__main__':
    # def csv_to_updates(path: str | Path, table_name: str, update_func: Callable = update):
    test_path = "C:/Users/AlistairKellaway/Downloads/snakes_count_100.csv"

    print(list(csv_to_inserts(test_path, "table_name", insertion_func=insertion)))
    print(up := list(csv_to_updates(test_path, "table_name", update_func=update)))
    for u in up:
        print(u)
