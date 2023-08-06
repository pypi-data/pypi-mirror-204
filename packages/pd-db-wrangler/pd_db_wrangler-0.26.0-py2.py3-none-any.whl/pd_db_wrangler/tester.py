from .pd_db_wrangler import Pandas_DB_Wrangler


"""
pdw = Pandas_DB_Wrangler(
    "postgresql+psycopg2://taiga:Squeezing-Subprime9-Partake@taiga.murraycountymed.org:5432/taiga"
)
sql = pdw.read_sql_file("build/history.sql")
df = pdw.df_fetch(sql)
# df = pdw.df_fetch("select * from accounts", index_col="guid")
print(df.index.name)
print(df.index.dtype)
print(df.dtypes)
print(df)
"""


pdw = Pandas_DB_Wrangler()
# sql = pdw.read_sql_file("build/transactions_master.sql")

multiplier = "* 1"
guid = "long_guid"
inner_where = f"""
                where
                    accounts.guid not in ('{guid}')
                """
main_where = f""" where a.guid in ('{guid}')"""
injection = {
    "multiplier": multiplier,
    "inner_where": inner_where,
    "main_where": main_where,
}
# sql = "select {multiplier} from { inner_where } where { main_where }"
sql = pdw.read_sql_file("build/transactions_master.sql")
print(sql)
print(sql.format(**injection))
