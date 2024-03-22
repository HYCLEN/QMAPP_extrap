# -*- coding: utf-8 -*-
"""
%% Example implementation of quantile mapping to correct bias of outliers falling outside of base CDF
% Sample data: daily total precipitation of July for the reference period (1995-2004) and target period (2085-2094)
%             (1) 'OBS_1995-2004': observed data
%             (2) 'HR_1995-2004': historical run of Regional Climte Model(RCM)   
%             (3) 'CCR_2085-2094': future climate change run of RCM


Created on Thu Mar 7  12:20:17 2024

@author: Kyuhyun Byun
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from QMAPP_extrap import QMAPP_extrap

def Cunnane_CDF(data):
    sorted_data = np.sort(data)[::-1]
    n = len(data)
    q = (np.arange(1, n + 1) - 0.4) / (n + 0.2)
    return q, sorted_data

# Import data
df = pd.read_csv("P_sample.csv")
P_OBS = df.iloc[:, 0].values
P_HR = df.iloc[:, 1].values
P_CCR = df.iloc[:, 2].values

# Main process: Bias correction using quantile mapping
P_CCR_BC = QMAPP_extrap(P_OBS, P_HR, P_CCR, 0)

#%% Plot results
x_or, y_or = Cunnane_CDF(P_OBS)
x_mr, y_mr = Cunnane_CDF(P_HR)
x_bef, y_bef = Cunnane_CDF(P_CCR)
x_af, y_af = Cunnane_CDF(P_CCR_BC)

plt.figure(figsize=(15, 17))

# Flag values falling outside of the range of historical CDF
idx = np.where(y_bef > max(y_mr))[0]

# Plot before correction
plt.subplot(2, 1, 1)
plt.plot(x_or, y_or, 'k-o', label='Observed', markersize=6)
plt.plot(x_mr, y_mr, 'b-s', label='Historical Simulation', markersize=6)
plt.plot(x_bef[idx[-1]:], y_bef[idx[-1]:], 'g-d', label='Raw Future Simulation', markeredgecolor='k', markerfacecolor='g', markersize=6)
plt.plot(x_bef[idx], y_bef[idx], 'r-d', label='Raw Future Simulation (Extrapolation Needed)', markeredgecolor='k', markerfacecolor='r', markersize=6)
plt.xlabel('Probability of Exceedance', fontweight='bold')
plt.ylabel('Daily Total Precipitation (mm)', fontweight='bold')
plt.xlim([0, 0.025])
plt.xticks(fontsize=13)
plt.yticks(fontsize=13)
plt.legend(loc='upper right', fontsize=13)
plt.grid(True)

# Plot after correction
plt.subplot(2, 1, 2)
plt.plot(x_or, y_or, 'k-o', label='Observed', markersize=6)
plt.plot(x_mr, y_mr, 'b-s', label='Historical Simulation', markersize=6)
plt.plot(x_af, y_af, 'r-*', label='Bias-Corrected Future Simulation', markeredgecolor='r', markerfacecolor='r', markersize=6)
plt.xlabel('Probability of Exceedance', fontweight='bold')
plt.ylabel('Daily Total Precipitation (mm)', fontweight='bold')
plt.xlim([0, 0.025])
plt.xticks(fontsize=13)
plt.yticks(fontsize=13)
plt.legend(loc='upper right', fontsize=13)
plt.grid(True)
