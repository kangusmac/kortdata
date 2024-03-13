
from pathlib import Path
import json
from sommerhuse import SOMMERHUSE
import pandas as pd
from datetime import datetime
from enum import Enum
import uuid


class Måneder(Enum):
    jan = 1
    feb = 2
    mar = 3
    apr = 4
    maj = 5
    jun = 6
    jul = 7
    aug = 8
    sep = 9
    okt = 10
    nov = 11
    dec = 12

    @classmethod
    def from_string(cls, string):
        try:
            return cls[string.lower()]
        except KeyError:
            raise ValueError()
    


# Create an enum class that translates the english weekday names to danish
class Ugedage(Enum):
    Monday = "Mandag"
    Tuesday = "Tirsdag"
    Wednesday = "Onsdag"
    Thursday = "Torsdag"
    Friday = "Fredag"
    Saturday = "Lørdag"
    Sunday = "Søndag"

    @classmethod
    def from_string(cls, string):
        try:
            return cls[string]
        except KeyError:
            raise ValueError()

#oversættelse = { "jan" : "Jan", "feb" : "February", "mar" : "March", "apr" : "April", "may" : "maj"
        


datafolder =Path("datafolder_Alledata")

files = list(datafolder.glob("*.json"))

def get_data_from_file(file):
     data = json.loads(file.read_text())
     return data

# get the data from the files
oplysninger = [get_data_from_file(file) for file in files]

def get_key_value_pairs(d):
     #return {k: v for k, v in d.items() if k != "Datoer"}.update(d['Datoer'])
     pik = {k: v for k, v in d.items() if k != "Datoer"}
     pik.update(d['Datoer'])
     return pik

#SOMMERHUSE  = pd.concat([pd.DataFrame([get_key_value_pairs(d)]) for d in oplysninger], axis=0, ignore_index=True)
#SOMMERHUSE = pd.read_csv("datamappe-sommerhuse/sommerhuse.csv")

def hent_dato(måned):
    month = måned.name
    #month = datetime.strptime(month, '%b').month
    month = Måneder.from_string(month).value
    year = datetime.now().year
    #måned = måned.dropna()
    måned = måned[~måned.isna()]
    return måned.explode().apply(lambda x: f"{x} {month} {year}")


def  kalender(måned=None):
    if måned is None:
        current_month = datetime.now().strftime('%b').lower()
    else:
        current_month = måned
    mym = hent_dato(SOMMERHUSE[current_month])
    mym = pd.DataFrame(mym)
    mym = mym.reset_index()
    mym.columns = ["Henvisning","Dato"]
    mym["Dato"] = pd.to_datetime(mym["Dato"], format='%d %m %Y')
    mym["Ugedag"] = mym["Dato"].dt.day_name()
    #mym["Ugedag"] = mym["Ugedag"].apply(lambda x: Ugedage.from_string(x).value)
    mym_gr = mym.groupby(["Dato","Henvisning"]).count()
    mymidx = mym_gr.index.unique(level=0)
    mymholder = []
    for d in mymidx:

        df = SOMMERHUSE.loc[mym_gr.loc[(d,)].index]['Placering']
        df = df.reset_index()
        #df.drop(columns="Henvisning", inplace=True)
        df['Dato'] = d
    
        mymholder.append(df)
    return mymholder

def datoer_i_måned(måned=None):
    måned = kalender(måned)
    datoer = dict()
    for dag in måned:
        dato = dag['Dato'].unique()[0]
        # remove the time from the date
        dato = dato.date()
        #datoer[dato] = dag['Placering'].to_list()
        datoer[dato] = dag[['Placering','Henvisning']].to_dict('records')
    # sortere datoer efter dato
    datoer = {k: v for k, v in sorted(datoer.items(), key=lambda item: item[0])}
    return datoer
    

if __name__ == "__main__":

    #test = kalender()
    måned = "mar"
    #test = kalender(måned)
    for x in SOMMERHUSE[måned].explode().apply(lambda x: f"{x} {måned} {datetime.now().year}"):
        print(x)
    #print(test[1])


