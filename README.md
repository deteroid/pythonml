# Air Pollution Forecasting using ARIMA in Python

## Introduction

This repository provides a Python implementation of time-series forecasting using ARIMA (AutoRegressive Integrated Moving Average) for air pollution data collected in the city of Beijing. The dataset, donated on 3/22/2016, consists of hourly responses from a gas multisensor device deployed in an Italian city. The hourly responses include averages recorded from 5 metal oxide chemical sensors embedded in an Air Quality Chemical Multisensor Device. The goal is to predict the concentrations of various gases, including CO, Non Metanic Hydrocarbons, Benzene, Total Nitrogen Oxides (NOx), and Nitrogen Dioxide (NO2).

## Dataset Information

- **Instances:** 9358
- **Features:** 15
- **Subject Area:** Computer Science
- **Associated Tasks:** Regression
- **Feature Type:** Real
- **Missing Values:** Yes (Tagged with -200 value)

### Variables Table

| Variable Name  | Role       | Type       | Demographic | Description                                                         | Units       | Missing Values |
|----------------|------------|------------|-------------|---------------------------------------------------------------------|-------------|-----------------|
| Date           | Feature    | Date       |             | Date in DD/MM/YYYY format                                           | -           | No              |
| Time           | Feature    | Categorical|             | Time in HH.MM.SS format                                             | -           | No              |
| CO(GT)         | Feature    | Integer    |             | True hourly averaged concentration CO in mg/m^3 (reference analyzer)| mg/m^3      | No              |
| PT08.S1(CO)    | Feature    | Categorical|             | Hourly averaged sensor response (nominally CO targeted)             | -           | No              |
| NMHC(GT)       | Feature    | Integer    |             | True hourly averaged overall Non Metanic HydroCarbons concentration | microg/m^3  | No              |
| C6H6(GT)       | Feature    | Continuous |             | True hourly averaged Benzene concentration                           | microg/m^3  | No              |
| PT08.S2(NMHC)  | Feature    | Categorical|             | Hourly averaged sensor response (nominally NMHC targeted)            | -           | No              |
| NOx(GT)        | Feature    | Integer    |             | True hourly averaged NOx concentration in ppb (reference analyzer)  | ppb         | No              |
| PT08.S3(NOx)   | Feature    | Categorical|             | Hourly averaged sensor response (nominally NOx targeted)             | -           | No              |
| NO2(GT)        | Feature    | Integer    |             | True hourly averaged NO2 concentration in microg/m^3                 | microg/m^3  | No              |

### Additional Variable Information

0. Date (DD/MM/YYYY)
1. Time (HH.MM.SS)
2. True hourly averaged concentration CO in mg/m^3 (reference analyzer)
3. PT08.S1 (tin oxide) hourly averaged sensor response (nominally CO targeted)
4. True hourly averaged overall Non Metanic HydroCarbons concentration in microg/m^3 (reference analyzer)
5. True hourly averaged Benzene concentration in microg/m^3 (reference analyzer)
6. PT08.S2 (titania) hourly averaged sensor response (nominally NMHC targeted)
7. True hourly averaged NOx concentration in ppb (reference analyzer)
8. PT08.S3 (tungsten oxide) hourly averaged sensor response (nominally NOx targeted)
9. True hourly averaged NO2 concentration in microg/m^3 (reference analyzer)
10. PT08.S4 (tungsten oxide) hourly averaged sensor response (nominally NO2 targeted)
11. PT08.S5 (indium oxide) hourly averaged sensor response (nominally O3 targeted)
12. Temperature in °C
13. Relative Humidity (%)
14. AH Absolute Humidity

## Usage

1. Clone the repository:

```bash
git clone https://github.com/yourusername/air-pollution-forecasting.git
cd air-pollution-forecasting

