# -*- coding: utf-8 -*-

import numpy as np
import scipy as sp

import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import pandas_talib as pdta

import csv

#----------code.init
mpl.style.use('seaborn-whitegrid');

def do_MOM(file_name):
    df = pd.read_csv(file_name,encoding='gbk');
    df = pdta.MOM(df,3);

    size = df['Momentum_3'].size;
    
    return [(df['Momentum_3'][size-1] - df['Momentum_3'][size-3]),(df['Momentum_3'][size-1] - df['Momentum_3'][size-2])]

def do_MACD(file_name):
    df = pd.read_csv(file_name,encoding='gbk');
    df = pdta.MACD(df,4,12);

    size = df['MACDdiff_4_12'].size

    return [(df['MACDdiff_4_12'][size-1] - df['MACDdiff_4_12'][size-2]),df['MACDdiff_4_12'][size-1]]








