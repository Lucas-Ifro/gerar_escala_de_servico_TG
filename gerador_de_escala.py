import pandas as pd
from datetime import datetime, timedelta

def gerarEscala(data_inicio, quantidade_de_dias, quantidade_sentinelas, feridos=None, folga=None):
    data_convertida = datetime.strptime(data_inicio, "%Y-%m-%d")
    data_convertida = data_convertida + timedelta(days=-1)
    df_escala = pd.DataFrame(['comandante','cent1','cent2','cent3','data'])
    df_escala_dict = None

    for i in range(quantidade_de_dias):
        data_da_escala = data_convertida + timedelta(days=i)

        df_atiradores = pd.read_csv('./atiradores.csv', header=0)
        df_monitores = pd.read_csv('./monitores.csv', header=0)

        df_atiradores['ultima_escala_preta'] = pd.to_datetime(df_atiradores['ultima_escala_preta'])
        df_atiradores_sorted = df_atiradores.sort_values(by='ultima_escala_preta')

        df_monitores['ultima_escala_preta'] = pd.to_datetime(df_monitores['ultima_escala_preta'])
        df_monitores_sorted = df_monitores.sort_values(by='ultima_escala_preta')

        if data_da_escala.weekday() < 5:
            # print(data_da_escala.strftime("%Y-%m-%d"))
            for sentinela in range(quantidade_sentinelas):
                print(None)
        else:
            print("fim de semana")
    return None

if __name__ == "__main__":
    gerarEscala("2024-09-10", 10)