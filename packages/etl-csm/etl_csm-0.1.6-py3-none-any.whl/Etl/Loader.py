import psycopg2
from re import findall
from logging import info, warning
from sqlalchemy import create_engine
from typing import Type
from os import environ
from .Helper import psql_insert_copy,timing,sqlcol

@timing
def load_cloud(df:Type,bot:str) -> None:
    """
    Ira fazer o processo de carregamento para o RDS depois de processado.
    Ira estipular os datatype para sqlalchemy
    Em seu excption acrescentar nova coluna de acordo com o datatype que ela precisa
    ARGS
    df = pd.DataFrame
    """
    engine_alchemy = create_engine(f"postgresql://tracking:{environ['SQL_PRD_PASSWORD']}@prd-avi-chatbot-tracking-db.clarobrasil.mobi:5432/clean_data")
    tries = 5

    for _ in range(tries):
        try:
            df.to_sql(f'{bot}_tracking_treated',engine_alchemy,method = psql_insert_copy,if_exists = 'append',index = False,chunksize = 10000)
        except  (Exception,psycopg2.Error) as error:
            warning("Tivemos um erro", error)
            warning("Vou executar um handler para ver se consigo resolver!")         
            engine = psycopg2.connect(
                database = 'clean_data',
                user = 'tracking',
                password = environ['SQL_PRD_PASSWORD'],
                host = 'prd-avi-chatbot-tracking-db.clarobrasil.mobi',
                port = '5432',
            )
            cursor = engine.cursor()
            column = findall('"(.*?)"',str(error))[0]
            warning(f"Tive que acrescentar mais uma coluna ao seu dataframe ja existente a coluna foi {column}")
            query = f"""
            ALTER TABLE {bot}_tracking_treated
            ADD COLUMN {column} VARCHAR NULL;
            """
            info(query)
            cursor.execute(query)
            engine.commit()
            # Sempre fazer esse commit pelo amor
            tries -= 1
        if tries == 0:
            warning("E não deu eu puis maximo de colunas que podia")