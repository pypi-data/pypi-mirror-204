import sqlite3
import json
from typing import Any
from dataclasses import dataclass
from date_time import get_unix_time
import os

@dataclass
class Column():
    cid: int
    name: str
    type: str
    default: Any
    is_not_null_req: bool
    is_primary_key: bool

@dataclass
class TableDef():
    name: str
    init_sql: str
    num_columns: int
    columns: list

def dict_factory(cursor, row):
    """
    Returns a dict instead of tuple from fetches
    """
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_tables(con: sqlite3.Connection):
    """
    Returns the name of every table in the default DB
    """
    cur = con.cursor()
    res = cur.execute("SELECT * FROM sqlite_master WHERE type='table'")
    p = [TableDef(name=x[1], init_sql=x[-1], num_columns=x[3], columns=[]) for x in res.fetchall()]
    cur.row_factory = dict_factory
    for i in p:
        r = cur.execute(f"pragma table_info({i.name})").fetchall()[0]
        C = Column(cid=r["cid"], name=r["name"], type=r["type"], is_not_null_req=bool(r["notnull"]), default=r["dflt_value"], is_primary_key=bool(r["pk"]))
        i.columns.append(C)
    cur.close()
    return p

def has_table_definition_changed(con: sqlite3.Connection):
    pass

def table_exists(con: sqlite3.Connection, table_name: str) -> bool:
    """
    Returns bool on table existing in db
    """
    if table_name in get_tables(con):
        return True
    else:
        return False

def init_sqlite(tables: list[TableDef], dbname: str=":memory:")->sqlite3.Connection:
    """
    Adds tables to db
    If a table already exists, test if it the new definition is equal to the old
    If not, do something

    """
    con = sqlite3.connect(dbname)
    current_tables = get_tables(con=con)
    for t in tables:
        l = list(filter(lambda x: (t.name == x.name), current_tables))
        print(l[0])
        if len(l) == 1:
            # Must be identical
            if l[0].init_sql == t.init_sql:
                continue
            else:
                print(t.init_sql, l[0].init_sql)

        else:
            con.execute(t.init_sql)
    return con

def get_db_path(con: sqlite3.Connection):
    cur = con.cursor()
    cur.execute("PRAGMA database_list")
    rows = cur.fetchall()
    return rows[0][2]

def backup_table(con: sqlite3.Connection, table_name: str):
    cur = con.cursor()
    columns = cur.execute(f'PRAGMA table_info({table_name});').fetchall()
    cols = {}
    count = 0
    for c in columns:
        cols = {**cols, **{c[1]: []}}
        count = count + 1

    cur.row_factory = dict_factory
    res = cur.execute(f"SELECT * FROM {table_name}")
    res = res.fetchall()
    for r in res:
        for rr in r.items():
            cols[rr[0]].append(rr[1])
    db_path = get_db_path(con)
    dir = os.path.dirname(db_path)
    with open(os.path.join(dir, f"{get_unix_time()}.db_backup.json"), "w") as f:
        json.dump(cols, f)

def dict_to_where_clause(d: dict)->str:
    res = []
    for kv in d.items():
        if " " in kv[0]:
            key = kv[0].replace(" ", "_")
        else:
            key = kv[0]

        if isinstance(kv[1], str):
            val = f"'{kv[1]}'"
        else:
            val = kv[1]
        res.append(f"{key}={val}")
    return ", ".join(res)

if __name__ == "__main__":
    init_sqlite([TableDef(name="testing", init_sql=f"CREATE TABLE testing (id, name, other_stuff)", num_columns=3, columns=[])], "/shared/todos/default.db")
