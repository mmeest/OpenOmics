import errno
import os

import dask.dataframe as dd
import requests
import sqlalchemy as sa
from astropy.utils import data
from requests.adapters import HTTPAdapter


def get_pkg_data_filename(dataurl, file_name):
    """
    Downloads a remote file given the url, then caches it to the user's home folder.
    Args:
        dataurl: Url to the download path, excluding the file name
        file_name: The file name to download

    Returns:
        filename (str): A file path on the local file system corresponding to the data requested in data_name.
    """
    with data.conf.set_temp("dataurl", dataurl), data.conf.set_temp("remote_timeout", 30):
        return data.get_pkg_data_filename(file_name, show_progress=True)


def read_db(connString="sqlite:///c:\\temp\\test.db", table='testtable'):
    engine = sa.create_engine(connString)
    conn = engine.connect()
    m = sa.MetaData()
    table = sa.Table(table, m, autoload=True, autoload_with=engine)

    # conn.execute("create table testtable (uid integer Primary Key, datetime NUM)")
    # conn.execute("insert into testtable values (1, '2017-08-03 01:11:31')")
    # print(conn.execute('PRAGMA table_info(testtable)').fetchall())
    # conn.close()

    uid, dt = list(table.columns)
    q = sa.select([dt.cast(sa.types.String)]).select_from(table)

    daskDF = dd.read_sql_table(table, connString, index_col='uid', parse_dates={'datetime': '%Y-%m-%d %H:%M:%S'})
    return daskDF


def mkdirs(outdir):
    try:
        os.makedirs(outdir)
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise exc
        pass


def retry(num=5):
    """"retry connection.

        define max tries num
        if the backoff_factor is 0.1, then sleep() will sleep for
        [0.1s, 0.2s, 0.4s, ...] between retries.
        It will also force a retry if the status code returned is 500, 502, 503 or 504.

    """
    s = requests.Session()
    retries = Retry(total=num, backoff_factor=0.1,
                    status_forcelist=[500, 502, 503, 504])
    s.mount('http://', HTTPAdapter(max_retries=retries))

    return s
