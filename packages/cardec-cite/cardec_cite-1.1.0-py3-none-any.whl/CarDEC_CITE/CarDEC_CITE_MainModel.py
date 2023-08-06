from .CarDEC_CITE_SAE import SAE
from .CarDEC_CITE_utils import build_dir, find_resolution
from .CarDEC_CITE_layers import ClusteringLayer
from .CarDEC_CITE_optimization import grad_MainModel as grad, total_loss, MSEloss
from .CarDEC_CITE_dataloaders import simpleloader, dataloader, tupleloader

import tensorflow as tf
from tensorflow.keras import Model, Sequential
from tensorflow.keras.layers import Dense, concatenate
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.backend import set_floatx

from sklearn.cluster import KMeans

import scanpy as sc
from anndata import AnnData
import pandas as pd

import random
import numpy as np
from math import ceil

import os
from copy import deepcopy
from time import time

set_floatx('float32')

class CarDEC_CITE_Model(Model):
    def __init__(self, adata, dims, LVGP_dims = None, tol = 0.005, n_clusters = None, random_seed = 201809, 
                 louvain_seed = 0, n_neighbors = 15, pretrain_epochs = 300, batch_size = 64, decay_factor = 1/3, 
                 patience_LR = 3, patience_ES = 9, act = 'relu', actincenter = "tanh", ae_lr = 1e-04, clust_weight = 1., 
                 load_encoder_weights = True, set_centroids = True, weights_dir = "CarDEC_CITE Weights"):
        super(CarDEC_CITE_Model, self).__init__()
        """ This class creates the TensorFlow CarDEC_CITE model architecture.


        Arguments:
        ------------------------------------------------------------------
        - adata: `anndata.AnnData`, the annotated data matrix of shape (n_obs, n_vars). Rows correspond to cells and columns to genes.
        - dims: `list`, the number of output features for each layer of the HVGP encoder. The length of the list determines the number of layers.
        - LVGP_dims: `list`, the number of output features for each layer of the LVGP encoder. The length of the list determines the number of layers.
        - tol: `float`, stop criterion, clustering procedure will be stopped when the difference ratio between the current iteration and last iteration larger than tol.
        - n_clusters: `int`, The number of clusters into which cells will be grouped.
        - random_seed: `int`, The seed used for random weight intialization.
        - louvain_seed: `int`, The seed used for louvain clustering intialization.
        - n_neighbors: `int`, The number of neighbors used for building the graph needed for louvain clustering.
        - pretrain_epochs: `int`, The maximum number of epochs for pretraining the HVG autoencoder. In practice, early stopping criteria should stop training much earlier.
        - batch_size: `int`, The batch size used for pretraining the HVG autoencoder.
        - decay_factor: `float`, The multiplicative factor by which to decay the learning rate when validation loss is not decreasing.
        - patience_LR: `int`, the number of epochs which the validation loss is allowed to increase before learning rate is decayed when pretraining the autoencoder.
        - patience_ES: `int`, the number of epochs which the validation loss is allowed to increase before training is halted when pretraining the autoencoder.
        - act: `str`, The activation function used for the intermediate layers of CarDEC_CITE, other than the bottleneck layer.
        - actincenter: `str`, The activation function used for the bottleneck layer of CarDEC_CITE.
        - ae_lr: `float`, The learning rate for pretraining the HVG autoencoder.
        - clust_weight: `float`, a number between 0 and 2 qhich balances the clustering and reconstruction losses.
        - load_encoder_weights: `bool`, If True, the API will try to load the weights for the HVG encoder from the weight directory.
        - set_centroids: `bool`, If True, intialize the centroids by running Louvain's algorithm.
        - weights_dir: `str`, the path in which to save the weights of the CarDEC_CITE model.
        ------------------------------------------------------------------
        """
        
        assert clust_weight <= 2. and clust_weight>=0.
        
        tf.keras.backend.clear_session()
                    
        self.dims = dims
        self.LVGP_dims = LVGP_dims
        self.tol = tol
        self.input_dim = dims[0]  # for clustering layer 
        self.n_stacks = len(self.dims) - 1
        self.n_neighbors = n_neighbors
        self.batch_size = batch_size
        self.random_seed = random_seed
        self.activation = act
        self.actincenter = actincenter
        self.load_encoder_weights = load_encoder_weights
        self.clust_weight = clust_weight
        self.weights_dir = weights_dir
        self.preclust_embedding = None
        
        # set random seed
        random.seed(random_seed)
        np.random.seed(random_seed)
        tf.random.set_seed(random_seed)
        self.splitseed = round(abs(10000*np.random.randn()))
        
        # build the autoencoder
        self.sae = SAE(dims = self.dims, act = self.activation, actincenter = self.actincenter, 
                       random_seed = random_seed, splitseed = self.splitseed, init="glorot_uniform", optimizer = Adam(), 
                       weights_dir = weights_dir)
        
        build_dir(self.weights_dir)
        
        decoder_seed = round(100 * abs(np.random.normal()))
        if load_encoder_weights:
            if os.path.isfile("./" + self.weights_dir + "/pretrained_autoencoder_weights.index"):
                print("Pretrain weight index file detected, loading weights.")
                self.sae.load_autoencoder()
                print("Pretrained high variance autoencoder weights initialized.")
            else:
                print("Pretrain weight index file not detected, pretraining autoencoder weights.\n")
                self.sae.train(adata, lr = ae_lr, num_epochs = pretrain_epochs, 
                               batch_size = batch_size, decay_factor = decay_factor, 
                               patience_LR = patience_LR, patience_ES = patience_ES)
                self.sae.load_autoencoder()
        else:
            print("Pre-training high variance autoencoder.\n")
            self.sae.train(adata, lr = ae_lr, num_epochs = pretrain_epochs, 
                           batch_size = batch_size, decay_factor = decay_factor, 
                           patience_LR = patience_LR, patience_ES = patience_ES)
            self.sae.load_autoencoder()
        
        features = self.sae.embed(adata)
        self.preclust_emb = deepcopy(features)
        self.preclust_denoised = self.sae.denoise(adata, batch_size)
                
        if not set_centroids:
            self.init_centroid = np.zeros((n_clusters, self.dims[-1]), dtype = 'float32')
            self.n_clusters = n_clusters
            self.init_pred = np.zeros((adata.shape[0], dims[-1]))
            
        elif louvain_seed is None:
            print("\nInitializing cluster centroids using K-Means")

            kmeans = KMeans(n_clusters=n_clusters, n_init = 20)
            Y_pred_init = kmeans.fit_predict(features)

            self.init_pred = deepcopy(Y_pred_init)
            self.n_clusters = n_clusters
            self.init_centroid = kmeans.cluster_centers_
            
        else:
            print("\nInitializing cluster centroids using the louvain method.")
            
            n_cells = features.shape[0]
            
            if n_cells > 10**5:
                subset = np.random.choice(range(n_cells), 10**5, replace = False)
                adata0 = AnnData(features[subset])
            else: 
                adata0 = AnnData(features)

            sc.pp.neighbors(adata0, n_neighbors = self.n_neighbors, use_rep="X")
            self.resolution = find_resolution(adata0, n_clusters, louvain_seed)
            adata0 = sc.tl.louvain(adata0, resolution = self.resolution, random_state = louvain_seed, copy = True)

            Y_pred_init = adata0.obs['louvain']
            self.init_pred = np.asarray(Y_pred_init, dtype=int)

            features = pd.DataFrame(adata0.X, index = np.arange(0, adata0.shape[0]))
            Group = pd.Series(self.init_pred, index = np.arange(0, adata0.shape[0]), name="Group")
            Mergefeature = pd.concat([features, Group],axis=1)

            self.init_centroid = np.asarray(Mergefeature.groupby("Group").mean())
            self.n_clusters = self.init_centroid.shape[0]

            print("\n " + str(self.n_clusters) + " clusters detected. \n")
        
        self.encoder = self.sae.encoder
        self.decoder = self.sae.decoder
        
        if LVGP_dims is not None:
            n_stacks = len(dims) - 1

            LVGP_encoder_layers = []

            for i in range(n_stacks-1):
                LVGP_encoder_layers.append(Dense(LVGP_dims[i + 1], kernel_initializer = 'glorot_uniform', activation = self.activation, name='encoder%d' % i))

            LVGP_encoder_layers.append(Dense(LVGP_dims[-1], kernel_initializer = 'glorot_uniform', activation = self.actincenter, name='embedding'))
            self.encoderLVGP = Sequential(LVGP_encoder_layers, name = 'encoderLVGP')

        if LVGP_dims is not None:
            decoder_layers = []
            for i in range(self.n_stacks - 1, 0, -1):
                decoder_layers.append(Dense(self.LVGP_dims[i], kernel_initializer = 'glorot_uniform', 
                                            activation = self.activation, name='decoderLVGP%d' % (i-1)))
                
            decoder_layers.append(Dense(self.LVGP_dims[0], activation = 'linear', name='outputLVGP'))
            self.decoderLVGP = Sequential(decoder_layers, name = 'decoderLVGP')
        
        self.clustering_layer = ClusteringLayer(centroids = self.init_centroid, name = 'clustering')
        
        del self.sae
        
        self.construct()
        
    def construct(self, summarize = True):
        """ This class method fully initalizes the TensorFlow model.


        Arguments:
        ------------------------------------------------------------------
        - summarize: `bool`, If True, then print a summary of the model architecture.
        """
        
        x = [tf.zeros(shape = (1, self.dims[0]), dtype=float), None]
        if self.LVGP_dims is not None:
            x[1] = tf.zeros(shape = (1, self.LVGP_dims[0]), dtype=float)
            
        out = self(*x)
        
        if summarize:
            print("\n-----------------------CarDEC_CITE Architecture-----------------------\n")
            self.summary()

            print("\n--------------------Encoder Sub-Architecture--------------------\n")
            self.encoder.summary()
            
            print("\n------------------Base Decoder Sub-Architecture------------------\n")
            self.decoder.summary()

            if self.LVGP_dims is not None:
                print("\n------------------LVGP Encoder Sub-Architecture------------------\n")
                self.encoderLVGP.summary()

                print("\n----------------LVGP Base Decoder Sub-Architecture----------------\n")
                self.decoderLVGP.summary()

    def call(self, hvgp, lvgp, denoise = True):
        """ This is the forward pass of the model.
        

        ***Inputs***
            - hvgp: `tf.Tensor`, an input tensor of shape (n_obs, n_HVG + n_HVP).
            - lvgp: `tf.Tensor`, (Optional) an input tensor of shape (n_obs, n_LVG + n_LVP).
            - denoise: `bool`, (Optional) If True, return denoised expression values for each cell.
            
        ***Outputs***
            - denoised_output: `dict`, (Optional) Dictionary containing denoised tensors.
            - cluster_output: `tf.Tensor`, a tensor of cell cluster membership probabilities of shape (n_obs, m).
        """
        
        hvgp = self.encoder(hvgp)

        cluster_output = self.clustering_layer(hvgp)
        
        if not denoise:
            return cluster_output

        HVGP_denoised_output = self.decoder(hvgp)
        denoised_output = {'HVGP_denoised': HVGP_denoised_output}

        if self.LVGP_dims is not None:
            lvgp = self.encoderLVGP(lvgp)
            z = concatenate([hvgp, lvgp], axis=1)

            LVGP_denoised_output = self.decoderLVGP(z)

            denoised_output['LVGP_denoised'] = LVGP_denoised_output

        return denoised_output, cluster_output

    @staticmethod
    def target_distribution(q):
        """ Updates target distribution cluster assignment probabilities given CarDEC_CITE output.
        
        
        Arguments:
        ------------------------------------------------------------------
        - q: `tf.Tensor`, a tensor of shape (b, m) identifying the probability that each of b cells is in each of the m clusters. Obtained as output from CarDEC_CITE.
        
        Returns:
        ------------------------------------------------------------------
        - p: `tf.Tensor`, a tensor of shape (b, m) identifying the pseudo-label probability that each of b cells is in each of the m clusters.
        """
        
        weight = q ** 2 / np.sum(q, axis = 0)
        p = weight.T / np.sum(weight, axis = 1)
        return p.T
    
    def make_generators(self, adata, val_split, batch_size):
        """ This class method creates training and validation data generators for the current input data and pseudo labels.
        
        
        Arguments:
        ------------------------------------------------------------------
        - adata: `anndata.AnnData`, the annotated data matrix of shape (n_obs, n_vars). Rows correspond to cells and columns to genes.
        - val_split: `float`, The fraction of cells to be reserved for validation during this step.
        - batch_size: `int`, The batch size used for training the full model.
        - p: `tf.Tensor`, a tensor of shape (b, m) identifying the pseudo-label probability that each of b cells is in each of the m clusters.
        - splitseed: `int`, The seed used to split cells between training and validation. Should be consistent between iterations to ensure the same cells are always used for validation.
        - newseed: `int`, The seed that is set after splitting cells between training and validation. Should be different every iteration so that stochastic operations other than splitting cells between training and validation vary between epochs.
        
        Returns:
        ------------------------------------------------------------------
        - train_dataset: `tf.data.Dataset`, Dataset that returns training examples.
        - val_dataset: `tf.data.Dataset`, Dataset that returns validation examples.
        """
                
        if self.LVGP_dims is None:
            hvgp_input = adata.layers["normalized input"]
            hvgp_target = adata.layers["normalized input"]
            lvgp_input = None
            lvgp_target = None
        else:
            hvgp_input = adata.layers["normalized input"][:, (adata.var['Variance Type'] == 'HVG') | (adata.var['Variance Type'] == 'HVP')]
            hvgp_target = adata.layers["normalized input"][:, (adata.var['Variance Type'] == 'HVG') | (adata.var['Variance Type'] == 'HVP')]
            lvgp_input = adata.layers["normalized input"][:, (adata.var['Variance Type'] == 'LVG') | (adata.var['Variance Type'] == 'LVP')]
            lvgp_target = adata.layers["normalized input"][:, (adata.var['Variance Type'] == 'LVG') | (adata.var['Variance Type'] == 'LVP')]
                    
        return dataloader(hvgp_input, hvgp_target, lvgp_input, lvgp_target, val_split, batch_size, self.splitseed)
        
    def train_loop(self, train_dataset):
        """ This class method runs the training loop.
        
        
        Arguments:
        ------------------------------------------------------------------
        - train_dataset: `tf.data.Dataset`, Dataset that returns training examples.
        
        Returns:
        ------------------------------------------------------------------
        - epoch_loss_avg: `float`, The mean training loss for the iteration.
        """

        epoch_loss_avg = tf.keras.metrics.Mean()
        
        for inputs, target, LVGP_target, batch_p in train_dataset(val = False):
            loss_value, grads = grad(self, inputs, target, batch_p, total_loss = total_loss,
                                     LVGP_target = LVGP_target, aeloss_fun = MSEloss, 
                                     clust_weight = self.clust_weight)
            self.optimizer.apply_gradients(zip(grads, self.trainable_variables))
            epoch_loss_avg(loss_value)
                
        return epoch_loss_avg.result()
                
    def validation_loop(self, val_dataset):
        """ This class method runs the validation loop.
        
        
        Arguments:
        ------------------------------------------------------------------
        - val_dataset: `tf.data.Dataset`, Dataset that returns validation examples.
        
        Returns:
        ------------------------------------------------------------------
        - epoch_loss_avg: `float`, The mean validation loss for the iteration (reconstruction + clustering loss)
        - epoch_aeloss_avg_val: `float`, The mean validation reconstruction loss for the iteration
        """

        epoch_loss_avg_val = tf.keras.metrics.Mean()
        epoch_aeloss_avg_val = tf.keras.metrics.Mean()
            
        for inputs, target, LVGP_target, batch_p in val_dataset(val = True):
            denoised_output, cluster_output = self(*inputs)
            loss_value, aeloss = total_loss(target, denoised_output, batch_p, cluster_output, 
                           LVGP_target = LVGP_target, aeloss_fun = MSEloss, clust_weight = self.clust_weight)
            epoch_loss_avg_val(loss_value)
            epoch_aeloss_avg_val(aeloss)
                
        return epoch_loss_avg_val.result(), epoch_aeloss_avg_val.result()
    
    def package_output(self, adata, init_pred, preclust_denoised, preclust_emb):
        """ This class adds some quantities to the adata object.
        
        
        Arguments:
        ------------------------------------------------------------------
        - adata: `anndata.AnnData`, the annotated data matrix of shape (n_obs, n_vars). Rows correspond to cells and columns to genes.
        - init_pred: `np.ndarray`, the array of initial cluster assignments for each cells, of shape (n_obs,).
        - preclust_denoised: `np.ndarray`, This is the array of feature zscores denoised with the pretrained autoencoder of shape (n_obs, n_vars).
        - preclust_emb: `np.ndarray`, This is the latent embedding from the pretrained autoencoder of shape (n_obs, n_embedding).
        """        
        
        adata.obsm['precluster denoised'] = preclust_denoised
        adata.obsm['precluster embedding'] = preclust_emb
        if adata.shape[0] == init_pred.shape[0]:
            adata.obsm['initial assignments'] = init_pred
    
    def embed(self, adata, batch_size):
        """ This class method can be used to compute the low-dimension embedding for HVGP features. 
        
        
        Arguments:
        ------------------------------------------------------------------
        - adata: `anndata.AnnData`, The annotated data matrix of shape (n_obs, n_vars). Rows correspond to cells and columns to genes.
        - batch_size: `int`, The batch size for filling the array of low dimension embeddings.
        
        Returns:
        ------------------------------------------------------------------
        - embedding: `np.ndarray`, Array of shape (n_obs, p_embedding) containing the HVGP embedding for every cell in the dataset.
        """
        
        input_ds = simpleloader(adata.layers["normalized input"][:, (adata.var['Variance Type'] == 'HVG') | (adata.var['Variance Type'] == 'HVP')], batch_size)
        
        embedding = np.zeros((adata.shape[0], self.dims[-1]), dtype = 'float32')
        start = 0

        for x in input_ds:
            end = start + x.shape[0]
            embedding[start:end] = self.encoder(x).numpy()
            start = end
            
        return embedding
    
    def embed_LVGP(self, adata, batch_size):
        """ This class method can be used to compute the low-dimension embedding for LVGP features. 
        
        
        Arguments:
        ------------------------------------------------------------------
        - adata: `anndata.AnnData`, The annotated data matrix of shape (n_obs, n_vars). Rows correspond to cells and columns to genes.
        - batch_size: `int`, The batch size for filling the array of low dimension embeddings.
        
        Returns:
        ------------------------------------------------------------------
        - embedding: `np.ndarray`, Array of shape (n_obs, n_embedding) containing the LVGP embedding for every cell in the dataset.
        """
        
        input_ds = simpleloader(adata.layers["normalized input"][:, (adata.var['Variance Type'] == 'LVG') | (adata.var['Variance Type'] == 'LVP')], batch_size)

        LVGP_embedded = np.zeros((adata.shape[0], self.LVGP_dims[-1]), dtype = 'float32')
        start = 0

        for x in input_ds:
            end = start + x.shape[0]
            LVGP_embedded[start:end] = self.encoderLVGP(x).numpy()
            start = end

        return np.concatenate((adata.obsm['embedding'], LVGP_embedded), axis = 1)
    
    def make_outputs(self, adata, batch_size, denoise = True):
        """ This class method can be used to pack all relvant outputs into the adata object after training.
        
        
        Arguments:
        ------------------------------------------------------------------
        - adata: `anndata.AnnData`, The annotated data matrix of shape (n_obs, n_vars).
        - batch_size: `int`, The batch size for filling the array of low dimension embeddings.
        - denoise: `bool`, Whether to provide denoised expression values for all cells.
        """
        
        if not denoise:
            input_ds = simpleloader(adata.layers["normalized input"][:, (adata.var['Variance Type'] == 'HVG') | (adata.var['Variance Type'] == 'HVP')], batch_size)
            adata.obsm["cluster memberships"] = np.zeros((adata.shape[0], self.n_clusters), dtype = 'float32')
            
            start = 0     
            for x in input_ds:
                q_batch = self(x, None, False)
                end = start + q_batch.shape[0]
                adata.obsm["cluster memberships"][start:end] = q_batch.numpy()
            
                start = end
            
            
        elif self.LVGP_dims is not None:
            if not ('embedding' in list(adata.obsm) and 'LVGP embedding' in list(adata.obsm)):
                        adata.obsm['embedding'] = self.embed(adata, batch_size)
                        adata.obsm['LVGP embedding'] = self.embed_LVGP(adata, batch_size)
            input_ds = tupleloader(adata.obsm["embedding"], adata.obsm["LVGP embedding"], batch_size = batch_size)
            
            adata.obsm["cluster memberships"] = np.zeros((adata.shape[0], self.n_clusters), dtype = 'float32')
            adata.layers["denoised"] = np.zeros(adata.shape, dtype = 'float32')
            
            start = 0     
            for input_ in input_ds:
                denoised_batch = {'HVGP_denoised': self.decoder(input_[0]), 'LVGP_denoised': self.decoderLVGP(input_[1])}
                q_batch = self.clustering_layer(input_[0])
                end = start + q_batch.shape[0]
                
                adata.obsm["cluster memberships"][start:end] = q_batch.numpy()
                adata.layers["denoised"][start:end, (adata.var['Variance Type'] == 'HVG') | (adata.var['Variance Type'] == 'HVP')] = denoised_batch['HVGP_denoised'].numpy()
                adata.layers["denoised"][start:end, (adata.var['Variance Type'] == 'LVG') | (adata.var['Variance Type'] == 'LVP')] = denoised_batch['LVGP_denoised'].numpy()
            
                start = end
        
        else:
            if not ('embedding' in list(adata.obsm)):
                adata.obsm['embedding'] = self.embed(adata, batch_size)
            input_ds = simpleloader(adata.obsm["embedding"], batch_size)
            
            adata.obsm["cluster memberships"] = np.zeros((adata.shape[0], self.n_clusters), dtype = 'float32')
            adata.layers["denoised"] = np.zeros(adata.shape, dtype = 'float32')
            
            start = 0
            
            for input_ in input_ds:
                denoised_batch = {'HVGP_denoised': self.decoder(input_)}
                q_batch = self.clustering_layer(input_)
                
                end = start + q_batch.shape[0]
                
                adata.obsm["cluster memberships"][start:end] = q_batch.numpy()
                adata.layers["denoised"][start:end] = denoised_batch['HVGP_denoised'].numpy()
                
                start = end
                
    def train(self, adata, batch_size = 64, val_split = 0.1, lr = 1e-04, decay_factor = 1/3,
              iteration_patience_LR = 3, iteration_patience_ES = 6, 
              maxiter = 1e3, epochs_fit = 1, optimizer = Adam(), printperiter = None, denoise = True):
        """ This class method can be used to train the main CarDEC_CITE model
        
        
        Arguments:
        ------------------------------------------------------------------
        - adata: `anndata.AnnData`, The annotated data matrix of shape (n_obs, n_vars).
        - batch_size: `int`, The batch size used for training the full model.
        - val_split: `float`, The fraction of cells to be reserved for validation during this step.
        - lr: `float`, The learning rate for training the full model.
        - decay_factor: `float`, The multiplicative factor by which to decay the learning rate when validation loss is not decreasing.
        - iteration_patience_LR: `int`, The number of iterations tolerated before decaying the learning rate during which the number of cells that change assignment is less than tol.
        - iteration_patience_ES: `int`, The number of iterations tolerated before stopping training during which the number of cells that change assignment is less than tol.
        - maxiter: `int`, The maximum number of iterations allowed to train the full model. In practice, the model will halt training long before hitting this limit.
        - epochs_fit: `int`, The number of epochs during which to fine-tune weights, before updating the target distribution.
        - optimizer: `tensorflow.python.keras.optimizer_v2`, An instance of a TensorFlow optimizer.
        - printperiter: `int`, Optional integer argument. If specified, denoised values will be returned every printperiter epochs, so that the user can evaluate the progress of denoising as training continues.
        - denoise: `bool`, If True, then denoised expression values are provided for all cells.
        
        Returns:
        ------------------------------------------------------------------
        - adata: `anndata.AnnData`, The updated annotated data matrix of shape (n_obs, n_vars). Rows correspond to cells and columns to genes. Depending on the arguments of the train call, some outputs will be added to adata.
        """
        
        total_start = time()
        seedlist = list(1000*np.random.randn(int(maxiter)))
        seedlist = [abs(int(x)) for x in seedlist]
        
        self.optimizer = optimizer
        self.optimizer.lr = lr
        
        # Begin deep clustering
        y_pred_last = np.ones((adata.shape[0],), dtype = int) * -1.

        min_delta = np.inf
        current_aeloss_val = np.inf
        delta_patience_ES = 0
        delta_patience_LR = 0
        delta_stop = False
        
        dataset = self.make_generators(adata, val_split = 0.1, batch_size = batch_size)
        
        self.make_outputs(adata, batch_size, denoise = printperiter is not None)
        
        for ite in range(int(maxiter)):
            
            p = self.target_distribution(adata.obsm['cluster memberships'])
            
            dataset.update_p(p)

            best_loss = np.inf
            iter_start = time()
                        
            for epoch in range(epochs_fit):
                current_loss_train = self.train_loop(dataset)
                current_loss_val, current_aeloss_val = self.validation_loop(dataset)
            
            self.make_outputs(adata, batch_size, denoise = printperiter is not None)
            
            y_pred = np.argmax(adata.obsm['cluster memberships'], axis = 1)
                        
            if printperiter is not None:
                if ite % printperiter == 0 and ite > 0:
                    denoising_filename = os.path.join(CarDEC_CITE.weights_dir, '/intermediate_denoising/denoised' + ite)
                    outfile = open(denoising_filename,'wb')
                    pickle.dump(adata.layers["denoised"][:, (adata.var['Variance Type'] == 'HVG') | (adata.var['Variance Type'] == 'HVP')], outfile)
                    outfile.close()
                    
                    if self.LVGP_dims is not None:
                        denoising_filename = os.path.join(CarDEC_CITE.weights_dir, '/intermediate_denoising/denoisedLVGP' + ite)
                        outfile = open(denoising_filename,'wb')
                        pickle.dump(adata.layers["denoised"][:, (adata.var['Variance Type'] == 'LVG') | (adata.var['Variance Type'] == 'LVP')], outfile)
                        outfile.close()
            
            # check stop criterion
            delta_label = np.sum(y_pred != y_pred_last).astype(np.float32) / y_pred.shape[0]
            y_pred_last = deepcopy(y_pred)
            
            current_aeloss_val = current_aeloss_val.numpy()
            current_clustloss_val = (current_loss_val.numpy() - (1 - self.clust_weight) * current_aeloss_val)/self.clust_weight
            print("Iter {:03d} Loss: [Training: {:.3f}, Validation Cluster: {:.3f}, Validation AE: {:.3f}], Label Change: {:.3f}, Time: {:.1f} s".format(ite, current_loss_train.numpy(), current_clustloss_val, current_aeloss_val, delta_label, time() - iter_start))
            
            if current_aeloss_val + 10**(-3) < min_delta:
                min_delta = current_aeloss_val
                delta_patience_ES = 0
                delta_patience_LR = 0
                
            if delta_patience_ES >= iteration_patience_ES:
                delta_stop = True
                
            if delta_patience_LR >= iteration_patience_LR:
                self.optimizer.lr = self.optimizer.lr * decay_factor
                delta_patience_LR = 0
                print("\nDecaying Learning Rate to: " + str(self.optimizer.lr.numpy()))

            delta_patience_ES = delta_patience_ES + 1
            delta_patience_LR = delta_patience_LR + 1
            
            if delta_stop and delta_label < self.tol:
                print('\nAutoencoder_loss ', current_aeloss_val, 'not improving.')
                print('Proportion of Labels Changed: ', delta_label, ' is less than tolerance of ', self.tol)
                print('\nReached tolerance threshold. Stop training.')
                break
                
                        
        y0 = pd.Series(y_pred, dtype='category')
        y0.cat.categories = range(0, len(y0.cat.categories))
        print("\nThe final cluster assignments are:")
        x = y0.value_counts()
        print(x.sort_index(ascending=True))
        
        adata.obsm['embedding'] = self.embed(adata, batch_size)
        if self.LVGP_dims is not None:
            adata.obsm['LVGP embedding'] = self.embed_LVGP(adata, batch_size)
            
        del adata.layers['normalized input']
        
        if denoise:
            self.make_outputs(adata, batch_size, denoise = True)
        
        self.save_weights("./" + self.weights_dir + "/tuned_CarDEC_CITEweights", save_format='tf')
                   
        print("\nTotal Runtime is " + str(time() - total_start))
                
        print("\nThe CarDEC_CITE model is now making inference on the data matrix.")
        
        self.package_output(adata, self.init_pred, self.preclust_denoised, self.preclust_emb)
            
        print("Inference completed, results added.")
        
        return adata
    
    def reload_model(self, adata = None, batch_size = 64, denoise = True):
        """ This class method can be used to load the model's saved weights and redo inference.
        
        
        Arguments:
        ------------------------------------------------------------------
        - adata: `anndata.AnnData`, (Optional) The annotated data matrix of shape (n_obs, n_vars). Rows correspond to cells and columns to genes. If left as None, model weights will be reloaded but inference will not be made.
        - batch_size: `int`, The batch size for filling the array of low dimension embeddings.
        - denoise: `bool`, Whether to provide denoised expression values for all cells.
        
        Returns:
        ------------------------------------------------------------------
        - adata: `anndata.AnnData`, (Optional) The annotated data matrix of shape (n_obs, n_vars). If an adata object was provided as input, the adata object will be returned with inference outputs added.
        """
        
        if os.path.isfile("./" + self.weights_dir + "/tuned_CarDEC_CITEweights.index"):
            print("Weight index file detected, loading weights.")
            self.load_weights("./" + self.weights_dir + "/tuned_CarDEC_CITEweights").expect_partial()
            print("CarDEC_CITE Model weights loaded successfully.")
        
            if adata is not None:
                print("\nThe CarDEC_CITE model is now making inference on the data matrix.")
                
                adata.obsm['embedding'] = self.embed(adata, batch_size)
                if self.LVGP_dims is not None:
                    adata.obsm['LVGP embedding'] = self.embed_LVGP(adata, batch_size)
                    
                del adata.layers['normalized input']
                
                if denoise:
                    self.make_outputs(adata, batch_size, True)
                
                self.package_output(adata, self.init_pred, self.preclust_denoised, self.preclust_emb)
                
                print("Inference completed, results returned.")
                
                return adata

        else:
            print("\nWeight index file not detected, please call CarDEC_CITE_Model.train to learn the weights\n")

