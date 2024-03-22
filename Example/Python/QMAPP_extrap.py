# -*- coding: utf-8 -*-
"""
Created on Thu Mar 7  16:25:17 2024

@author: Kyuhyun Byun

"""

import numpy as np

def QMAPP_extrap(Target_CDF, Base_CDF, DATA, min_bound=None):
    # Make Output vector having the same length with DATA
    Output = np.zeros_like(DATA)

    # Unbiased quantile estimator (Cunnane formulation)
    Rank_Target_CDF = np.arange(1, len(Target_CDF) + 1)
    Rank_Base_CDF = np.arange(1, len(Base_CDF) + 1)

    Target_CDF = np.sort(Target_CDF)[::-1]
    Base_CDF = np.sort(Base_CDF)[::-1]

    q_Target_CDF = (Rank_Target_CDF - 0.4) / (len(Target_CDF) + 0.2)
    q_Base_CDF = (Rank_Base_CDF - 0.4) / (len(Base_CDF) + 0.2)

    # flag1: number of values falling outside of Base_CDF in original DATA
    idx1 = np.where((DATA > np.max(Base_CDF)) | (DATA < np.min(Base_CDF)))[0]
    n1 = len(idx1)

    # Determine if any value is below zero, which needs the offset of data
    if np.any(np.array([np.min(Target_CDF), np.min(Base_CDF), np.min(DATA)]) < 0):
        min_val = min(np.min(Target_CDF), min(np.min(Base_CDF), np.min(DATA)))
        offset = abs(int(np.floor(min_val)))

        Target_CDF += offset
        Base_CDF += offset
        DATA += offset

    # Quantile mapping
    for i, val in enumerate(DATA):
        # if same values exist on the Base_CDF
        if np.sum(Base_CDF == val) > 1:
            apple = np.where(Base_CDF == val)[0]
            start_q = q_Base_CDF[apple[0]]
            end_q = q_Base_CDF[apple[-1]]
            length_zero = end_q - start_q
            scaled_distance = np.random.rand()
            q = start_q + (length_zero * scaled_distance)
            apple = np.argmin(np.abs(q_Target_CDF - q))
            Output[i] = Target_CDF[apple]
            continue

        # Extrapolation of extreme value
        # Higher than maximum value of Base CDF
        if val > np.max(Base_CDF):
            # Mean of Base CDF
            mu1 = np.mean(Base_CDF)
            # Calculate mean if the highest value of Base CDF is replaced with the extreme value
            mu2 = (val + np.sum(Base_CDF[1:])) / len(Base_CDF)
            # Relative changes in the means
            R = (mu2 - mu1) / abs(mu1)
            # Mean of Target CDF
            mu3 = np.mean(Target_CDF)
            # Adjust values in a way that preserves the changes in the 1st moment
            Output[i] = (mu3 + abs(mu3) * R) * len(Target_CDF) - np.sum(Target_CDF[1:])

        # Lower than minimum value of Base CDF
        elif val < np.min(Base_CDF):
            # Mean of Base CDF
            mu1 = np.mean(Base_CDF)
            # Calculate mean if lowest value is replaced with extreme value
            mu2 = (val + np.sum(Base_CDF[:-1])) / len(Base_CDF)
            # Relative changes in the means
            R = (mu2 - mu1) / abs(mu1)
            # Mean of Target CDF
            mu3 = np.mean(Target_CDF)
            # Adjust values in a way that preserves the changes in the 1st moment
            Output[i] = (mu3 + abs(mu3) * R) * len(Target_CDF) - np.sum(Target_CDF[:-1])

        else:
            apple = np.argmin(np.abs(Base_CDF - val))
            q = q_Base_CDF[apple]
            apple = np.argmin(np.abs(q_Target_CDF - q))
            Output[i] = Target_CDF[apple]

    # Bring back the data to the original range by substracting offset value. 
    if np.any(np.array([np.min(Target_CDF), np.min(Base_CDF), np.min(DATA)]) < 0):
        Target_CDF -= offset
        Base_CDF -= offset
        DATA -= offset
        Output -= offset

    # if minimum bound is provided, then replace the value outise the bound
    if min_bound is not None and isinstance(min_bound, (int, float)):
        idx = np.where(DATA < min_bound)[0]
        DATA[idx] = min_bound

    return Output

