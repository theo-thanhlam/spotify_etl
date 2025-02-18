import sqlalchemy
import pandas as pd
from .. import logger


def load_to_db(engine: sqlalchemy.engine.base.Engine, df:pd.DataFrame, table_name:str):
    with engine.connect() as conn:
        try:
            total_records =  df.to_sql(name=table_name, con=conn, if_exists="append", index=False)
            logger.info(f"Add to table {table_name} with {total_records} records")
        except Exception as err:
            logger.error(f"Error when loading to table {table_name}: {err}")
            return 
