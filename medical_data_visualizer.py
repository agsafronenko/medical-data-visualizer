import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os
import platform

if platform.system() == "Windows":
    os.system("cls")
else:
    os.system("clear")

df = pd.read_csv('medical_examination.csv')
df['overweight'] = (df['weight'] / ((df['height'] / 100) ** 2)).apply(lambda w: 1 if w > 25 else 0)
df['cholesterol'] = df['cholesterol'].apply(lambda x: 1 if x > 1 else 0)
df['gluc'] = df['gluc'].apply(lambda x: 1 if x > 1 else 0)

def draw_cat_plot():

    df_cat = pd.melt(df, id_vars=['cardio'], value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])
    df_cat = df_cat.groupby(['cardio', 'variable', 'value']).size().reset_index(name='total')
    fig = sns.catplot(
        x="variable", y="total", hue="value", col="cardio",
        data=df_cat, kind="bar", height=7, aspect=1
    ).fig
    fig.savefig('catplot.png')
    return fig

def draw_heat_map():
    df_heat = df[
        (df['ap_lo'] <= df['ap_hi']) &
        (df['height'] >= df['height'].quantile(0.025)) &
        (df['height'] <= df['height'].quantile(0.975)) &
        (df['weight'] >= df['weight'].quantile(0.025)) &
        (df['weight'] <= df['weight'].quantile(0.975))
    ]
    corr = df_heat.corr()
    mask = np.triu(np.ones_like(corr))
    fig, ax = plt.subplots(figsize=(12, 12))
    sns.heatmap(corr, mask=mask, annot=True, fmt='.1f', ax=ax, cmap='viridis', square=False, linewidths=1)
    fig.savefig('heatmap.png')
    return fig
