import numpy as np
import os
from scipy.sparse import issparse

import scanpy as sc
from anndata import AnnData
import pandas as pd


def normalize_scanpy(adata, batch_key = None, type_key="type", n_high_var_gene = 2000, 
                     n_high_var_protein = 150, LVG = True, LVP = True, 
                     normalize_samples = True, log_normalize = True, normalize_features = True):
    """ This function preprocesses the raw count data.
    
    
    Arguments:
    ------------------------------------------------------------------
    - adata: `anndata.AnnData`, the annotated data matrix of shape (n_obs, n_vars) where n_vars = n_vars_gene + n_vars_protein. Rows correspond to cells and columns to genes.
    - batch_key: `str`, string specifying the name of the column in the observation dataframe which identifies the batch of each cell. If this is left as None, then all cells are assumed to be from one batch.
    - type_key: `str`, string specifying the name of the column in the variables dataframe which identifies the type of each feature, whether it is a gene (expects "Gene Expression") or a protein (expects "Antibody Capture"). By default we use "type".
    - n_high_var_gene: `int`, integer specifying the number of genes to be idntified as highly variable. E.g. if n_high_var_gene = 2000, then the 2000 genes with the highest variance are designated as highly variable.
    - n_high_var_protein: `int`, integer specifying the number of proteins to be idntified as highly variable. E.g. if n_high_var_protein = 1500, then the 150 proteins with the highest variance are designated as highly variable.
    - LVG: `bool`, Whether to retain and preprocess LVGs.
    - LVP: `bool`, Whether to retain and preprocess LVPs. 
    - normalize_samples: `bool`, If True, normalize expression of each gene in each cell by the sum of expression counts in that cell.
    - log_normalize: `bool`, If True, log transform expression. I.e., compute log(expression + 1) for each gene, cell expression count.
    - normalize_features: `bool`, If True, z-score normalize each gene's expression.
    
    Returns:
    ------------------------------------------------------------------
    - adata_gene_protein: `anndata.AnnData`, the annotated data matrix of shape (n_obs, n_vars). Contains preprocessed data (gene and protein preprocessed separately).
    """
    
    n, p = adata.shape
    sparsemode = issparse(adata.X)
    
    if batch_key is not None:
        batch = list(adata.obs[batch_key])
        batch = convert_vector_to_encoding(batch)
        batch = np.asarray(batch)
        batch = batch.astype('float32')
    else:
        batch = np.ones((n,), dtype = 'float32')
        norm_by_batch = False
        
    sc.pp.filter_genes(adata, min_counts=1)
    sc.pp.filter_cells(adata, min_counts=1)

    adata_protein = adata[:, adata.var[type_key] == "Antibody Capture"].copy()
    adata_gene = adata[:, adata.var[type_key] == "Gene Expression"].copy()

    # A. gene first 
    count_gene = adata_gene.X.copy()

    # A1. cell level normalization    
    if normalize_samples:
        out = sc.pp.normalize_total(adata_gene, inplace = False)
        obs_ = adata_gene.obs
        var_ = adata_gene.var
        adata_gene = None
        adata_gene = AnnData(out['X'])
        adata_gene.obs = obs_
        adata_gene.var = var_
        
        size_factors = out['norm_factor'] / np.median(out['norm_factor'])
        out = None
    else:
        size_factors = np.ones((adata_gene.shape[0], ))

    # A2. log normalization and hvg      
    if not log_normalize:
        adata_gene_ = adata_gene.copy()
    
    sc.pp.log1p(adata_gene)
    
    if n_high_var_gene is not None:
        sc.pp.highly_variable_genes(adata_gene, inplace = True, min_mean = 0.0125, max_mean = 3, min_disp = 0.5, 
                                          n_bins = 20, n_top_genes = n_high_var_gene, batch_key = batch_key)
        
        hvg = adata_gene.var['highly_variable'].values
        
        if not log_normalize:
            adata_gene = adata_gene_.copy()

    else:
        hvg = [True] * adata_gene.shape[1]

    # A3. scale with batch specific z score   
    if normalize_features:
        batch_list = np.unique(batch)

        if sparsemode:
            adata_gene.X = adata_gene.X.toarray()

        for batch_ in batch_list:
            indices = [x == batch_ for x in batch]
            sub_adata_gene = adata_gene[indices]
            
            sc.pp.scale(sub_adata_gene)
            adata_gene[indices] = sub_adata_gene.X
        
        adata_gene.layers["normalized input"] = adata_gene.X
        adata_gene.X = count_gene
        adata_gene.var['Variance Type'] = [['LVG', 'HVG'][int(x)] for x in hvg]
            
    else:
        if sparsemode:   
            adata_gene.layers["normalized input"] = adata_gene.X.toarray()
        else:
            adata_gene.layers["normalized input"] = adata_gene.X
            
        adata_gene.var['Variance Type'] = [['LVG', 'HVG'][int(x)] for x in hvg]

    # A4. delete not useful information           
    if n_high_var_gene is not None:
        del_keys = ['dispersions', 'dispersions_norm', 'highly_variable', 'highly_variable_intersection', 'highly_variable_nbatches', 'means']
        del_keys = [x for x in del_keys if x in adata_gene.var.keys()]
        adata_gene.var = adata_gene.var.drop(del_keys, axis = 1)
            
    y = np.unique(batch)
    num_batch = len(y)
    
    adata_gene.obs['size factors'] = size_factors.astype('float32')
    adata_gene.obs['batch'] = batch
    adata_gene.uns['num_batch'] = num_batch
    
    if sparsemode:
        adata_gene.X = adata_gene.X.toarray()
        
    if not LVG:
        adata_gene = adata_gene[:, adata_gene.var['Variance Type'] == 'HVG']


    # B. protein then 
    count_protein = adata_protein.X.copy()

    # B1. cell level normalization    
    if normalize_samples:
        out = sc.pp.normalize_total(adata_protein, inplace = False)
        obs_ = adata_protein.obs
        var_ = adata_protein.var
        adata_protein = None
        adata_protein = AnnData(out['X'])
        adata_protein.obs = obs_
        adata_protein.var = var_
        
        size_factors = out['norm_factor'] / np.median(out['norm_factor'])
        out = None
    else:
        size_factors = np.ones((adata_protein.shape[0], ))

    # B2. log normalization and hvp  
    if not log_normalize:
        adata_protein_ = adata_protein.copy()
    
    sc.pp.log1p(adata_protein)
    
    if n_high_var_protein is not None:
        sc.pp.highly_variable_genes(adata_protein, inplace = True, min_mean = 0.0125, max_mean = 3, min_disp = 0.5, 
                                          n_bins = 20, n_top_genes = n_high_var_protein, batch_key = batch_key)
        
        hvp = adata_protein.var['highly_variable'].values
        
        if not log_normalize:
            adata_protein = adata_protein_.copy()

    else:
        hvp = [True] * adata_protein.shape[1]

    # B3. scale with batch specific z score   
    if normalize_features:
        batch_list = np.unique(batch)

        if sparsemode:
            adata_protein.X = adata_protein.X.toarray()

        for batch_ in batch_list:
            indices = [x == batch_ for x in batch]
            sub_adata_protein = adata_protein[indices]
            
            sc.pp.scale(sub_adata_protein)
            adata_protein[indices] = sub_adata_protein.X
        
        adata_protein.layers["normalized input"] = adata_protein.X
        adata_protein.X = count_protein
        adata_protein.var['Variance Type'] = [['LVP', 'HVP'][int(x)] for x in hvp]
            
    else:
        if sparsemode:   
            adata_protein.layers["normalized input"] = adata_protein.X.toarray()
        else:
            adata_protein.layers["normalized input"] = adata_protein.X
            
        adata_protein.var['Variance Type'] = [['LVP', 'HVP'][int(x)] for x in hvg]

    # B4. delete not useful information           
    if n_high_var_protein is not None:
        del_keys = ['dispersions', 'dispersions_norm', 'highly_variable', 'highly_variable_intersection', 'highly_variable_nbatches', 'means']
        del_keys = [x for x in del_keys if x in adata_protein.var.keys()]
        adata_protein.var = adata_protein.var.drop(del_keys, axis = 1)
            
    y = np.unique(batch)
    num_batch = len(y)
    
    adata_protein.obs['size factors'] = size_factors.astype('float32')
    adata_protein.obs['batch'] = batch
    adata_protein.uns['num_batch'] = num_batch
    
    if sparsemode:
        adata_protein.X = adata_protein.X.toarray()
        
    if not LVP:
        adata_protein = adata_protein[:, adata_protein.var['Variance Type'] == 'HVP']


    # C. merge gene and protein as one dataset
    adata_gene_protein=AnnData(
        X=np.concatenate((adata_gene.X, adata_protein.X), axis=1),
        obs=adata_gene.obs,
        var=pd.concat([adata_gene.var, adata_protein.var]))

    adata_gene_protein.layers['normalized input'] = np.concatenate((
        adata_gene.layers['normalized input'], adata_protein.layers['normalized input']), axis=1)

    adata_gene_protein.obs.rename(columns={"size factors": "size factors gene"}, inplace=True)
    adata_gene_protein.obs['size factors protein'] = adata_protein.obs['size factors']

    return adata_gene_protein


