import unittest
from sys import path

path.append("sqlstrings")

import postgre

class TestPostgre(unittest.TestCase):

    def test_insertion(self):
        names_values = {
            "col1": "flash",
            "col2": "batman",
            "col3": "joker",
            "col4": "iceman"
        }
        exp = "INSERT INTO my_table\n\tmy_table(col1, col2, col3, col4)\nVALUES\n\t(\"flash\", \"batman\", \"joker\", \"iceman\");"
        self.assertEqual(postgre.insertion("my_table", names_values), exp)

    def test_procedure_call(self):
        params_args = {
            "param1": "arg1",
            "param2": "arg2",
            "param3": "arg3",
            "param4": "arg4",
            "param5": "arg5"
        }
        exp = "CALL proc_name(\"arg1\", \"arg2\", \"arg3\", \"arg4\", \"arg5\");"
        self.assertEqual(exp, postgre.procedure_call(
            "proc_name", params_args))

    def test_create_table(self):
        col_names_types = {
            "name1": "typ1",
            "name2": "type2",
            "name3": "type3",
            "name4": "type4",
            "name5": "type5"
        }
        exp = "CREATE TABLE table_name (name1 typ1,\n\tname2 type2,\n\tname3 type3,\n\tname4 type4,\n\tname5 type5\n);"
        self.assertEqual(exp, postgre.create_table(
            "table_name", col_names_types))

    def test_drop_table(self):
        exp = "DROP TABLE table_name;"
        self.assertEqual(exp, postgre.drop_table("table_name"))
        exp = "DROP TABLE table, table2, table3;"
        self.assertEqual(exp, postgre.drop_table(
            ["table", "table2", "table3"]))

    def test_update(self):
        d = {
            "k1": "10",
            "k2": "10.01234",
            "k3": "NULL",
            "k4": "v4"
        }
        exp = "UPDATE table_name\nSET k1 = \"10\",\n    k2 = \"10.01234\",\n    k3 = NULL,\n    k4 = \"v4\"\nWHERE X>4;"
        self.assertEqual(exp, postgre.update("table_name", d, where="X>4"))
        d = {
            "f1": 10,
            "f2": "Holla",
            "f3": 1234.56,
            "f4": -13.9087321
        }
        exp = "UPDATE table_name\nSET f1 = 10,\n    f2 = \"Holla\",\n    f3 = 1234.56,\n    f4 = -13.9087321\nWHERE HERE IS SOME CONDITIONAL;"
        self.assertEqual(exp, postgre.update(
            "table_name", d, where="HERE IS SOME CONDITIONAL"))


if __name__ == '__main__':
    unittest.main()
