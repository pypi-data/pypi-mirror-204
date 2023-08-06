from tensorflow import convert_to_tensor as tensor
from numpy import setdiff1d
from numpy.random import choice, seed

class batch_sampler(object):
    def __init__(self, array, val_frac, batch_size, splitseed):
        seed(splitseed)
        self.val_indices = choice(range(len(array)), round(val_frac * len(array)), False)
        self.train_indices = setdiff1d(range(len(array)), self.val_indices)
        self.batch_size = batch_size
        
    def __iter__(self):
        batch = []
        
        if self.val:
            for idx in self.val_indices:
                batch.append(idx)
                
                if len(batch) == self.batch_size:
                    yield batch
                    batch = []
                    
        else:
            train_idx = choice(self.train_indices, len(self.train_indices), False)
            
            for idx in train_idx:
                batch.append(idx)
                
                if len(batch) == self.batch_size:
                    yield batch
                    batch = []
                    
        if batch:
            yield batch
            
    def __call__(self, val):
        self.val = val
        return self
            
class simpleloader(object):
    def __init__(self, array, batch_size):
        self.array = array
        self.batch_size = batch_size
        
    def __iter__(self):
        batch = []
        
        for idx in range(len(self.array)):
            batch.append(idx)
            
            if len(batch) == self.batch_size:
                yield tensor(self.array[batch].copy())
                batch = []
                
        if batch:
            yield self.array[batch].copy()
            
class tupleloader(object):
    def __init__(self, *arrays, batch_size):
        self.arrays = arrays
        self.batch_size = batch_size
        
    def __iter__(self):
        batch = []
        
        for idx in range(len(self.arrays[0])):
            batch.append(idx)
            
            if len(batch) == self.batch_size:
                yield [tensor(arr[batch].copy()) for arr in self.arrays]
                batch = []
                
        if batch:
            yield [tensor(arr[batch].copy()) for arr in self.arrays]
            
class aeloader(object):
    def __init__(self, *arrays, val_frac, batch_size, splitseed):
        self.arrays = arrays
        self.batch_size = batch_size
        self.sampler = batch_sampler(arrays[0], val_frac, batch_size, splitseed)
        
    def __iter__(self):
        for idxs in self.sampler(self.val):
            yield [tensor(arr[idxs].copy()) for arr in self.arrays]
            
    def __call__(self, val):
        self.val = val
        return self
            
class countloader(object):
    def __init__(self, embedding, target, sizefactor, val_frac, batch_size, splitseed):
        self.sampler = batch_sampler(embedding, val_frac, batch_size, splitseed)
        self.embedding = embedding
        self.target = target
        self.sizefactor = sizefactor
        
    def __iter__(self):
        for idxs in self.sampler(self.val):
            yield (tensor(self.embedding[idxs].copy()), tensor(self.sizefactor[idxs].copy())), tensor(self.target[idxs].copy())
            
    def __call__(self, val):
        self.val = val
        return self
            
class dataloader(object):
    def __init__(self, hvgp_input, hvgp_target, lvgp_input = None, lvgp_target = None, val_frac = 0.1, batch_size = 128, splitseed = 0):
        self.sampler = batch_sampler(hvgp_input, val_frac, batch_size, splitseed)
        self.hvgp_input = hvgp_input
        self.hvgp_target = hvgp_target
        self.lvgp_input = lvgp_input
        self.lvgp_target = lvgp_target
        
    def __iter__(self):
        for idxs in self.sampler(self.val):
            hvgp_input = tensor(self.hvgp_input[idxs].copy())
            hvgp_target = tensor(self.hvgp_target[idxs].copy())
            p_target = tensor(self.p_target[idxs].copy())
            
            if (self.lvgp_input is not None) and (self.lvgp_target is not None):
                lvgp_input = tensor(self.lvgp_input[idxs].copy())
                lvgp_target = tensor(self.lvgp_target[idxs].copy())
            else:
                lvgp_input = None
                lvgp_target = None
                
            yield [hvgp_input, lvgp_input], hvgp_target, lvgp_target, p_target
            
    def __call__(self, val):
        self.val = val
        return self
    
    def update_p(self, new_p_target):
        self.p_target = new_p_target