from typing import Type
from .Helper import map_substring,timing

@timing
def steps_pme(s:Type):
    """
    Semelhante a steps mas mais generalizada
    Aviso: Somente utilizar em bots novos
    ARGS
    s = pd.Series category do dataframe tracking
    """
    product_map = {
        'identify': '1-Identifica prospect e endereco',
        'plan-selection':'2-Escolhe plano',
        'registration':'3-Realiza cadastro',
        'payment':'4-Define metodo de pagamento',
        'schedule':'5-Agenda instalacao',
        'checkout':'6-Finaliza pedido'
    }
    
    s = s.apply(lambda x : map_substring(x, product_map))
    return s