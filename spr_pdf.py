#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A script that asks the user for a file containing data from SPR experiments 
and plots the data 
Created on Fri Mar 14 11:00:01 2025

@author: hugoo
"""

#Importing required packages
import matplotlib.pyplot as plt
import pandas
import numpy as np


#Setting the fonts used by plot_vtm()
hfont = {'fontname':'arial'}
afont = {'fontname':'arial'}

#Prompting the user to provide the name or path of a file, then loading the 
#data into a pandas dataframe.
filename = input("Type the name or path of the file you want to plot")
f = pandas.read_csv(filename, sep = ';')

def trim_time(data):
    """
    A function that assigns the needed time vector to a np array and trims 
    the remaining time data. Also delivers the concentrations as a list.

    """
    titles = list(data.columns)[0:-1:4]
    j = 0
    for i in titles:
        name = i.split(';')
        titles[j] = name[-1][6:-3]
        j += 1
    data = data.replace(',', '.', regex = True)
    data = data.replace(r'^\s*$', np.nan, regex=True)
    time = np.array(data[data.columns[0]].to_numpy(np.float16))
    data = data.drop(np.array(data.columns)[::2], axis = 1)
    return time, data, titles

def without_fits(data):
    """
    A function that removes the fit data from the input dataframe.

    """
    data = data.drop(np.array(f.columns)[1::2], axis = 1)
    return data

def plot_fits_anyone(data):
    """
    A function that prompts the user to decide if they want to plot fits or not,
    then treating the dataframe accordinglky and assigning a boolean "fits".

    """
    
    #asking if the user want to plot fits or not
    plot_fits = input("Do you want to plot fits? [y/n] ")
    if plot_fits in ['y', 'Y', 'Yes', 'yes']:
        data = data
        fits = True
    elif plot_fits in ('N', 'n', 'no', 'No'):
        data = without_fits(data)
        fits = False
    else:
        print('input error')
    return data, fits

def plot_sensorgrams(data, time, fits, name_of_file, legends):
    """
    Based on a dataframe trimmed by previous functions, a time vector created
    in trim_time() and boolean delivered by plot_fits_anyone() this funtion 
    produces the plot of the sensorgrams, with or without fitted data
    depending on the value of "fits".
    """
    fig = plt.figure()
    ax  = fig.add_subplot(111)
    stop_at = name_of_file.index('_')
    construct = name_of_file[0:stop_at]
    ax.set_title(f'SPR of {construct}', **hfont, fontsize=16, weight='bold')
   
    counter = 0
    conc = 0
    
    while len(list(data.columns)) > 0:
        curve = np.array(data[data.columns[0]].to_numpy(np.float16))
        data = data.drop(np.array(data.columns)[0], axis = 1)
        if fits:
            if counter in range(1, 100, 2):
                ax.plot(time, curve, color = 'k', linestyle = 'dashed')
            else:
                ax.plot(time, curve, color = 'k', label = legends[conc])
                conc += 1
            counter += 1
        else:
            ax.plot(time, curve, color = 'k', label = legends[conc])
            conc += 1
    
    ax.legend(reverse = True)
    ax.set_xlabel(r'Time (s)', **afont, fontsize=14)
    ax.set_ylabel(r'RU', **afont, fontsize=14)
    plt.show()
    #fig.savefig(f'{filename}.pdf', format='pdf', bbox_inches='tight')

#Calling the functions to write the graph
time, f, legends = trim_time(f)
f, fits = plot_fits_anyone(f)
plot_sensorgrams(f, time, fits, filename, legends)