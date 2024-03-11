from sqlalchemy import create_engine
from urllib.parse import quote_plus

class connectionAlchemy:
    server = 'NOBRPOASQL02' #Trocar para uma variavel de ambiente
    database = 'FPY' #Trocar para uma variavel de ambiente
    username = 'FPY' #Trocar para uma variavel de ambiente
    password = quote_plus('FPY@2020!') #O @ estava atrapalhando a conexão. Trocar para uma variavel de ambiente
    engine = None

    def __init__(self):
        self.engine = create_engine(url="mssql+pymssql://{0}:{1}@{2}/{3}".format(self.username, self.password, self.server, self.database))