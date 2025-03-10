%Script to threshold and binarize correlation matrices based on the
%threshold propotional function of the Brain connectivity toolbox. Hence,
%Brain Connectivity Toolbox install is needed. For more information about
%the function type : doc threshold_proportional
%Author: Adrian Asendorf

%=========================Magic Numbers====================================
% Specify whether to binarize the result_matrix (yes or no)
binarize_result = 'yes'; % Change to 'no' if you don't want to binarize
%_list_sources
% Define the list of thresholds you want to use
thresholds = 0.1:0.05:0.5; % Add or change thresholds as needed
%=========================================================================

% Load the matrix from the .mat file
load('UnThresh_CorrMatrices_f_DoMoCo_PD_1.mat');

% Get the dimensions of the 3D matrix
matrix_size = size(ZZ);
ZZ_raw= ZZ;
% Iterate through the list of thresholds
for t = 1:length(thresholds)
    % Get the current threshold value
    threshold = thresholds(t);
    
    % Initialize an empty storage matrix with the same dimensions
    thresholded_matrix = zeros(matrix_size);
    MaxD= zeros([1, matrix_size(3)]);
    % Loop through the matrices
    for i = 1:matrix_size(3)
        % Extract the ith matrix from the 3D array
        input_matrix = ZZ_raw(:,:,i);
        
        % Apply the brain connectivity function: threshold_proportional to the unthresh matrix
        result_matrix = threshold_proportional(input_matrix, threshold);
        
        %In some cases there are minimaldifferces in matrix symetry
        %if they are present we need to Enforce Symetry on the matrix
        difference = result_matrix - result_matrix';% Check if matrix_k is symmetric within tolerance
        symmetry_difference = sum(abs(difference(:)));
        if symmetry_difference > 0 %if asymetry present
            disp([num2str(i),': Matrix diff of: ', num2str(symmetry_difference),'detected']);
            disp(['Focring Symmetry ... '])
            result_matrix = (result_matrix + result_matrix') / 2; %we take the average of the differences by doing over whole matrix if not asymetric this does not affect results
        end
        % Binarize the result_matrix if specified
        if strcmpi(binarize_result, 'yes')
            result_matrix = result_matrix > 0;
        end
        
        % Store the result in the thresholded_matrix
        thresholded_matrix(:,:,i) = result_matrix;
        %change MaxD, which ist the density of the given network using the
        %densitiy_und funciton using the newly thresholded result_matrix
        MaxD(:,i)=density_und(result_matrix);
    end
    
    %Define ZZ again as thresholded_matrix
    ZZ= thresholded_matrix;
    
    % Define the number of decimal places you want in the filename
    decimal_places = 3;
    
    % Create a formatted string of the threshold value with the desired number of decimal places
    threshold_str = sprintf(['%0.', num2str(decimal_places), 'f'], threshold);
    
    % Include binarize_result in the filename
    binarize_suffix = '';
    if strcmpi(binarize_result, 'yes')
        binarize_suffix = '_binarized';
    end
    
    % Create the filename string with the rounded threshold value and binarize_suffix
    result_file_name = ['UnThresh_CorrMatrices_f_thresh_', threshold_str, binarize_suffix, '.mat'];
    
     % Create a directory with the threshold value and the binarize suffix
    directory_name = ['threshold_', threshold_str, binarize_suffix];
    %full_directory_path = fullfile(base_directory, directory_name);
    
    % Create the directory if it doesn't exist
    if ~exist(directory_name, 'dir')
        mkdir(directory_name);
    end
    
    % Define the full file path within the new directory
    result_file_path = fullfile(directory_name, result_file_name);
    
    % Save the resulting matrix under the specified name and directory
    save(result_file_path, 'ZZ', 'MaxD');
end
