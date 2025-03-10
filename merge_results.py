#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 14:43:53 2024

@author: asendorfa
"""
import os 
import pandas as pd
output_dir   =  os.getcwd() +'/'
#/DATA/DoMoCo/Targeted Attacks/Analysis/03_Results/5.2th_GO_19PD+6PD_preupdate/1_sub/Big_df_demog+targ_attack_all_thresh.csv
big_df1 = pd.read_csv(output_dir+'1_sub/Big_df_demog+targ_attack_all_thresh.csv')
big_df5 = pd.read_csv(output_dir+'5_sub/Big_df_demog+targ_attack_all_thresh.csv')
big_df19 = pd.read_csv(output_dir+'19_sub/Big_df_demog+targ_attack_all_thresh.csv')


big_df = pd.concat([big_df1, big_df5, big_df19], ignore_index=True)

#drop empty PA ids
big_df = big_df[big_df['Met_50'].notna()]
big_df = big_df[big_df['gmp'].notna()]
#big_df = big_df[big_df['gcp'].notna()]
big_df = big_df[big_df['mean_putamen'].notna()]

big_df = big_df.sort_values(by=['Density', 'ID'], ascending=True)
big_df.to_csv(output_dir+'/25_Merged_all_PD/merge_Big_df_demog+targ_attack_all_thresh.csv',index = True)

