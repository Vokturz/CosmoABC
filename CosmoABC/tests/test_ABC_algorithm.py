#!/usr/bin/env python

import unittest 
import os
import numpy as np

from statsmodels.stats.weightstats import DescrStatsW

from CosmoABC.distances import distance_quantiles, summ_quantiles
from CosmoABC.priors import flat_prior
from CosmoABC.ABC_sampler import ABC
from CosmoABC.ABC_functions import SelectParamInnerLoop, SetDistanceFromSimulation, DrawAllParams, get_cores
from CosmoABC.plots import plot_1D, plot_2D, plot_3D, plot_4D


def ysim(v):

    l1 = np.random.normal(loc=v['mu'], scale=v['sigma'], size=v['n'])
    
    return np.atleast_2d(l1).T    

class TestABC(unittest.TestCase):

    def setUp(self):

        self.mu = 2.5
        self.sigma = 1.0
        self.n = 1000
        
        self.params = {}
        self.params['simulation_func'] = ysim
        self.params['simulation_params'] = {'mu': self.mu, 'sigma':self.sigma, 'n':self.n} 
        self.params['dataset1'] = self.params['simulation_func']( self.params['simulation_params'] )
        self.params['param_to_fit']=['mu', 'sigma', 'n']							
        self.params['param_lim']=[[0.0, 5.0],[0.001, 3.0],[500, 1500]]	
        self.params['prior_par'] = [[1.0, 4.0],[0.001, 3.0],[600, 1400]]
        self.params['screen'] = 0
        self.params['Mini'] = 200 							
        self.params['M'] = 100				
        self.params['delta'] =0.1				
        self.params['qthreshold'] = 0.75
        self.params['file_root'] = os.getcwd() + '/test_PS'	
        self.params['distance_func'] =  distance_quantiles 
 	self.params['prior_func'] = [ flat_prior, flat_prior, flat_prior ]
        self.params['ncores'] = 1 

        #initiate ABC sampler
        self.sampler_ABC = ABC( self.params ) 

        self.W = [1.0/self.params['M'] for i in xrange( self.params['M'] )]
        self.params = summ_quantiles(self.params['dataset1'], self.params)   	 

      
    def test_DrawAllParams( self ):
         
        #draw parameters
        r1 = DrawAllParams(self.params)

        res = []
        for i1 in xrange(len(r1)):
            if r1[i1] >= self.params['param_lim'][i1][0] and r1[i1] < self.params['param_lim'][i1][1]:
                res.append(True)

            else:
                res.append(False)

        self.assertEqual([True for item in r1], res)

    def test_SetDistanceFromSimulation(self):

        #set distance
        r2 = SetDistanceFromSimulation(self.params)

        self.assertTrue(r2 >= 0)

    def test_plot(self):

        self.params['ncores'] = get_cores()
        self.sampler_ABC.fullABC(build_first_system=True)

        if len(self.params['param_to_fit']) == 1:
            plot_1D(self.sampler_ABC.T, 'results.pdf', self.params)

        elif len(self.params['param_to_fit']) == 2:
            plot_2D(self.sampler_ABC.T, 'results.pdf', self.params) 

        elif len(self.params['param_to_fit']) == 3:
            plot_3D(self.sampler_ABC.T, 'results.pdf', self.params) 

        elif len(self.params['param_to_fit']) == 4:
            plot_4D(self.sampler_ABC.T, 'results.pdf', self.params) 
   

if __name__ == '__main__':

    unittest.main()