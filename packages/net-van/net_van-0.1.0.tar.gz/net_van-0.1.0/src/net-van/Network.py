# -*- coding: utf-8 -*-
"""
Created on Sun Aug 15 12:55:38 2021

@author: vavri
"""
import numpy as np
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os
from glob import glob


class Network(object):
    
    path_ = os.path.join('..','..','training_params')

#activation functions
    
    def ReLU(x, d=False):
            
        return np.where(x<0,0.,(x if d==False else 1)) 
        
        
    def Sigmoid(x, d=False):

        return (1/(1+np.exp(-x))) if d == False\
        else ((1/(1+np.exp(-x)))*(1-(1/(1+np.exp(-x)))))
    
    
    def extract_int(string, cut=None):
        
        if cut is None:
            n_str = ''
            for i, char in enumerate(string):
                n_str += char if char.isdigit() == True else ''
            n_str = int(n_str)
            
        else:
            try:
                assert cut == any(['first','last']), "Split needs to be either \"first\" or \"last\""
            except AssertionError:
                raise
            
            if cut == "first":
                n_str = ''
                for i, char in enumerate(string):
                    n_str += char if char.isdigit() == True else ''
                    if char == '_': break
                
            if cut == "last":
                n_str = ''
                for i,char1 in enumerate(string):
                    if char1 == '_':
                        for char2 in string[i:]:
                            n_str += char2 if char2.isdigit() == True else ''
                        break
        return n_str
    
    
    def __init__(self, index=None): #if index is left None, than the latest existing is used
        
        bias_load = []
        weight_load = []
        path_ = np.copy(Network.path_)
        all_files = glob(os.path.join(path_,'*.npy'))

        try:
            assert len(all_files) != 0, "No parameter files available!"
        except AssertionError:
            raise #TODO propper error handling

        last_file = all_files[-1]
        last_index = Network.extract_int(last_file,cut='first')        

        if index is not None: 
            
            try:
                assert index < last_index, "Adressed parameters doesnt exist!"
            except AssertionError:
                raise #TODO propper error handling
            
            p_ind = index
        
        else: p_ind = last_index
        
        w_par_files = glob(os.path.join(path_,f'p{p_ind}_w*.npy'))
        b_par_files = glob(os.path.join(path_,f'p{p_ind}_b*.npy'))
        
        for file in w_par_files:           
            weight_load.append(np.load(file))
            
        for file in b_par_files:
            bias_load.append(np.load(file))
        
        params = [weight_load,bias_load]
        
        N = [len(weight_load[0][:,0])]
        for matrix in weight_load:
            N.append(len(matrix[0,:]))
            
        self.N = N
        
        weight_like = [0]*len(self.N)
        bias_like = [0]*len(self.N)
        
        for l in range(1,len(self.N)):    
            weight_like[l] = np.zeros((self.N[l-1],self.N[l]))  
            bias_like[l] = np.zeros((self.N[l]))
        
        self.weight_like = weight_like
        self.bias_like = bias_like
        self.weights = self.weight_like[:]
        self.bias = self.bias_like[:]
            
        for l,neurons in enumerate(self.N):                
            self.weights[l] = params[0][l]
            self.bias[l] = params[1][l]
    
    
    def clear_dir(self, indices=None):
         
        try:
            if indices is not None:
                
                path_ = np.copy(Network.path_)
                files = []
                
                for n in indices:
                    n = int(n)
                    files_ = glob(os.path.join(path_,f'p{n}*.npy'))
                    files.extend(files_)
                    
                for file in files:
                    os.remove(file)
            
            else:
                files = glob(os.path.join(path_,'p*.npy'))
                for file in files:
                    os.remove(file)
                    
        except (ValueError, IndexError):
            print('Warning: Input indices must correspond with existing parameter files!')
            
    
    def current_index(self):
        
        path_ = np.copy(Network.path_)
        end_file = glob(os.path.join(path_,'p*.npy'))[-1]
        extracted = Network.extract_int(end_file,cut='first')
        return extracted
    
#output method
    
    def get_output(self, inp_, layer=False, label=None):
            
        if layer == True:            
            all_out = []

    #first layer output
                
        p_output = inp_[:]
        
        if layer == True:                    
            all_out.append(p_output[:])
 
    #rest of the layers propagating       
 
        if (layer > 1) or (len(self.N) > 1):
 
            for l in range(1,(len(self.N) if type(layer) == bool else layer)):                
                        
                activation1 = np.sum(np.full(
                    (self.N[l],self.N[l-1]),
                    p_output
                    ).T\
                    *self.weights[l],axis=0)
                p_output = (Network.ReLU(activation1 + self.bias[l]))\
                    if l < (len(self.N)-1) else (Network.Sigmoid(activation1 + self.bias[l]))                      
                        
                if layer == True:                            
                    all_out.append(p_output[:])
    
    #computing cost
        
        if label is not None:
        
            cost = 0                       
            cost = np.sum((label[:] - (
                p_output[:] if layer==False or type(layer)==int else all_out[-1]))**2)                       
            self.cost = cost                     
            
        return p_output if layer==False or type(layer)==int else all_out  
                        

