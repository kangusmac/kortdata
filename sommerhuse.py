import pandas as pd
from pathlib import Path
import json

datafolder =Path("datafolder_Alledata")
datamappe_sommerhuse = Path("datamappe-sommerhuse")
data_fil = Path("sommerhuse_2024_03_10.csv")
# join the path with the filename
data_fil = datamappe_sommerhuse / data_fil


files = list(datafolder.glob("*.json"))

def get_data_from_file(file):
    data = json.loads(file.read_text())
    return data

oplysninger = [get_data_from_file(file) for file in files]

def get_key_value_pairs(d):
    #return {k: v for k, v in d.items() if k != "Datoer"}.update(d['Datoer'])
    pik = {k: v for k, v in d.items() if k != "Datoer"}
    pik.update(d['Datoer'])
    return pik

def mygeodata(dato):
    myg = pd.DataFrame(dato).set_index('Henvisning')
    return SOMMERHUSE.loc[myg.index][['Placering','latitude','longitude']]


SOMMERHUSE  = pd.concat([pd.DataFrame([get_key_value_pairs(d)]) for d in oplysninger], axis=0, ignore_index=True)
#SOMMERHUSE = pd.read_csv(data_fil)

SOMMERHUSE['Placering'] = SOMMERHUSE['Placering'].str.replace('Gr Hoved', 'Grønninghoved')


sommergeo = pd.read_csv('sommergeo.csv')
# # rename column 'input_string' to 'Placering'
sommergeo = sommergeo.rename(columns={'input_string':'Placering'})
geodata = sommergeo[['Placering','latitude','longitude']]
SOMMERHUSE = pd.merge(SOMMERHUSE, geodata, on='Placering', how='left')


if __name__ == "__main__":
    #print(SOMMERHUSE.head())
#    print(geodata.head())
    # if SOMMERHUSE['Placering'].equals(geodata['Placering']):
    #     print('equal')
    print(type(SOMMERHUSE).loc[0,'latitude'])

