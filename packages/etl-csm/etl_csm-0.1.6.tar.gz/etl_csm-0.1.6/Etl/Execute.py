from typing import Type
from pandas import concat
from logging import basicConfig,INFO
from .Extrator import form_df_tracking,form_df_extras
from .Treatment_tracking import fill_na_tracking,dtype_tracking,remove_test
from .Treatment_tracking import steps_residential,errors,flag_duplicated_tracks
from .Treatment_extras import patternizing_columns,ensure_nan_extras,dtype_extras,fill_na_extras
from .Treatment_tracking_pme import steps_pme
from .Helper import timing
from .Loader import load_cloud


class Runner:
    """
        Runner é a classe que executa todo o conjunto de funcoes de tratamento.
        Ele tambem inicializa o processo de logs
        ARGS:
        query = String que representa um SQL query valido  
    """
    def __init__(self,query:str,bot:str) -> Type:
        if bot:
            self.bot = bot
            self.query = query
            basicConfig(filename='etl.log',filemode='a',level=INFO, format='%(levelname)s: %(message)s')
        else:
            raise Exception("Para poder rodar essa classe repasse um bot, corparate/residential")

    def etl_df(self):
        """
            Funcao que roda ETL do dataframe tracking,
            nao arquiva em memoria o dataframe extras_df
        """ 
        df = form_df_tracking(self.query) #1
        df = fill_na_tracking(df) #2
        df = remove_test(df) #3 Não se pode remover testes no ambiente de teste porque senao você remove todo mundo
        flag_duplicated_tracks(df) #4
        df = dtype_tracking(df) #5
        df['steps'] = steps_residential(df['category']) #6
        df['errors'] = errors(df['category']) #7
        return df

    def etl_extras_df(self,df:Type) -> Type:
        """
            Funcao que forma o dataframe de extras
            e os trata
        """
        extras_df = form_df_extras(df) #1
        extras_df = patternizing_columns(extras_df) #2
        extras_df = ensure_nan_extras(extras_df) #3
        extras_df = fill_na_extras(extras_df) #4 
        extras_df = dtype_extras(extras_df) #5
        return extras_df

    def etl_df_pme(self):
        df = form_df_tracking(self.query) #1
        df = fill_na_tracking(df) #2
        df = remove_test(df) #3 Não se pode remover testes no ambiente de teste porque senao você remove todo mundo
        flag_duplicated_tracks(df) #4
        df = dtype_tracking(df) #5
        df['steps'] = steps_pme(df['category']) #6
        df['errors'] = errors(df['category']) #7
        return df

    def etl_extras_df_pme(self,df:Type) -> Type:
        extras_df = form_df_extras(df) #1
        extras_df = patternizing_columns(extras_df) #2
        # extras_df = ensure_nan_extras(extras_df) #3 Deixar para avaliacao
        # extras_df = fill_na_extras(extras_df) #4 Deixar para avaliacao
        # extras_df = dtype_extras(extras_df) #5 Deixar para avaliacao
        return extras_df

    def run(self) -> None:
        if self.bot == 'residential':
            df = self.etl_df()
            extras_df = self.etl_extras_df(df)
            df = concat([df,extras_df],axis = 1)
            load_cloud(df,self.bot)
        if self.bot == 'corporate':
            df = self.etl_df_pme()
            extras_df = self.etl_extras_df_pme(df)
            df = concat([df,extras_df],axis = 1)
            load_cloud(df,self.bot)

