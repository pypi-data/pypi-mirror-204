import inspect
import os
import re
from difflib import SequenceMatcher
from typing import Any, Dict

from debug_toolbar.panels.sql.tracking import unwrap_cursor, wrap_cursor
from django.db import DEFAULT_DB_ALIAS, connections
from django.test import TransactionTestCase
from django.test.testcases import _AssertNumQueriesContext


class Logger(object):
    def __init__(self, context):
        self.queries = []
        self.context = context

    def record(self, sql, raw_sql, stacktrace, *args, **kwargs):
        self.context["records"].append(
            {
                "sql": sql,
                "raw_sql": re.sub(r'SAVEPOINT ".*"', 'SAVEPOINT "%1"', raw_sql),
                "stacktrace": stacktrace,
                "args": args,
                **kwargs,
            }
        )

    def current_transaction_id(self, alias):
        pass

    def new_transaction_id(self, alias):
        pass


class _AssertQueriesContext(_AssertNumQueriesContext):
    def __init__(self, test_case, num, connection, context_dict):
        self.context_dict = context_dict
        super().__init__(test_case, num, connection)

    def __exit__(self, exc_type, exc_value, traceback):
        unwrap_cursor(self.connection)
        filename = self.context_dict["filename"]
        try:
            with open(filename, "r") as f:
                lines = f.readlines()
        except FileNotFoundError:
            lines = None
        raw_queries = [s["raw_sql"] for s in self.context_dict["records"]]
        if lines:
            lines = [line.strip() for line in lines]
            s = SequenceMatcher(None, lines, raw_queries)
            for tag, i1, i2, j1, j2 in s.get_opcodes():
                if tag not in ["insert", "replace", "equal"]:
                    print(
                        "{:7}   a[{}:{}] --> b[{}:{}] {!r:>8} --> {!r}".format(
                            tag,
                            i1,
                            i2,
                            j1,
                            j2,
                            [s[:50] + "..." for s in lines[i1:i2]],
                            [s[:50] + "..." for s in raw_queries[j1:j2]],
                        )
                    )
                if tag in ["insert", "replace"]:
                    for j in range(j1, j2):
                        string = ""
                        if tag == "insert":
                            string += "New query was recorded:\n"
                        elif tag == "replace":
                            string += "Query was replaced:\n"
                        string += raw_queries[j1]
                        string += "\n"
                        string += "Stacktrace:\n"
                        string += "\n".join(
                            f'  File: "{s[0]}", Line: {s[1]}, in {s[2]}\n    {s[3]}'
                            for s in self.context_dict["records"][j]["stacktrace"]
                        )
                        string += "\n"
                        string += "\n".join(
                            [
                                f"{rk}: {rv}"
                                for rk, rv in self.context_dict["records"][j].items()
                                if rk not in ["raw_sql", "stacktrace"]
                            ]
                        )
                        string += "\n"
                        string += "-----------------------------------------"
                        print(string)

        if not os.environ.get("TEST_QUERIES_REWRITE_SQLLOGS"):
            filename += ".new"
        os.makedirs(filename.rsplit("/", 1)[0], exist_ok=True)
        with open(filename, "w") as f:
            f.write("\n".join(raw_queries))

        return super().__exit__(exc_type, exc_value, traceback)


class NumQueriesMixin(TransactionTestCase):
    context: Dict[str, Any] = {
        "records": [],
    }

    def assertNumQueries(  # noqa: N802
        self, num, func=None, *args, using=DEFAULT_DB_ALIAS, **kwargs
    ):
        conn = connections[using]
        path, file_prefix = inspect.getmodule(self).__file__[:-3].rsplit("/", 1)
        filename = (
            f"{path}/sqllog/{file_prefix}."
            f"{self.__class__.__name__}."
            f"{self._testMethodName}.sqllog"
        )
        # if os.path.exists(filename):
        #     os.remove(filename)
        self.context["filename"] = filename
        logger = Logger(context=self.context)

        wrap_cursor(conn, logger)
        context = _AssertQueriesContext(self, num, conn, self.context)

        if func is None:
            return context

        with context:
            func(*args, **kwargs)
