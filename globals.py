import pandas as pd
import os

if ("df_despesa.csv" in os.listdir()) and ("df_receita.csv" in os.listdir()):
    df_despesa = pd.read_csv("df_despesa.csv", index_col=0, parse_dates=True)
    df_receita = pd.read_csv("df_receita.csv", index_col=0, parse_dates=True)

else:
    data_structure = {
        'Valor': [],
        'Efetuado': [],
        'Fixo': [],
        'Data': [],
        'Categoria': [],
        'Descrição': [],
    }
    df_receita = pd.DataFrame(data_structure)
    df_despesa = pd.DataFrame(data_structure)
    df_despesa.to_csv("df_despesa.csv")
    df_receita.to_csv("df_receita.csv")

if ("df_cat_despesa.csv" in os.listdir()) and ("df_cat_receita.csv" in os.listdir()):
    df_cat_despesa = pd.read_csv(
        "df_cat_despesa.csv", index_col=0, parse_dates=True)
    df_cat_receita = pd.read_csv(
        "df_cat_receita.csv", index_col=0, parse_dates=True)
    cat_receita = df_cat_receita.values.tolist()
    cat_despesa = df_cat_despesa.values.tolist()

else:
    cat_receita = {'Categoria': ["Salário", "Envestimentos", "Comissão"]}
    cat_despesa = {'Categoria': ["Alimentação",
                                 "Aluguel", "Transporte", "Saúde", "Lazer"]}

    df_cat_receita = pd.DataFrame(cat_receita)
    df_cat_despesa = pd.DataFrame(cat_despesa)
    df_cat_despesa.to_csv("df_cat_despesa.csv")
    df_cat_receita.to_csv("df_cat_receita.csv")
