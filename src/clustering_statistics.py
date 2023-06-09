

import numpy as np
import matplotlib.pyplot as plt

import aulibrary as au
from network import Network, NetworkGrowthAnalysis


class ClusteringDistribution:
    def __init__(self, n_tests):
        self.n_tests = n_tests
        self.test_types = ["random", "preferential", 
                      "modified preferential", "random modified"]
        self.test_dict = {}
        
    def get_network_clustering(self, growth_type, iterations):
        n = Network(growth_type) 
        n.grow(iterations)
        n.calculate_clustering_coefficient()
        return n.C
    
    def calculate_n_tests(self):  
        """
        -----------------------------------------------------------------------
        | Method for calculating n number networks and their clustering       |
        | coefficients                                                        |
        -----------------------------------------------------------------------
        """
        for t in self.test_types:
            self.test_dict[t] = {"clustering": np.zeros(self.n_tests),
                                 "C_mean":None}
              
        for t in self.test_types:
            for i in range(self.n_tests):
                self.test_dict[t]["clustering"][i] = self.get_network_clustering(t, 97)
                
            self.test_dict[t]["C_mean"] = np.mean(self.test_dict[t]["clustering"])
         
    def plot_histogram(self):
        """
        -----------------------------------------------------------------------
        | Method for plotting the clustering distribution for n number of     |
        | test                                                                |
        -----------------------------------------------------------------------
        """
        
        fig, ax = plt.subplots(figsize = (6,6)) 
        ax.set_facecolor('#212946')
        fig.set_facecolor('#212946')
          
        plt.hist(self.test_dict["random"]["clustering"], bins = 20, 
                 label='Random attachment',
                 color=au.AUpink, alpha=0.5)
        plt.hist(self.test_dict["preferential"]["clustering"], bins = 20, 
                 label='BA Scale-Free (Preferential)',
                 color=au.AUgreen, alpha=0.5)
        plt.hist(self.test_dict["modified preferential"]["clustering"], bins = 20, 
                 label='BA Scale-Free (Modified Preferential)',
                 color=au.AUyellow, alpha=0.5)
        plt.hist(self.test_dict["random modified"]["clustering"], bins = 20, 
                 label='Random Modified',
                 color=au.AUblue2, alpha=0.5)
        
        plt.title("Histogram of Clustering Coefficients",
        #          fontproperties= au.AUb, 
                  fontsize=13, color=au.AUlightblue)
        plt.xlabel('Clustering Coefficient, C')
        plt.ylabel('Bin size')
        plt.xlim(0, 1)
        plt.legend()
        
        ax.spines['bottom'].set_color(au.AUblue3)
        ax.spines['top'].set_color(au.AUblue3)
        ax.spines['left'].set_color(au.AUblue3)
        ax.spines['right'].set_color(au.AUblue3)
        ax.xaxis.label.set_color(au.AUblue3)
        ax.yaxis.label.set_color(au.AUblue3)
        ax.tick_params(axis='x', colors=au.AUblue3)
        ax.tick_params(axis='y', colors=au.AUblue3)
        ax.grid(which='major', color=au.AUbluegrey, linestyle='-', linewidth=0.7, alpha=0.5)
        ax.grid(which='minor', color=au.AUbluegrey, linestyle='-.', linewidth=0.7, alpha=0.6)

        plt.show()


