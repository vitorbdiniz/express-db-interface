import pandas as pd
from pandas.core.dtypes.missing import notna
import main.reader.DQL as reader
import main.writer.DML as writer
import main.generator.go_interface as go


def get_durations(df):

    if type(df) == pd.DataFrame:
        for i in df.index:
            tempo = reader.get_duration(df['Tempo Vídeo'].loc[i])
            print(tempo)
    else:
        tempo = reader.get_duration(df)
        print(tempo)

def add_test():
    
    query = """
        SELECT L.Id, S.Id
        FROM Subscription S
                RIGHT JOIN Module M ON M.CourseId=S.CourseId
                RIGHT JOIN Lecture L ON L.ModuleId=M.Id
        WHERE S.UserId='y1f9eyo93idrx8smca5pgntcha'
        ORDER BY S.Id, L.Id
        ;
    """  
    query_result = writer.execute_query(query)

    DML_code = "INSERT INTO Annotation VALUES"
    for i in range(query_result.shape[0]):
        DML_code += f"('{generate_id()}', '{query_result[0].iloc[i]}', '{query_result[1].iloc[i]}', 'Teste para Locust', {get_time()}, 1)"
        DML_code += ',' if i != query_result.shape[0]-1 else ';'
    writer.execute_DML(DML_code)
    return DML_code

def generate_id():
    return go.go_get_id()

def get_time():
    return go.get_date()

#name = 'Cyber Security.csv'

#data = pd.read_csv(f'~/Downloads/TCSchool - files/{name}')
#result = get_durations(data)

#get_durations('00:15:08')

#print( generate_id() )
#print( get_time() )

print(add_test())