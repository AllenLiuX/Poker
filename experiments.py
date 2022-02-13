import random
import logging
from typing import final
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pyparsing import line_start
import seaborn as sns
from dataclasses import dataclass, replace

import blackjack as blackjack

def plot_data(data, save_file = ''):
    plt.figure(figsize=(20,6))
    sns.lineplot(list(range(len(data))), data)
    plt.grid()
    # if save_file:
    #     plt.savefig(save_file)
    # else:
    #     plt.show()

def experiment(bj_ratio = 0.3, commission=0, iterations=1000, epochs=5):
    data_dict = {}    
    
    for i in range(epochs):
        game = blackjack.Game(money=500, blackjack_ratio=bj_ratio, commission=commission)
        data = game.simulate(manual_mode=False, bet=20, iterations=iterations)
        data = data + [0 for _ in range(iterations-len(data))]
        data_dict[f'experiment_{i}'] = data
        
    return data_dict

def plot(data_dict, title, save_file=''):
    df = pd.DataFrame(data_dict)
    print(df)
    # plt.style.use('dark_background')
    # plt.grid()
    sns.set_style('darkgrid',rc={"grid.color": ".5", "grid.linestyle": ":"})
    # sns.set_theme()
    plt.figure(figsize=(25,10))
    plt.title(title)

    maxs = []
    finals = []
    for key, data in data_dict.items():
        # Annotate max value
        data = np.array(data)
        max_ind = np.argmax(data)
        maxs.append(data[max_ind])
        finals.append(data[-1])
        plt.annotate(f'max{key[-1]}: {data[max_ind]}', xy=(max_ind, data[max_ind]))
        plt.annotate(f'final{key[-1]}: {data[-1]}', xy=(len(data), data[-1]), fontsize=8)
        
    plt.annotate(f'Average Max: {round(np.mean(maxs), 2)}', xy=(0,0))
    plt.annotate(f'Average Final: {round(np.mean(finals), 2)}', xy=(0, 80))
    sns.lineplot(data=df)
    plt.xlabel('Round')
    plt.ylabel('Money ($)')
    
    
    if save_file:
        plt.savefig(save_file)
    else:
        plt.show()

if __name__=='__main__':
    data_dict = experiment(iterations=1000, epochs=7)
    plot(data_dict, title='Venetian Blackjack Ratio=0.3 commission=0 bet=20 Trend', save_file='plot/vegas.png')
    data_dict = experiment(bj_ratio=0.2, commission=1, iterations=1000, epochs=7)
    plot(data_dict, title='Hollywood Casino Blackjack Ratio=0.2 commission=1 bet=20 Trend', save_file='plot/hollywood.png')