def build_dir(dir_path):
    """ This function builds a directory if it does not exist.
    
    
    Arguments:
    ------------------------------------------------------------------
    - dir_path: `str`, The directory to build. E.g. if dir_path = 'folder1/folder2/folder3', then this function will creates directory if folder1 if it does not already exist. Then it creates folder1/folder2 if folder2 does not exist in folder1. Then it creates folder1/folder2/folder3 if folder3 does not exist in folder2.
    """
    
    subdirs = [dir_path]
    substring = dir_path

    while substring != '':
        splt_dir = os.path.split(substring)
        substring = splt_dir[0]
        subdirs.append(substring)
        
    subdirs.pop()
    subdirs = [x for x in subdirs if os.path.basename(x) != '..']

    n = len(subdirs)
    subdirs = [subdirs[n - 1 - x] for x in range(n)]
    
    for dir_ in subdirs:
        if not os.path.isdir(dir_):
            os.mkdir(dir_)


def convert_string_to_encoding(string, vector_key):
    """A function to convert a string to a numeric encoding.
    
    
    Arguments:
    ------------------------------------------------------------------
    - string: `str`, The specific string to convert to a numeric encoding.
    - vector_key: `np.ndarray`, Array of all possible values of string.
    
    Returns:
    ------------------------------------------------------------------
    - encoding: `int`, The integer encoding of string.
    """
    
    return np.argwhere(vector_key == string)[0][0]


