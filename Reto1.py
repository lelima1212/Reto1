import gspread 
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
import pandas as pd
from gspread_dataframe import set_with_dataframe


scope = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file", 'https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)

client = gspread.authorize(creds)

sheets = client.open("Data TEST")

ws = sheets.worksheet("Reto1")

data = ws.get_all_records()

df=pd.DataFrame(data)
#Only in the first execution because create the worksheet, not quite the comment
#salida = sheets.add_worksheet(title = "SalidaReto1", rows = 100, cols = 20)
salida2= sheets.worksheet('SalidaReto1')

pt = df.reset_index().pivot_table(values=['Country'],columns=[df.Country],index=['Author','Sentiment'], aggfunc=lambda x: bool('TRUE'),fill_value='False')
pt2 = df.reset_index().pivot_table(values=['Theme'],columns=[df.Theme],index=['Author','Sentiment'], aggfunc=lambda x: bool('TRUE'), fill_value='False')
pt_concat = pd.concat([pt,pt2],1,join="inner")

set_with_dataframe(salida2, pt_concat, include_index=True)

pprint (pt_concat)

