import psycopg2
import pandas as pd
from os import environ
from sys import exit
from typing import Type
from .Helper import timing,helper_columns

        
@timing
def form_df_tracking(query:str) -> type(pd.DataFrame):
    """
        Extrai os dados do RDS, e transforma em pandas object
        ARGS
        query = Query a ser feita
    """
    try:
        engine = psycopg2.connect(
            database = 'postgres',
            user = 'tracking',
            password = environ['SQL_PET_PASSWORD'],
            host = 'pet-avi-chatbot-tracking-db.clarobrasil.mobi',
            port = '5432',
        )
    except (Exception,psycopg2.Error) as error:
        print(f'''
            Erro na conexão
            {error}
            ''',)
        exit(1)

    cursor = engine.cursor()
    cursor.execute(query) # Executando query, para obtencao de dados
    data = cursor.fetchall() # Pegando esse dados
    cols = helper_columns(cursor = cursor)
    df = pd.DataFrame(data = data, columns = cols)
    if df.empty:
        raise Exception('O seu dataframe está vazio! Algo está de errado com o seu query')
    return df
    
@timing
def form_df_extras(df:Type):
    """  
        Explode os extras globais dentro da coluna,
        global_extras_raw
        ARGS
        df = Dataframe base
    """
    new_df = pd.DataFrame(list(df['global_extras_raw']))
    if new_df.empty:
        raise Exception('O seu dataframe de extras está vazio! Verifique o seu query')
    return new_df

def expurge_to_s3():
    pass

