import pandas as pd
from setup.initialize import logger

df = pd.read_excel('C:/Users/Benjamin Bagi/Documents/Uni/Masterarbeit/sim.xlsx')
df_split = df.iloc[:, 0].str.split(r'\s{4}', expand=True)
logger.info(df_split.dtypes)
df_split.iloc[:, 0] = pd.to_numeric(df_split.iloc[:, 0], errors='coerce')
df_split.iloc[:, 1] = pd.to_numeric(df_split.iloc[:, 1], errors='coerce')
df_first_part = df_split.iloc[:301, :-1] #125-176
df_first_part = df_first_part.iloc[125:176, :].reset_index(drop=True)
df_first_part.columns = ['w in um', 'Electric displacement field in C/m']
#df_first_part.to_excel('C:/Users/Benjamin Bagi/Documents/Uni/Masterarbeit/sim_ff.xlsx', index=False)
df_second_part = df_split.iloc[303:, :-1].reset_index(drop=True) #428-479
df_second_part = df_second_part.iloc[125:176, :].reset_index(drop=True)
df_second_part.columns = ['w in um', 'Electric displacement field in C/m']
#df_second_part.to_excel('C:/Users/Benjamin Bagi/Documents/Uni/Masterarbeit/sim_mf.xlsx', index=False)
logger.info('done')