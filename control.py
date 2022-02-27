import os, datetime

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD


if not os.path.exists('data'):
    os.mkdir('data')
files = os.listdir("./data")

clear = lambda: os.system('cls')


print(files)

t = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=3, minutes=0))
date = t.strftime("%Y.%m.%d %H.%M")
db_name = 'matrix '+date

conn = sqlite3.connect(f"{db_name}.db")
csr = conn.cursor()
csr.execute("CREATE TABLE matrix (context TEXT NOT NULL, reply NULL)")

