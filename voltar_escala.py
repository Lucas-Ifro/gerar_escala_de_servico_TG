import pandas as pd
import os

def voltar_escala(data_da_escala):
    try:
        print(f'./copia_csv/atiradores/atiradores_copy_{data_da_escala}.csv')
        df_atiradores = pd.read_csv(f'./copia_csv/atiradores/atiradores_copy_{data_da_escala}.csv', header=0)
        df_monitores = pd.read_csv(f'./copia_csv/monitores/monitores_copy_{data_da_escala}.csv', header=0)
        df_atiradores.to_csv(f'./atiradores.csv', index=False)
        df_monitores.to_csv(f'./monitores.csv', index=False)

        arquivos = [f'./copia_csv/atiradores/atiradores_copy_{data_da_escala}.csv', 
                    f'./copia_csv/monitores/monitores_copy_{data_da_escala}.csv',
                    f'./escalas/escala_servico_dia_{data_da_escala}.csv']
        
        for arquivo in arquivos:
            if os.path.exists(arquivo):
                os.remove(arquivo)
                print("Arquivo apagado com sucesso!")
    except:
        print("Ocorreu um erro: Verifique se a data está correta, e se está no formato correto.\nVocê deve colocar a data do primeiro dia da escala que deseja voltar.\n É a mesma data que fica salva no arquivo da escala que foi gerada errada.")

if __name__ == "__main__":
    # 1-Imagine que você gerou uma escala errada, faltou colocar o dia de folga ou feriado por exemplo.
    # Aqui você vai voltar no passado, e gerar uma nova escala adicionando esse dia de feriado.
    # Primeiramente você deve colocar a data de inicio da escala que você fez errado.
    # E executar, Pronto, a escala que você gerou errado foi apagada.
    # se você gerou mais de uma escala errada, coloque a data da primeira escala que foi errada, 
    # e pronto tudo voltará ao estado de quando você não gerou a escala.

    # 2-Depois de executar esse codigo, volte ao gerador_de_escala.py e gere as escalas novamente.
    # COMO EXECUTAR: segure, CTHL + J, o terminal abrirá
    # DIGITE O COMANDO: python voltar_escala.py e aperte Enter
    # PRONTO
    voltar_escala(data_da_escala="2024-10-02")