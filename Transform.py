def feature_engineering(lista): 
    '''
    lista: arquivo json
    '''
    # Recebe o arquivo json e retorna um dataframe 
    
    """################### Importando os Pacotes ######################"""
    
    import pandas as pd
    from datetime import datetime as dt
    import math

    """################### Feature Engineering ###################"""
    
    df = pd.json_normalize(lista)

    # converter a coluna Datetime em tipo datetime;
    df.Date = pd.to_datetime(df.Date, format="%Y-%m-%d").dt.tz_localize(None)

    # Criando features para cada período
    df['year'] = df.Date.dt.year
    df['month'] = df.Date.dt.month.map({1:'Janeiro', 1:'Fevereiro', 3:'Março', 4:'Abril', 5:'Maio', 6:'Junho', 7:'Julho', 8:'Agosto',9:'Setembro', 10:'Outubro', 11:'Novembro', 12:'Dezembro'})
    df['day'] = df.Date.dt.day
    df['day_of_week'] = df.Date.dt.dayofweek.map({0:'Segunda', 1:'Terça', 2:'Quarta', 3:'Quinta', 4:'Sexta', 5:'Sábado', 6:'Domingo'})

    #Criando variáveis para os eventos diários  ao invés de acumulados
    df['Mortes_por_Dia'] = df.Deaths.diff().fillna(0)
    df['Casos_Confirmados_por_Dia'] = df.Confirmed.diff().fillna(0).astype('int64')
    df['Recuperados_por_Dia'] = df.Recovered.diff().fillna(0).astype('int64')
    df['Active'] = df.Recovered.diff().fillna(0).astype('int64')
    df['Dias'] = (df.index + 1 ).astype('float64')
    
    return df
    