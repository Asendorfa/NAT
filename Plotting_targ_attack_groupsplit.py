# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 15:47:48 2023

@author: Adrian Asendorf
"""

from scipy.io import loadmat
from scipy import stats
import os
import fnmatch, glob
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from scipy.stats import spearmanr
from collections import Counter

#==============================================================================
gr1_mat_name = 'MSizeTargAttack_deg_geff_PD_weighted'
meta_path    = '/DATA/DoMoCo/Targeted Attacks/Analysis/09_Demographics/5.3th_GO_19PD+6PD_preupdate/DoMoCo_Demographics.xlsx'
inp_dir      = '/DATA/DoMoCo/Targeted Attacks/Analysis/02_Attack_Analysis_GAT/5th_GO_5_additional_Subjects/TargAttack_1p_long/'
path_overv   = "/archive/DoMoCo/DATA/raw_data/Overview_Data.xlsx"
output_dir   =  os.getcwd() +'/'
signlevel    = 0.05
network_dirs = ['All_ROIs','Frontoparietal_network','DefaultMode_network', 
    'Somatomotor_network', 'Attention_network'
    ]#, 'CinguloOpercular_network','Auditory_network']
thresh_OI    = ['0.100','0.150','0.200','0.250','0.300','0.350','0.400','0.450','0.500']  
#==============================================================================

#read input dataframes
#df_PA    = pd.read_excel (path_PA, index_col='record_id', sheet_name='DoMoCo_PA_linked_value' )

df_meta  = pd.read_excel (meta_path, index_col= 'record_id')
# =============================================================================
# df_meta  = df_meta[(df_meta['No-MRI-Participant'] != 1) & (df_meta['Status'] != 'HC') & (df_meta['Post_Scanner_Update']==1)]
# merged_df = merged_df.sort_index()
# =============================================================================
index_OI = [9087]
df_meta  = df_meta.loc[index_OI]
df_meta  = df_meta.sort_index()
#add index with actual index n
df_meta['ind']=range(len(df_meta))

#==============================================================================
#Test group differences
#define dfs

df_all_attac= pd.DataFrame(index = df_meta.index)


for network_name in network_dirs:
    #create a subj df
    df_attack= pd.DataFrame(index = df_meta.index)
    #find only the folders starting with tresholded
    new_dir = inp_dir+network_name
    folder_dirs = glob.glob(new_dir+'/thr*')
    #Load the data for  all thresholds for both groups in one df
    dicti={}
    #crate a container for sign findings:
    sign=[]
    print('============'+network_name+'===================')
    for i,folder in enumerate(sorted(folder_dirs)):
        threshold    = folder.split('/')[-1].split('_')[1]
        res_mat      = loadmat(folder+'/'+gr1_mat_name)
        Attack_geff  = pd.DataFrame(res_mat['mszT']) #individual attack values. These are normalized already
        n_nodes      = Attack_geff.shape[0]          #number of attack equals number of nodes of the network
        AUC_mat      = res_mat['auc_TA'][0]
        norm_AUC     = AUC_mat / n_nodes
        auc          = list(np.around(norm_AUC, decimals=3)) #round number
        df_attack['NAT_'+str(network_name)+'_'+str(threshold)]= auc
        #test normality
        #test_normality_and_plot_density(AUC_gr2)
        #test_normality_and_plot_density(AUC_gr1)
        dicti[threshold]=norm_AUC
        #check for statistical differences between groups and report them:
    df_all_attac= pd.merge(df_all_attac, df_attack, left_index=True, right_index=True)
    df =pd.DataFrame(dicti)
    df.to_csv(output_dir+'csvs/'+network_name+'_targ_attack.csv',index = True ) 

import statsmodels.api as sm
import statsmodels.formula.api as smf

dfs=[]
#Add into 
for thresh in thresh_OI:
    thresh= '_'+thresh
    #merge and export as one excel sheet 
    df_OI_attack =df_all_attac[[
              'NAT_All_ROIs'+thresh,\
              'NAT_Somatomotor_network'+thresh, 'NAT_Attention_network'+thresh,\
            'NAT_Frontoparietal_network'+thresh, 'NAT_DefaultMode_network'+thresh]]
    final_df = pd.merge(df_meta,df_OI_attack, left_index=True, right_index=True)
    dfs.append(final_df)
    for network in df_OI_attack.columns:
        netw_name ='_'.join(network.split('_')[:3])
        rename = netw_name+'_'+thresh[3:]
        print(f'======================={rename}=============')
        final_df.rename(columns={netw_name+thresh: rename}, inplace=True)
    final_df.to_csv(output_dir+'demog+targ_attack_'+thresh+'.csv',index = True)




# Assuming you have the following DataFrames: df_150, df_250, df_350, df_400, df_500
#thresholds = ['150', '250','350','500']
thresholds = ['100','150','200', '250','300', '350','400', '450','500']
# Create a list to store processed DataFrames
processed_dfs = []

for df, threshold in zip(dfs, thresholds):
    # Add the 'Threshold' column
    df['Density'] = int(threshold)
    df['ID']        = df.index
    # Rename the NAT columns to remove the threshold suffix
    df.columns = [col.replace(f'_{threshold}', '') if f'_{threshold}' in col else col for col in df.columns]
    
    # Append the processed DataFrame to the list
    processed_dfs.append(df)

# Concatenate all the processed DataFrames
big_df = pd.concat(processed_dfs, ignore_index=True)
#save the df
big_df.to_csv(output_dir+'Big_df_demog+targ_attack_all_thresh.csv',index = True)













