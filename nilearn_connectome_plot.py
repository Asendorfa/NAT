#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 09:17:09 2024

@author: asendorfa
"""

from scipy.io import loadmat
import os
import fnmatch, glob
import numpy as np
import pandas as pd
from collections import Counter
from nilearn import plotting
import matplotlib.pyplot as plt

output_path = ('/DATA/DoMoCo/Targeted Attacks/Analysis/01_Network_Construction_CONN/Atlases/Seitzmann_300_ROI/'
                '300_ROI_Set/niLearn/DMN/')
folder       = '/DATA/DoMoCo/Targeted Attacks/Analysis/02_Attack_Analysis_GAT/5th_GO_31_Subjects/TargAttack/All_ROIs/threshold_0.100_binarized/UnThresh_CorrMatrices_f_thresh_0.100_binarized.mat'
folder2      = '/DATA/DoMoCo/Targeted Attacks/Analysis/02_Attack_Analysis_GAT/5th_GO_31_Subjects/TargAttack/All_ROIs/UnThresh_CorrMatrices_f_DoMoCo_31_sub.mat'
#import coordinates of the Seitzman atlas
df = pd.read_excel('/DATA/DoMoCo/Targeted Attacks/Analysis/01_Network_Construction_CONN/Atlases/Seitzmann_300_ROI/300_ROI_Set/ROIs_300inVol_MNI_allInfo.xlsx')
print (df['netName'].unique())
folder_FPN = '/DATA/DoMoCo/Targeted Attacks/Analysis/02_Attack_Analysis_GAT/5th_GO_31_Subjects/TargAttack/Frontoparietal_network/threshold_0.500_binarized/UnThresh_CorrMatrices_f_thresh_0.500_binarized.mat'
folder_DMN = ('/DATA/DoMoCo/Targeted Attacks/Analysis/02_Attack_Analysis_GAT/5th_GO_31_Subjects/TargAttack/DefaultMode_network/'
'threshold_0.300_binarized/UnThresh_CorrMatrices_f_thresh_0.300_binarized.mat')
#folder_DMN = '/DATA/DoMoCo/Targeted Attacks/Analysis/02_Attack_Analysis_GAT/5th_GO_31_Subjects/TargAttack/DefaultMode_network/UnThresh_CorrMatrices_f_DoMoCo_31_sub.mat'


res_mat = loadmat(folder_DMN)
cov_mat = pd.DataFrame(res_mat['ZZ'][:,:,2])
cov_mat_arr = cov_mat.to_numpy()
#plot cov matrix
ax = plotting.plot_matrix(cov_mat_arr, cmap='Spectral_r', colorbar=False)
# Save the figure from the Axes object
#ax.figure.savefig('unthresh_DMN_cov_mat3.png', dpi=500, bbox_inches='tight')

def generate_coords(df, searchterms):
    df_search =df[df['netName'].isin(searchterms)]
    coords = [(row['x'], row['y'], row['z']) for _, row in df_search.iterrows()]
    return coords

searchterms = ['DefaultMode']
coords = generate_coords(df, searchterms)
 

view = plotting.view_connectome(cov_mat_arr, coords,
                                node_color='crimson',
                                edge_cmap = 'Reds',
                                node_size = 20)
#view.open_in_browser()
view.save_as_html(output_path+'DMN_connectome_plot.html')

#ALL ROIS
coords = [(row['x'], row['y'], row['z']) for _, row in df.iterrows()]