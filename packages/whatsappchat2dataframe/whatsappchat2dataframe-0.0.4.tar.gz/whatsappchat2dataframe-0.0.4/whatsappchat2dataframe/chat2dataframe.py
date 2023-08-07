"""
This module implements the main functionality of whatsappchat2dataframe.
Author: Kiran Busch
"""

import re
from tqdm import tqdm
import pandas as pd

class Converter:
    def __init__(self) -> None:
        pass

    def chat2dataframe(self,path_to_filename:str):
        """converts a whatsappchat (.txt file) into a pandas dataframe

        Args:
            path_to_filename (str): path to file e.g. data/chat.txt

        Returns:
            pd.DataFrame: return a pandas DataFrame of the .txt file
        """
        self.DATE_TIME = re.compile(r"([\[]).*?([\]])")
        self.DATE_TIME = re.compile(r"[\[]*[0-9]+[\./][0-9]+[\./][0-9]+..[0-9]+:[0-9]+[:]*([0-9]+)*[\]]*[-]*")
        self.AUTHOR = re.compile(r"((( [a-zA-ZöäüÖÄÜ]+)+):)")
        self.LTR = chr(8206)
        try:
            with open(path_to_filename, 'r') as file:
                self.data = file.read().replace('\n', '')
        except Exception as e:
            print(f"Could not process {path_to_filename}, because the following error occured: {type(e).__name__}: {str(e)}")
        

        df = pd.DataFrame(self.__chat2df(data=self.data), columns=["DateTime", "Author", "Message"])
        df['DateTime'] = df['DateTime'] + pd.to_timedelta(df.groupby('DateTime').cumcount(), unit='ms')
        df['numMessage']=1
        return df

    def __to_pd_row(self, s):
        match = self.DATE_TIME.match(s)
        if match:
            g = match.group(0)
            date_time = g.replace('[','').replace(']','').replace(' ','').split(',')
            author = re.search(self.AUTHOR, s).group(0)[1:-1]
            message = s.split(': ')[1]
            return self.__try_parsing_date(date_time), author, message.replace("\n", "")
        
    def __chat2df(self,data):
        start_positions_date = [m.start() for m in re.finditer(self.DATE_TIME, data)]
        for start,end in tqdm(list(zip(start_positions_date[:-1],start_positions_date[1:])), desc='Read messages'):
            subdata = data[start:end]
            if len(self.AUTHOR.findall(subdata))>0:
                yield self.__to_pd_row(subdata.replace(self.LTR, ""))
    
    def __try_parsing_date(self,date_time):
        for fmt in ("%d.%m.%y-%H:%M:%S", "%Y/%m/%d-%H:%M:%S", "%d/%m/%y-%H:%M", "%d.%m.%y-%H:%M"):
            try:
                return pd.to_datetime(f'{date_time[0]}-{date_time[1]}', format=fmt)
            except ValueError:
                pass
        raise ValueError(f'no valid date format found for "{str(date_time[0])}-{str(date_time[1])}"')