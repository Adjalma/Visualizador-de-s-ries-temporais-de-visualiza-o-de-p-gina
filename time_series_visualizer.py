import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', 
                 parse_dates=['date'], 
                 index_col='date')

# Clean data
df = df[(df['value'] >= df['value'].quantile(0.025)) & 
        (df['value'] <= df['value'].quantile(0.975))]

def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(15, 5))
    
    ax.plot(df.index, df['value'], color='red', linewidth=1)
    
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    
    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['Year'] = df_bar.index.year
    df_bar['Month'] = df_bar.index.month
    df_bar = df_bar.groupby(['Year', 'Month'])['value'].mean().unstack()
    
    # Draw bar plot
    fig = df_bar.plot(kind='bar', figsize=(15, 10)).figure
    
    plt.title('')
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    
    months = ['January', 'February', 'March', 'April', 'May', 'June', 
              'July', 'August', 'September', 'October', 'November', 'December']
    plt.legend(title='Months', labels=months)
    
    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = df_box.date.dt.year
    df_box['month'] = df_box.date.dt.strftime('%b')
    
    # Create figure and subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
    
    # Year-wise Box Plot
    years = [2016, 2017, 2018, 2019]
    year_data = [df_box[df_box['year'] == year]['value'] for year in years]
    
    # Box plot com configurações específicas para controlar o número de linhas
    bp1 = ax1.boxplot(year_data, 
                      labels=years,
                      notch=False,  # Desativar entalhes
                      showmeans=False,  # Não mostrar média
                      meanline=False,  # Não mostrar linha da média
                      whis=1.5,  # Whiskers padrão
                      patch_artist=True,  # Usar patch_artist para controlar melhor as linhas
                      showfliers=True,  # Mostrar outliers
                      boxprops={'facecolor': 'white'},  # Caixa branca
                      capprops={'color': 'black'},  # Cor dos caps
                      whiskerprops={'color': 'black'},  # Cor dos whiskers
                      flierprops={'markerfacecolor': 'red', 'marker': 'o'},  # Configuração dos outliers
                      medianprops={'color': 'red'})  # Cor da mediana
    
    ax1.set_title('Year-wise Box Plot (Trend)')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Page Views')
    ax1.set_yticks(range(0, 200001, 20000))
    ax1.set_yticklabels([str(x) for x in range(0, 200001, 20000)])
    
    # Month-wise Box Plot
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    month_data = [df_box[df_box['month'] == month]['value'] for month in month_order]
    
    # Usar as mesmas configurações para o gráfico mensal
    bp2 = ax2.boxplot(month_data, 
                      labels=month_order,
                      notch=False,
                      showmeans=False,
                      meanline=False,
                      whis=1.5,
                      patch_artist=True,
                      showfliers=True,
                      boxprops={'facecolor': 'white'},
                      capprops={'color': 'black'},
                      whiskerprops={'color': 'black'},
                      flierprops={'markerfacecolor': 'red', 'marker': 'o'},
                      medianprops={'color': 'red'})
    
    ax2.set_title('Month-wise Box Plot (Seasonality)')
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Page Views')
    ax2.set_yticks(range(0, 200001, 20000))
    ax2.set_yticklabels([str(x) for x in range(0, 200001, 20000)])
    
    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig 
