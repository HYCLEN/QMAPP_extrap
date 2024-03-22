# -*- coding: utf-8 -*-
"""
%% Example implementation of quantile mapping to correct bias of outliers falling outside of base CDF
% Sample data: daily maximum temperature(Tmax) of July for the reference period (1995-2004) and target period (2085-2094)
%             (1) 'OBS_1995-2004': observed data
%             (2) 'HR_1995-2004': historical run of Regional Climte Model(RCM)   
%             (3) 'CCR_2085-2094': future climate change run of RCM


Created on Thu Mar 11  11:13:18 2024

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
df = pd.read_csv("Tmax_sample.csv")
Tmax_OBS = df.iloc[:, 0].values
Tmax_HR = df.iloc[:, 1].values
Tmax_CCR = df.iloc[:, 2].values

# Main process: Bias correction using quantile mapping
Tmax_CCR_BC = QMAPP_extrap(Tmax_OBS, Tmax_HR, Tmax_CCR, 'None')

#%% Plot results
x_or, y_or = Cunnane_CDF(Tmax_OBS)
x_mr, y_mr = Cunnane_CDF(Tmax_HR)
x_bef, y_bef = Cunnane_CDF(Tmax_CCR)
x_af, y_af = Cunnane_CDF(Tmax_CCR_BC)

plt.figure(figsize=(15, 17))

# Flag values falling outside of the range of historical CDF
idx_out = np.where(y_bef > np.max(y_mr))[0]

# Plot before correction
plt.subplot(2, 1, 1)
plt.plot(x_or, y_or, 'k-o', markersize=6, label='Observed')
plt.plot(x_mr, y_mr, 'b-s', markersize=6, label='Historical Simulation')
plt.plot(x_bef[idx_out[-1]:], y_bef[idx_out[-1]:], 'g-d', markeredgecolor='k', markerfacecolor='g', markersize=6, label='Raw Future Simulation')
plt.plot(x_bef[idx_out], y_bef[idx_out], 'r-d', markeredgecolor='k', markerfacecolor='r', markersize=6, label='Raw Future Simulation Needing Extrapolation')
plt.plot([0, 1], [np.max(y_mr), np.max(y_mr)], 'b--')

plt.xlabel('Probability of Exceedance', fontweight='bold')
plt.ylabel('Daily Maximum Temperature (°C)', fontweight='bold')
plt.xlim([0, 0.28])
plt.ylim([27, 47])
plt.xticks(fontsize=13)
plt.yticks(fontsize=13)
plt.legend(loc='upper right', fontsize=12)
plt.grid(True)

# After correction
plt.subplot(2, 1, 2)
plt.plot(x_or, y_or, 'k-o', markersize=6, label='Observed')
plt.plot(x_mr, y_mr, 'b-s', markersize=6, label='Historical Simulation')
plt.plot(x_af, y_af, 'r-*', markeredgecolor='r', markerfacecolor='r', markersize=6, label='Bias-Corrected Future Simulation')
plt.plot([0, 1], [np.max(y_or), np.max(y_or)], 'k--')

plt.xlabel('Probability of Exceedance', fontweight='bold')
plt.ylabel('Daily Maximum Temperature (°C)', fontweight='bold')
plt.xlim([0, 0.28])
plt.ylim([27, 47])
plt.xticks(fontsize=13)
plt.yticks(fontsize=13)
plt.legend(loc='upper right', fontsize=12)
plt.grid(True)

plt.show()