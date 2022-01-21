import pyodbc

import requests

repoList = list()
server = 'introducaosql.database.windows.net' 
database = 'pythonSQL' 
username = 'g.rosa' 
password = 'kumulus2022.' 
driver = '{ODBC Driver 17 for SQL Server}'
conn = pyodbc.connect('DRIVER='+driver+';SERVER='+server +';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+password)

cursor = conn.cursor()

user = str(input('User: '))
r = requests.get(f'https://api.github.com/users/{user}/repos')
repos = r.json()


for repo in repos:
    repoList.append(repo['name'])
    cursor.execute('''
    INSERT INTO repositorios (nome, repositorio) VALUES(?,?)''', user, repo["name"])
cursor.commit()
cursor.close()
conn.close()