def convert_vector_to_encoding(vector):
    """A function to convert a vector of strings to a dense numeric encoding.
    
    
    Arguments:
    ------------------------------------------------------------------
    - vector: `array_like`, The vector of strings to encode.
    
    Returns:
    ------------------------------------------------------------------
    - vector_num: `list`, A list containing the dense numeric encoding.
    """
    
    vector_key = np.unique(vector)
    vector_strings = list(vector)
    vector_num = [convert_string_to_encoding(string, vector_key) for string in vector_strings]
    
    return vector_num


def find_resolution(adata_, n_clusters, random):
    """A function to find the louvain resolution tjat corresponds to a prespecified number of clusters, if it exists.
    
    
    Arguments:
    ------------------------------------------------------------------
    - adata_: `anndata.AnnData`, the annotated data matrix of shape (n_obs, n_vars). Rows correspond to cells and columns to low dimension features.
    - n_clusters: `int`, Number of clusters.
    - random: `int`, The random seed.
    
    Returns:
    ------------------------------------------------------------------
    - resolution: `float`, The resolution that gives n_clusters after running louvain's clustering algorithm.
    """
    
    obtained_clusters = -1
    iteration = 0
    resolutions = [0., 1000.]
    
    while obtained_clusters != n_clusters and iteration < 50:
        current_res = sum(resolutions)/2
        adata = sc.tl.louvain(adata_, resolution = current_res, random_state = random, copy = True)
        labels = adata.obs['louvain']
        obtained_clusters = len(np.unique(labels))
        
        if obtained_clusters < n_clusters:
            resolutions[0] = current_res
        else:
            resolutions[1] = current_res
        
        iteration = iteration + 1
        
    return current_res

