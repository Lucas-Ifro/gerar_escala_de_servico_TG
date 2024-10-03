import pandas as pd
import ast
from datetime import datetime, timedelta

def ordenar_df(df, coluna):
    df[coluna] = pd.to_datetime(df[coluna])
    return df.sort_values(by=coluna).reset_index(drop=True)

def type_colunas(df):
    df["ultima_escala_preta"] = pd.to_datetime(df["ultima_escala_preta"])
    df["ultima_escala_vermelha"] = pd.to_datetime(df["ultima_escala_vermelha"])
    return df

def gerarEscala(data_inicio, quantidade_de_dias, quantidade_sentinelas, feriados=[], folgas=[]):
    data_convertida = datetime.strptime(data_inicio, "%Y-%m-%d")
    feriados = [datetime.strptime(data, "%Y-%m-%d") for data in feriados]
    folgas = [datetime.strptime(data, "%Y-%m-%d") for data in folgas]
    df_escala_dict = []
    df_atiradores = pd.read_csv('./atiradores.csv', header=0)
    df_monitores = pd.read_csv('./monitores.csv', header=0)
    df_atiradores = type_colunas(df_atiradores)
    df_monitores = type_colunas(df_monitores)

    data_str = data_convertida.strftime("%Y-%m-%d")
    df_atiradores.to_csv(f'./copia_csv/atiradores/atiradores_copy_{data_str}.csv', index=False)
    df_monitores.to_csv(f'./copia_csv/monitores/monitores_copy_{data_str}.csv', index=False)
    

    for i in range(quantidade_de_dias):
        data_da_escala = data_convertida + timedelta(days=i)

        if (data_da_escala.weekday() < 5) & (data_da_escala not in feriados) & (data_da_escala not in folgas):
            escala_do_dia = {'data':data_da_escala.strftime("%Y-%m-%d")}
            dia_anterior = data_da_escala + timedelta(days=-1)
            
            for comandante in range(len(df_monitores)):
                
                df_monitores = ordenar_df(df_monitores,'ultima_escala_preta')

                disponibilidade = ast.literal_eval(df_monitores.loc[comandante,'disponibilidade'])
                ultimo_servico_preta = df_monitores.loc[comandante,'ultima_escala_preta']
                ultimo_servico_vermelha = df_monitores.loc[comandante,'ultima_escala_vermelha']

                if (data_da_escala.weekday() in disponibilidade) & (ultimo_servico_preta != dia_anterior) & (ultimo_servico_vermelha != dia_anterior):
                    nome = df_monitores.loc[comandante,'nome']
                    escala_do_dia['comandante'] = nome
                    df_monitores.loc[comandante,'ultima_escala_preta'] = data_da_escala.strftime("%Y-%m-%d")
                    break
            else:
                print(f"não foi possivel gerar uma escala para o dia {escala_do_dia}")
                escala_do_dia['comandante'] = f"não foi possivel gerar uma escala para o dia {escala_do_dia}"

            n_sent = 1
            for qtd in range(quantidade_sentinelas):
                for sentinela in range(len(df_atiradores)):
                    df_atiradores = ordenar_df(df_atiradores,'ultima_escala_preta')

                    disponibilidade = ast.literal_eval(df_atiradores.loc[sentinela,'disponibilidade'])
                    ultimo_servico_preta = df_atiradores.loc[sentinela,'ultima_escala_preta']
                    ultimo_servico_vermelha = df_atiradores.loc[sentinela,'ultima_escala_vermelha']

                    if (data_da_escala.weekday() in disponibilidade) & (ultimo_servico_preta != dia_anterior) & (ultimo_servico_vermelha != dia_anterior):
                        nome = df_atiradores.loc[sentinela,'nome']
                        escala_do_dia[f"sent{n_sent}"] = nome
                        df_atiradores.loc[sentinela,'ultima_escala_preta'] = data_da_escala.strftime("%Y-%m-%d")
                        n_sent += 1
                        break
                else:
                    print(f"não foi possivel gerar uma escala para o dia {escala_do_dia}")
                    escala_do_dia = {'data':data_da_escala.strftime("%Y-%m-%d")}
                    escala_do_dia['comandante'] = f"não foi possivel gerar uma escala para o dia {escala_do_dia}"

        elif ((data_da_escala.weekday() >= 5) | (data_da_escala in feriados)) & (data_da_escala not in folgas):
            escala_do_dia = {'data':data_da_escala.strftime("%Y-%m-%d")}
            dia_anterior = data_da_escala + timedelta(days=-1)
            
            for comandante in range(len(df_monitores)):
                
                df_monitores = ordenar_df(df_monitores,'ultima_escala_vermelha')

                disponibilidade = ast.literal_eval(df_monitores.loc[comandante,'disponibilidade'])
                ultimo_servico_preta = df_monitores.loc[comandante,'ultima_escala_preta']
                ultimo_servico_vermelha = df_monitores.loc[comandante,'ultima_escala_vermelha']

                if (data_da_escala.weekday() in disponibilidade) & (ultimo_servico_preta != dia_anterior) & (ultimo_servico_vermelha != dia_anterior):
                    nome = df_monitores.loc[comandante,'nome']
                    escala_do_dia['comandante'] = nome
                    df_monitores.loc[comandante,'ultima_escala_vermelha'] = data_da_escala.strftime("%Y-%m-%d")
                    break
            else:
                print(f"não foi possivel gerar uma escala para o dia {data_da_escala}")
                escala_do_dia['comandante'] = f"não foi possivel gerar uma escala para o dia {data_da_escala}"

            n_sent = 1
            for qtd in range(quantidade_sentinelas):
                for sentinela in range(len(df_atiradores)):
                    df_atiradores = ordenar_df(df_atiradores,'ultima_escala_vermelha')
                    disponibilidade = ast.literal_eval(df_atiradores.loc[sentinela,'disponibilidade'])
                    ultimo_servico_preta = df_atiradores.loc[sentinela,'ultima_escala_preta']
                    ultimo_servico_vermelha = df_atiradores.loc[sentinela,'ultima_escala_vermelha']

                    if (data_da_escala.weekday() in disponibilidade) & (ultimo_servico_preta != dia_anterior) & (ultimo_servico_vermelha != dia_anterior):
                        nome = df_atiradores.loc[sentinela,'nome']
                        escala_do_dia[f"sent{n_sent}"] = nome
                        df_atiradores.loc[sentinela,'ultima_escala_vermelha'] = data_da_escala.strftime("%Y-%m-%d")
                        n_sent += 1
                        break
                else:
                    print(f"não foi possivel gerar uma escala para o dia {data_da_escala}")
                    escala_do_dia = {'data':data_da_escala.strftime("%Y-%m-%d")}
                    escala_do_dia['comandante'] = f"não foi possivel gerar uma escala para o dia {data_da_escala}"
        else:
            print("folga")
        df_escala_dict.append(escala_do_dia)

    df_escala_finalizada = pd.DataFrame(df_escala_dict)
    print(df_escala_dict)

    df_escala_finalizada.to_csv(f'./escalas/escala_servico_dia_{data_str}.csv', index=False)

if __name__ == "__main__":
    gerarEscala(data_inicio="2024-10-01", quantidade_de_dias=60, quantidade_sentinelas=3, feriados=[], folgas=["2024-10-05","2024-10-04"])