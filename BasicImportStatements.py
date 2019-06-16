## Basic Imports
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
%matplotlib inline
import seaborn as sns
sns.set_style("darkgrid")

import copy

import os
from datetime import date, datetime, timedelta
path = "/home/Outputs"


#pd.set_option('display.height', 1000)
#pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
#pd.set_option('display.width', 1000)

pd.options.display.float_format = '{:,.3f}'.format
##########################################################


import warnings
warnings.filterwarnings('ignore')
warnings.filterwarnings(action='once')

