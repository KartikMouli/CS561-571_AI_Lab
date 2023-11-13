# %% [markdown]
# CS571 : Assignment 7 (Linear Regression)
# 

# %% [markdown]
# Group Members Roll No.s : 2001CS35,2001CS56,2001CS70

# %%
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# %% [markdown]
# Step 1: Processing dataset

# %%
# Load the dataset from TSV
file_path = './newspaper.csv'
df = pd.read_csv(file_path ,header=0)
df

# %% [markdown]
# Step 2: Data Analysis

# %%
min_daily_sales = df['Daily'].min()
max_daily_sales = df['Daily'].max()
avg_daily_sales = df['Daily'].mean()

print("Min Daily Sales: " ,min_daily_sales)
print("Max Daily Sales: " ,max_daily_sales)
print("Avg Daily Sales: " ,avg_daily_sales)

thres_min_daily_sales =  min_daily_sales * 1.3
thres_max_daily_sales = max_daily_sales * 1.3
thres_avg_daily_sales = avg_daily_sales * 1.3


print("\nMin Daily Sales Threshold: " ,thres_min_daily_sales)
print("Max Daily Sales Threshold: " ,thres_max_daily_sales)
print("Avg Daily Sales Threshold: " ,thres_avg_daily_sales)


# %% [markdown]
# Step 3: Estimate coefficient

# %%
# number of observations/points
x=df['Daily']
y=df['Sunday ']
n = np.size(x)

# mean of x and y vector
m_x = np.mean(x)
m_y = np.mean(y)

# calculating cross-deviation and deviation about x
SS_xy = np.sum(y*x) - n*m_y*m_x
SS_xx = np.sum(x*x) - n*m_x*m_x

# calculating regression coefficients
b_1 = SS_xy / SS_xx
b_0 = m_y - b_1*m_x


b=[b_0,b_1]
b


# %% [markdown]
# Step 4: Plot Graph

# %%
# plotting the actual points as scatter plot
plt.scatter(x, y, color = "m",marker = "o")

# predicted response vector
y_pred = b[0] + b[1]*x

# plotting the regression line
plt.plot(x, y_pred, color = "g")

# putting labels
plt.xlabel('Daily_Sales')
plt.ylabel('Sunday_Pred')

# function to show plot
plt.show()



# %%
df['Sunday_Pred'] = y_pred
df

# %% [markdown]
# Step 5: Check which Newspaper should stop Sunday circulation

# %%
df['Stop_Sunday_Min'] = np.where(df['Sunday_Pred'] > thres_min_daily_sales,'Yes','No')
df['Stop_Sunday_Max'] = np.where(df['Sunday_Pred'] > thres_max_daily_sales,'Yes','No')
df['Stop_Sunday_Avg'] = np.where(df['Sunday_Pred'] > thres_avg_daily_sales,'Yes','No')

df

# %%
print("Stop Sunday Edition (In case of Avg):")

no_sunday_edition_avg = df[df['Stop_Sunday_Avg'] == 'No']
no_sunday_edition_avg['Newspaper']

# %% [markdown]
# Step 6: Desired result

# %%
print("Stop Sunday Edition (In case of Min):")

no_sunday_edition_min = df[df['Stop_Sunday_Min'] == 'No']
no_sunday_edition_min['Newspaper']

# %%
print("Stop Sunday Edition (In case of Max):")

no_sunday_edition_max = df[df['Stop_Sunday_Max'] == 'No']
no_sunday_edition_max['Newspaper']


