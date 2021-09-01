import pandas as pd
from pandas.core.dtypes.missing import notna
import main.reader.DQL as reader
import main.generator.go_interface as go


def get_durations(df):

    if type(df) == pd.DataFrame:
        for i in df.index:
            tempo = reader.get_duration(df['Tempo Vídeo'].loc[i])
            print(tempo)
    else:
        tempo = reader.get_duration(df)
        print(tempo)


def generate_id():
    return go.go_get_id()

def get_time():
    return go.get_date()

#name = 'Cyber Security.csv'

#data = pd.read_csv(f'~/Downloads/TCSchool - files/{name}')
#result = get_durations(data)

get_durations('00:45:35')

#print( generate_id() )
#print( get_time() )

