import datetime
import pandas as pd


def today(fmt="%Y%m%d"):
    return datetime.datetime.now().strftime(fmt)


def yestoday(fmt="%Y%m%d"):
    return (datetime.datetime.now() - datetime.timedelta(days=1)).strftime(fmt)


def database2df(db, command="SELECT * from {table}", table=None):
    command = command.replace("{table}", table)
    df = pd.read_sql(command, db.conn)
    return df


def database2csv(db, table, csv):
    database2df(db=db, table=table).to_csv(csv, index=False)


def csv2database(db, csv):
    df = pd.read_csv(csv)
    for idx, row in df.iterrows():
        data = row.to_dict()
        db.insert(**data)