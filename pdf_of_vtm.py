#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A script to plot variable temperature measurements of proteins performed to
determine their thermal melting point using circular dichroism.
The script prompts the user to provide a name of a csv file and plots the data,
then writes the plot along with the estimated melting temperature to a pdf.
Created on Fri Mar  7 12:56:34 2025

@author: Hugo Olsson
"""
#Importing required packages
import matplotlib.pyplot as plt
import seaborn as sns
import pandas
import numpy as np
import scipy

#Setting the fonts used by plot_vtm()
hfont = {'fontname':'arial'}
afont = {'fontname':'arial'}

#prompting the user to provide the name or path of a file, then loading the 
# data into a pandas dataframe.
filename = input("Type the name or path of the file you want to plot")
f = pandas.read_csv(filename, sep = ';')

def get_tm(data):
    """
    A function that extracts the temperature and dichrosim signal data to 
    find the temperature where half the sample has lost its original signal,
    which corresponds to the melting point.
    """
    temp = np.array(data['Unnamed: 0'])
    cd = np.array(data['221'])
    floor = np.mean(cd[0:9])
    ceiling = np.mean(cd[-10:-1])
    inflection_point = np.mean([floor, ceiling])
    interpolator = scipy.interpolate.interp1d(cd, temp)
    tm = interpolator(inflection_point)
    return tm

def make_vectors(data):
    """
    Takes the dataframe as input and extracts the two data axes assigning them 
    to arrays.
    """
    temp = data['Unnamed: 0']
    cd = data['221']
    return temp, cd

def plot_vtm(x, y, nameoffile):
    """
    Takes in the name of the file as well as the two arrays produced by
    make_vectors and produces a VTM plot which it writes to a pdf together
    with the melting temperature calculated by get_tm(), which is called 
    inside plot_vtm().

    """
    fig = plt.figure()
    sns.set_theme(style="darkgrid")
    ax  = fig.add_subplot(111)
    stop_at = nameoffile.index('_')
    construct = nameoffile[0:stop_at]
    ax.set_title(f'VTM of {construct}', **hfont, fontsize=16, weight='bold')
    tm = get_tm(pandas.read_csv(nameoffile, sep = ';'))
    ax.plot(x, y, label=f'Melting point: {str(round(float(tm)))} °C', color = 'k')
    ax.set_xlabel(r'°C', **afont, fontsize=14)
    ax.legend()
    ax.set_ylabel(r'mdeg', **afont, fontsize=14)
    plt.show()
    #fig.savefig(f'{filename}_ploting.pdf', format='pdf', bbox_inches='tight')
    

# The script finishes by calling the necessary functions to produce the pdf
# according to the user input filename.
temp, cd = make_vectors(f)
plot_vtm(temp, cd, filename)

    