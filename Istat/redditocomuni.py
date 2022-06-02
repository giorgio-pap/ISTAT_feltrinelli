#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 31 18:47:35 2022

@author: giorgiopapitto

script made for the Feltrinelli Education workshop
data storytelling

this script works on data provided by ISTAT
https://www1.finanze.gov.it/finanze/analisi_stat/public/index.php?search_class[0]=cCOMUNE&opendata=yes
of the type "Redditi_e_principali_variabili_IRPEF_su_base_comunale_CSV"

python 3
"""

#import relevant packages
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#where the files are
root = "/Users/giorgiopapitto/Documents/GitHub/ISTAT_feltrinelli/Istat/files/"
file_name = "Redditi_e_principali_variabili_IRPEF_su_base_comunale_CSV_"

######################
##tipologie di reddito
######################

#define range of the years
for x in range(2015,2021):
    
    #convert year to string
    anno = str(x)
    
    #import file
    f0 = pd.read_csv(root + file_name + anno + ".csv", 
                    sep=';', index_col=False)
    
    #make list of relevant columns
    columns_relevant=["Reddito da fabbricati - Ammontare in euro", 
                      "Reddito da lavoro dipendente e assimilati - Ammontare in euro",
                      "Reddito da pensione - Ammontare in euro",
                      "Reddito da lavoro autonomo (comprensivo dei valori nulli) - Ammontare in euro",
                      ]
    
    #keep relevant columns
    f1 = f0[columns_relevant]
    
    #rename them
    f1.rename(columns = {'Reddito da fabbricati - Ammontare in euro':'Fabbricati',
                         'Reddito da lavoro dipendente e assimilati - Ammontare in euro':'Lavoro dipendete',
                         'Reddito da pensione - Ammontare in euro':'Pensione',
                         "Reddito da lavoro autonomo (comprensivo dei valori nulli) - Ammontare in euro":'Lavoro autonomo'}, inplace = True)
    
    #replace empty columns with 0s
    f1.fillna(0, inplace=True)
    
    #make total column and wor
    f1.loc['Percentuale']= f1.sum(numeric_only=True, axis=0)
    f1.loc[:,'Column_Total'] = f1.sum(numeric_only=True, axis=1)
    
    #keep the last row = one with total values
    f2 = f1.loc[["Percentuale"]]
    
    #calcucate percentages based on last column
    f3 = f2[['Fabbricati','Lavoro dipendete',
        "Pensione", "Lavoro autonomo"]].div(f2.Column_Total, axis=0)*100
    
    #make columns into rows
    f3_T = f3.T
    
    #transform the index into a column
    f3_T['Tipo di Lavoro'] = f3_T.index
    
    #set the title of the plot
    title_subplot = "Contributi alle entrate da parte di diversi tipi di reddito"
    
    #make a barplot
    ax = sns.barplot(x = "Tipo di Lavoro", y="Percentuale", data=f3_T)
    plt.title(title_subplot,fontsize=14)
    plt.suptitle(anno,fontsize=18, y=1)
    
    #set y limits ) from 0 to 60%
    plt.ylim(0, 60)
    plt.savefig(root + "figures/" + anno + ".png", dpi=300) 
    plt.show()
    
    
#################    
#fasce di reddito
#################

#create empty list for later appending to it
appended_data = []

#define range of the years
for x in range(2015,2021):
    
    #convert year to string
    anno = str(x)
    
    #import file
    f0 = pd.read_csv(root + file_name + anno + ".csv", 
                    sep=';', index_col=False)
    
    #make list of relevant columns
    columns_relevant=["Reddito complessivo da 0 a 10000 euro - Frequenza",
                      "Reddito complessivo da 10000 a 15000 euro - Frequenza",
                      "Reddito complessivo da 15000 a 26000 euro - Frequenza",
                      "Reddito complessivo da 26000 a 55000 euro - Frequenza",
                      "Reddito complessivo da 55000 a 75000 euro - Frequenza",
                      "Reddito complessivo da 75000 a 120000 euro - Frequenza",
                      "Reddito complessivo oltre 120000 euro - Frequenza"
                      ]
    
    #keep relevant columns
    f1 = f0[columns_relevant]
    
    #rename them
    f1.rename(columns = {"Reddito complessivo da 0 a 10000 euro - Frequenza": "0-10k",
                      "Reddito complessivo da 10000 a 15000 euro - Frequenza": "10k-15k",
                      "Reddito complessivo da 15000 a 26000 euro - Frequenza": "15k-26k",
                      "Reddito complessivo da 26000 a 55000 euro - Frequenza": "26k-55k",
                      "Reddito complessivo da 55000 a 75000 euro - Frequenza": "55k-75k",
                      "Reddito complessivo da 75000 a 120000 euro - Frequenza": "75k-120k",
                      "Reddito complessivo oltre 120000 euro - Frequenza": ">120k"
        }, inplace = True)
    
    #replace empty cells with 0s
    f1.fillna(0, inplace=True)
    
    #create a total value
    f1.loc['Totale']= f1.sum(numeric_only=True, axis=0)
    
    #keep the total row
    f2 = f1.loc[["Totale"]]
    
    #make columns into rows
    f2_T = f2.T
    
    #transform the index into a column
    f2_T['Fascia'] = f2_T.index
    
    #insert a column with the year
    f2_T.insert(0, 'Anno', anno)
    
    #reset the index
    f2_T = f2_T.reset_index(drop=True)

    #append the df to the empty list
    appended_data.append(f2_T)

#concatenate the appended things
#make only one df with all years    
data = pd.concat(appended_data)

#read the data as every 1000 people
data["Totale"] = data["Totale"]/1000

#reset index
data = data.reset_index(drop=True)

#creat a subplot structure
fig,ax = plt.subplots()

#plot lines on top of eachother
for name in pd.unique(data['Fascia']):
    ax.plot(data[data.Fascia==name].Anno,data[data.Fascia==name].Totale,label=name)

ax.set_title("Numero di contribuenti per fascia (ogni 1000 contribuenti)")
ax.set_xlabel("Anno")
ax.set_ylabel("Numero di contribuenti")

#legend outside of the plot
lgd = ax.legend(loc='center left', bbox_to_anchor=(1, 0.83))  
#create dummy text
text = ax.text(-0.2,1.05, "", transform=ax.transAxes)

#save this way otherwise the legend is cut when high resolution
fig.savefig(root + "figures/fasce_di_reddito_per_anno.png", bbox_extra_artists=(lgd, text), bbox_inches='tight',dpi=300)  
