import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

# ------------- DB CONFIG -------------
DB_DSN = (
    f"dbname={os.getenv('POSTGRES_DB')} "
    f"user={os.getenv('POSTGRES_USER')} "
    f"password={os.getenv('POSTGRES_PASSWORD')} "
    f"host=localhost "
    f"port={os.getenv('POSTGRES_PORT')}"
)

SCHEMA = "raw"
BASE_DIR = os.getenv('BASE_DIR')
DELIMITER = "|"          
TRUNCATE_BEFORE_LOAD = True


# TPC-H table definitions (Postgres types)
TABLE_DEFS = {
    "customer": {
        "filename": "customer.tbl",
        "columns": [
            ("c_custkey",   "INTEGER"),
            ("c_name",      "VARCHAR(25)"),
            ("c_address",   "VARCHAR(40)"),
            ("c_nationkey", "INTEGER"),
            ("c_phone",     "CHAR(15)"),
            ("c_acctbal",   "DECIMAL(15,2)"),
            ("c_mktsegment","CHAR(10)"),
            ("c_comment",   "VARCHAR(117)")
        ],
    },
    "lineitem": {
        "filename": "lineitem.tbl",
        "columns": [
            ("l_orderkey",      "INTEGER"),
            ("l_partkey",       "INTEGER"),
            ("l_suppkey",       "INTEGER"),
            ("l_linenumber",    "INTEGER"),
            ("l_quantity",      "DECIMAL(15,2)"),
            ("l_extendedprice", "DECIMAL(15,2)"),
            ("l_discount",      "DECIMAL(15,2)"),
            ("l_tax",           "DECIMAL(15,2)"),
            ("l_returnflag",    "CHAR(1)"),
            ("l_linestatus",    "CHAR(1)"),
            ("l_shipdate",      "DATE"),
            ("l_commitdate",    "DATE"),
            ("l_receiptdate",   "DATE"),
            ("l_shipinstruct",  "CHAR(25)"),
            ("l_shipmode",      "CHAR(10)"),
            ("l_comment",       "VARCHAR(44)")
        ],
    },
    "nation": {
        "filename": "nation.tbl",
        "columns": [
            ("n_nationkey", "INTEGER"),
            ("n_name",      "CHAR(25)"),
            ("n_regionkey", "INTEGER"),
            ("n_comment",   "VARCHAR(152)")
        ],
    },
    "orders": {
        "filename": "orders.tbl",
        "columns": [
            ("o_orderkey",      "INTEGER"),
            ("o_custkey",       "INTEGER"),
            ("o_orderstatus",   "CHAR(1)"),
            ("o_totalprice",    "DECIMAL(15,2)"),
            ("o_orderdate",     "DATE"),
            ("o_orderpriority", "CHAR(15)"),
            ("o_clerk",         "CHAR(15)"),
            ("o_shippriority",  "INTEGER"),
            ("o_comment",       "VARCHAR(79)")
        ],
    },
    "partsupp": {
        "filename": "partsupp.tbl",
        "columns": [
            ("ps_partkey",     "INTEGER"),
            ("ps_suppkey",     "INTEGER"),
            ("ps_availqty",    "INTEGER"),
            ("ps_supplycost",  "DECIMAL(15,2)"),
            ("ps_comment",     "VARCHAR(199)")
        ],
    },
    "part": {
        "filename": "part.tbl",
        "columns": [
            ("p_partkey",     "INTEGER"),
            ("p_name",        "VARCHAR(55)"),
            ("p_mfgr",        "CHAR(25)"),
            ("p_brand",       "CHAR(10)"),
            ("p_type",        "VARCHAR(25)"),
            ("p_size",        "INTEGER"),
            ("p_container",   "CHAR(10)"),
            ("p_retailprice", "DECIMAL(15,2)"),
            ("p_comment",     "VARCHAR(23)")
        ],
    },
    "region": {
        "filename": "region.tbl",
        "columns": [
            ("r_regionkey", "INTEGER"),
            ("r_name",      "CHAR(25)"),
            ("r_comment",   "VARCHAR(152)")
        ],
    },
    "supplier": {
        "filename": "supplier.tbl",
        "columns": [
            ("s_suppkey",   "INTEGER"),
            ("s_name",      "CHAR(25)"),
            ("s_address",   "VARCHAR(40)"),
            ("s_nationkey", "INTEGER"),
            ("s_phone",     "CHAR(15)"),
            ("s_acctbal",   "DECIMAL(15,2)"),
            ("s_comment",   "VARCHAR(101)")
        ],
    },
}


def main():
    conn = psycopg2.connect(DB_DSN)
    cur = conn.cursor()

    try:
        # 1) Ensure schema exists
        cur.execute(f'CREATE SCHEMA IF NOT EXISTS "{SCHEMA}";')

        for table_name, conf in TABLE_DEFS.items():
            filename = conf["filename"]
            path = os.path.join(BASE_DIR, filename)
            columns = conf["columns"]

            print(f"\nProcessing {path} -> {SCHEMA}.{table_name}")

            if not os.path.exists(path):
                print(f"File not found, skipping: {path}")
                continue

            # 2) Create table with correct column names/types
            col_defs = ", ".join(f'"{name}" {dtype}' for name, dtype in columns)
            create_sql = f'CREATE TABLE IF NOT EXISTS "{SCHEMA}"."{table_name}" ({col_defs});'
            cur.execute(create_sql)

            # 3) Optional truncate
            if TRUNCATE_BEFORE_LOAD:
                cur.execute(f'TRUNCATE TABLE "{SCHEMA}"."{table_name}";')

            # 4) COPY data
            col_names_sql = ", ".join(f'"{name}"' for name, _ in columns)
            copy_sql = (
                f'COPY "{SCHEMA}"."{table_name}" ({col_names_sql}) '
                f"FROM STDIN WITH (FORMAT csv, DELIMITER '{DELIMITER}', HEADER FALSE)"
            )

            print(f"Loading data from {path}")
            with open(path, "r", encoding="utf-8") as infile:
                cur.copy_expert(copy_sql, infile)

            print(f"Loaded into {SCHEMA}.{table_name}")

        conn.commit()
        print("\nAll TPC-H tables loaded into schema:", SCHEMA)

    except Exception as e:
        conn.rollback()
        print("\nError occurred, transaction rolled back.")
        print(e)
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    main()
