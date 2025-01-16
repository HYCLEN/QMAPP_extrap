# An Empirical Quantile Mapping for the Extrapolation of Extreme Values 
This project embodies an enhanced empirical Quantile Mapping (QM) technique for bias correction across various outputs of environmental models, including climate models. Specifically, this improved approach allows for the extrapolation of "new extremes" to correct biases in future projections that fall beyond the scope of existing quantile-based transfer functions. Additionally, it integrates a previously established wet-day frequency adjustment method using Monte Carlo simulations for precipitation (or other variables with zero-value tails), thus providing a more comprehensive version of empirical QM.

## Code Availability with requirements
1. Python (version 3.6 above) with numpy, pandas, and matplotlib (for implementing example and visualization of result)  
2. MATLAB (version 2017 above)

## Usage
  1. Python (QMAPP_extrap.py)
    
    def QMAPP_extrap(Target_CDF, Base_CDF, DATA, min_bound=None):
    
  2. MATLAB (QMAPP_extrap.m)

    function [Output]=QMAPP_extrap(Target_CDF, Base_CDF, DATA, min_bound)
- Input:
    - Target_CDF: Empirical Cumulative Distribution Function (CDF) of benchmark data (e.g., observations from 1950-2000).
    - Base_CDF: Empirical CDF of the baseline data to be corrected (e.g., monthly General Circulation Model (GCM) data for the historical periods of 1950-2000).
    - DATA : Data to be bias-corrected (e.g., GCM data spanning from 1950-2100, including future periods).
    - min_bound : If the corrected final output should be greater than or equal to a specific value (e.g. 0 in case of precipitation), the user can specify the minimum bound as a numeric value. Otherwise, leave it as 'none'.
                
- Output: Corrected data by Quantile Mapping

## Example
Implementation of code is demonstrated by an example in which the output of a regional climate model for a future period is bias-corrected.

Sample data: daily total precipitation of July for the reference period (1995-2004) and target period (2085-2094)

(1) 'OBS_1995-2004': observed data
  
(2) 'HR_1995-2004': historical run of Regional Climate Model(RCM)   
  
(3) 'CCR_2085-2094': future climate change run of RCM
 
## Citation
Details on this approach are provided in the following:

Byun, K. and Hamlet, A.F (2025) An improved empirical quantile mapping approach for bias correction of extreme values in climate model simulations. Environmental Research Letters 20, 014041. https://doi.org/10.1088/1748-9326/AD9B3D 
