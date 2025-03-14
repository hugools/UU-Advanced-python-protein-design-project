#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 10 08:40:27 2025
A script to plot the absorbance spectra of circularly polarized light of
proteins, obtained from circular dichroism measurements. The script prompts
the user to provide a file name/path and then loads it as a pandas dataframe, 
plotting it using matplotlib, seaborn and numpy. The plot is printed to pdf.

@author: hugoo
"""

#Importing required packages
import matplotlib.pyplot as plt
import seaborn as sns
import pandas
import numpy as np

#Setting fonts for later use
hfont = {'fontname':'arial'}
afont = {'fontname':'arial'}

#Importing the csv file containing the data
filename = input("Type the name or path of the file you want to plot")
f = pandas.read_csv(filename, sep = ';')

def make_vectors(data):
    """
    Takes the dataframe as input and extracts the two spectrum curves 
    to arrays. Aldso creates an array for plotting the 0 mdeg intercept as
    well as the x-axis of different wavelengths ("wave").
    """
    wave = data['Unnamed: 0']
    before = data['Subtracted:0']
    after = data['Subtracted:1']
    axel = np.zeros(len(wave))
    return wave, before, after, axel


def plot_spectra(data, name_of_file):
    """
    A function that plots to a pdf utilizing the make_vectors() function.

    """
    x, y1, y2, zero_intercept = make_vectors(data)
    fig = plt.figure()
    sns.set_theme(style="darkgrid")
    ax  = fig.add_subplot(111)
    stop_at = name_of_file.index('_')
    construct = name_of_file[0:stop_at]
    ax.set_title(f'CD Spectra of {construct}', **hfont, fontsize=16, weight='bold')
    ax.plot(x, y1, label='Before', color = 'r')
    ax.plot(x, y2, label='After', color = 'b')
    ax.plot(x, zero_intercept, linestyle = 'dashed', color = 'k')
    ax.legend()
    ax.set_xlim(195, 260)
    ax.set_xlabel(r'nm', **afont, fontsize=14)
    ax.set_ylabel(r'mdeg', **afont, fontsize=14)
    plt.show()
    fig.savefig('ZH4_refolding_plot.pdf', format='pdf', bbox_inches='tight')
    
#Calling the functions to produce the plot
plot_spectra(f, filename)

