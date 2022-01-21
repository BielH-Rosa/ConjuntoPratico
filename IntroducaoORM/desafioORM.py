import requests
import sqlalchemy
import pyodbc
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import urllib

repoList = list()
server = 'introducaosql.database.windows.net' 
database = 'pythonSQL' 
username = 'g.rosa' 
password = 'kumulus2022.' 
driver = '{ODBC Driver 17 for SQL Server}'

params = urllib.parse.quote_plus(
    'Driver=%s;' % driver +
    'Server=tcp:%s,1433;' % server +
    'Database=%s;' % database +
    'Uid=%s;' % username +
    'Pwd={%s};' % password +
    'Encrypt=yes;' +
    'TrustServerCertification=no;' +
    'Connection Timeout=30;')

conn_str = 'mssql+pyodbc:///?odbc_connect=' + params
engine = sqlalchemy.create_engine(conn_str, echo=True)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Repositorio(Base):
    __tablename__= 'repositorios'

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    repositorio = Column(String)

    def __repr__(self):
        return f'Python {self.nome}'

Base.metadata.create_all(engine) 

user = str(input('User: '))
r = requests.get(f'https://api.github.com/users/{user}/repos')
repos = r.json()


for repo in repos:
    repoList.append(repo['name'])
    engine.execute('''
    INSERT INTO repositorios (nome, repositorio) VALUES(?,?)''', user, repo["name"])

session.commit()
session.new