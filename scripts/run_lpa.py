from visualize import plot_pca
from LPA import PCA
import os
from LPA import Corpus, sockpuppet_distance , PCA
import pandas as pd
import seaborn as sns


def rename_matrix(df):
    for col in df.columns:
        if col.lower().startswith('write me'):
            df.rename(columns={col: 'prompt'}, inplace=True)
        else:
            df.rename(columns={col: 'real'}, inplace=True)
    for i, index_name in enumerate(df.index):
        if index_name.lower().startswith('write me'):
            df.rename(index={index_name: 'prompt ' + str(i)}, inplace=True)
        else:
            df.rename(index={index_name: 'real ' + str(i)}, inplace=True)
    return df


def calculate_distances(dvr_path, folder, outpath):
    """
    Calculates the Euclidean distances between a reference vector (the global_weight column of df)
    and all other vectors in a folder containing dataframes representing vectors.
    
    Args:
    - df (pd.DataFrame): A pandas DataFrame containing a column named 'global_weight' that will
    be used as the reference vector.
    - folder (str): Path to the folder containing CSV files representing other vectors.
    
    Returns:
    - A pandas DataFrame containing the distances between the reference vector and all other vectors.
    """
    dvr_frame = pd.read_csv(dvr_path, low_memory = False)
    # Create an empty list to hold the distances
    distances = []
    
       # Iterate over all CSV files in the folder
    for file_name in os.listdir(folder):
        # Check if the file is a CSV file
        if file_name.endswith('.csv'):
            # Load the CSV file into a pandas DataFrame
            df = pd.read_csv(os.path.join(folder, file_name))
            # Calculate the Euclidean distance between the reference vector and the current vector
            distance = compute_distance_15052023(df)
            # Add the distance to the list
            distances.append(distance)
            
    distances_df = pd.DataFrame(distances, columns=['Distance'], index=os.listdir(folder))
    
    distances_df.to_csv(outpath,mode='w',header=True, index=True)
    return distances_df


def wordfreq_random_files(prompt_folder , num_files=2):
    # Get a list of all files in the prompt folder
    all_files = os.listdir(prompt_folder)
    
    # If the sample size is larger than the number of files, set the sample size to the number of files
    sample_size = min(num_files, len(all_files))
    
    # Select num_files random files from the list
    random_files = random.sample(all_files, sample_size)
    dfs = []

    # Loop through each file in the directory
    for file_name in random_files:
        # Check if the file is a CSV file
        if file_name.endswith('.csv'):
            # Read the file into a DataFrame and append it to the list
            file_path = os.path.join(prompt_folder, file_name)
            df = pd.read_csv(file_path)
            dfs.append(df)
    # Concatenate all the DataFrames into a single DataFrame
    df = pd.concat(dfs, ignore_index=True)
    return df


def run_lpa(freq_folder , out_path , experiment_title, to_spd = False):
    out_folder = out_path+"/"+experiment_title
    os.makedirs(out_path+"/"+key_word , exist_ok=True)
    freq = wordfreq_random_files(freq_folder , num_files=4500)
    freq.rename(columns={'origin_index': 'document', 'word': 'element' , 'frequency': 'frequency_in_document'}, inplace=True)
    #Create Corpus
    corpus = Corpus(freq=freq)
    
    #Create DVR
    dvr = corpus.create_dvr()
    dvr_path = out_folder+"/"+experiment_title+"-dvr.csv"
    dvr.to_csv(dvr_path ,mode='w',header=True, index=False)
    #Create Epsilon
    # epsilon_frac = 2 # Change the epsilon to get better results
    epsilon = 1 / (len(dvr) * epsilon_frac)
    #Create Signatures
    signatures = corpus.create_signatures(epsilon=epsilon, sig_length=100, distance="KLDe")
    export_signatures(signatures , outputFolder = out_folder+"/Signatures/")
    all_distances = calculate_distances(dvr_path , out_folder+"/Signatures/" , out_folder+"/Results/all-distances.csv")
    if to_spd:
        spd = sockpuppet_distance(corpus, corpus , res = "matrix" )
        spd.to_csv(out_folder+"/Results/SPD_Matrix.csv",mode='w',header=True, index=True)
        spd_heatmap = rename_matrix(spd)
        fig = plt.figure(figsize=(15, 15))
        heatmap = sns.heatmap(spd_heatmap, cmap='viridis', annot=False ,ax=fig.gca())
        heatmap.figure.savefig(out_folder+"/Images-"+exp_date+"/heatmap.jpg")
        pca, evr = PCA(spd, n_components=2)
        plot_pca(pca,spd.index).save(out_folder+"/Images-"+exp_date+'pca_plot.html') 
