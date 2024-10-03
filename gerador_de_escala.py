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
        dia_de_folga = False
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
                    nome = df_atiradores.loc[sentinela,'nome']

                    if (data_da_escala.weekday() in disponibilidade) & (ultimo_servico_preta != dia_anterior) & (ultimo_servico_vermelha != dia_anterior) & ("rod" not in nome.lower()):
                        escala_do_dia[f"sent{n_sent}"] = nome
                        df_atiradores.loc[sentinela,'ultima_escala_vermelha'] = data_da_escala.strftime("%Y-%m-%d")
                        n_sent += 1
                        break
                else:
                    print(f"não foi possivel gerar uma escala para o dia {data_da_escala}")
                    escala_do_dia = {'data':data_da_escala.strftime("%Y-%m-%d")}
                    escala_do_dia['comandante'] = f"não foi possivel gerar uma escala para o dia {data_da_escala}"
        else:
            dia_de_folga = True
            
        if not dia_de_folga:
            df_escala_dict.append(escala_do_dia)

    df_escala_finalizada = pd.DataFrame(df_escala_dict)
    print(df_escala_dict)

    df_escala_finalizada.to_csv(f'./escalas/escala_servico_dia_{data_str}.csv', index=False)
    df_atiradores.to_csv(f'./atiradores.csv', index=False)
    df_monitores.to_csv(f'./monitores.csv', index=False)

if __name__ == "__main__":
    # 1- COMO EXECUTAR: segure, CTHL + J, o terminal abrirá
    # DIGITE O COMANDO: python gerador_de_escala.py e aperte Enter
    # PRONTO NA PASTA ESCALAS APARECERA UMA ESCALA COM A DATA IGUAL QUE VOCÊ UTILIZOU NO dia_inicio.

    gerarEscala(data_inicio="2024-10-02", 
                quantidade_de_dias=60, 
                quantidade_sentinelas=3, 
                feriados=["2024-10-08"], 
                folgas=["2024-10-04"])
    
    # 2- Como configurar os arquivos CSV, atiradores.csv e monitores.csv

    # nome,ultima_escala_preta,ultima_escala_vermelha,disponibilidade
    # nome: é o nome do atirador ou monitor
    # ultima_escala_preta: é o ultimo dia que ele tirou serviço em dia de semana.
    # ultima_escala_vermelha: é o ultimo dia que ele tirou serviço em fim de semana.
    # PRINCIPAL
    # disponibilidade: Aqui você pode configurar para um pessoa não tirar serviço em um determinado dia da semana.
    # Exemplo: Saurin, ele não pode tirar serviço no sábado.
    # para isso existe uma lista: "[0, 1, 2, 3, 4, 5, 6]" ela vai de segunda a domingo.
    # sendo 0 a segunda e 6 o domingo. se eu não posso tirar serviço na terça, eu apenas removo o 1 da lista.


    # 3- Parâmetros da chamada da função gerarEscala():

    # data_inicio: Data de início da escala no formato YYYY-MM-DD.(ano-mês-dia)
    # exemplo: "2024-10-02" isso funciona, "2024-10-2" isso não funciona, tem que ter o zero antes do 2.
    # Então se é dia 2 coloca 02 se é mês 5 coloca 05. E a ordem é, ano-mês-dia

    # quantidade_de_dias: Quantidade total de dias para gerar a escala.
    # quantidade_sentinelas: Número de sentinelas por dia.

    # feriados: Lista de datas de feriados no formato YYYY-MM-DD. (ano-mês-dia) os feriados entram para a escala vermelhar
    # folgas: Lista de datas de folgas no formato YYYY-MM-DD. (ano-mês-dia) esse dia não havera guarnição
    # As datas da lista seguem a quele mesmo formato, 
    # e caso tenha mais de um dia de folga ou feriado os dias tem quer ser separado por vírgula.
    # Exemplo: feriados=["2024-10-08", "2024-10-09", "2024-10-10", "2024-10-08"], 
    # Exemplo: folgas=["2024-10-08", "2024-10-01", "2024-10-07", "2024-10-04"]

    # 4- IMPORTANTE:

    # datas tem quer estar entre aspas duplas, e tem que estar no formato correto.
    # A data de início deve ser a data apos a ultima escala gerada, se não escala passada foi até o dia 03, a data_inicio será 04.
    
    # 5- Exemplos de chamada para executar

    # gerarEscala(data_inicio="2024-10-10", 
    #         quantidade_de_dias=15, 
    #         quantidade_sentinelas=3, 
    #         feriados=[], 
    #         folgas=["2024-10-04", "2024-10-04"])

    # A chamada acima gerou a escala até o dia 25, então na proxima eu gero com a data_inicio dia 26.

    # gerarEscala(data_inicio="2024-10-26", 
    #         quantidade_de_dias=15, 
    #         quantidade_sentinelas=3, 
    #         feriados=["2024-10-04", "2024-10-04"], 
    #         folgas=[])