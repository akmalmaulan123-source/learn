import pandas as pd
import matplotlib.pyplot as pyplot
import seaborn as sns

df = pd.read_csv("latihan1.csv")
print(df.head())
print(df.shape)
print(df.columns)
print(df.info())