import pandas as pd
pd.set_option('display.max_columns', None)

df = pd.read_csv('doctors.txt', sep='\s+:', engine='python')
df.info()


#print(df.values)
#print(df.columns)
#print(df.index)


