"""################### Importando os Pacotes ######################"""
#import pandas as pd
#import numpy as np
#import json
#from statsmodels.tsa.seasonal import seasonal_decompose
#import matplotlib.pyplot as plt
#import seaborn as sns
#from datetime import datetime as dt
#import math
#from scipy.optimize import curve_fit
#sns.set_style()



"""###################  Fonte dos dados ################### """
def extracao():

    import requests

    url = "https://api.covid19api.com/total/country/brazil"
    payload = {}
    headers= {} 
    response = requests.request("GET", url, headers=headers, data = payload)
    json_list = response.json()

    return json_list
