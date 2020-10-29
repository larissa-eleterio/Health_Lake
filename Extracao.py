"""################### Importando os Pacotes ######################"""
import pandas as pd
import numpy as np
import requests
import json
from statsmodels.tsa.seasonal import seasonal_decompose
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime as dt
import math
from scipy.optimize import curve_fit
sns.set_style()



"""###################  Fonte dos dados ################### """

url = "https://api.covid19api.com/total/country/brazil"

payload = {}
headers= {} 
response = requests.request("GET", url, headers=headers, data = payload)

json_list = response.json()
#df = pd.json_normalize(json_list)
