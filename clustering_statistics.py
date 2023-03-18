

import numpy as np

from network import Network, NetworkGrowthAnalysis
import matplotlib as plt

def get_clustering(growth_type, iterations):
    n = Network(growth_type) 
    n.grow(iterations)
    n.calculate_clustering_coefficient()
    return n.C


tests = 1000
C1=np.zeros(tests) 
C2=np.zeros(tests) 
C3=np.zeros(tests) 
C4=np.zeros(tests)
for i in range(tests):
    
    
    C1[i] = get_clustering("random", 97)
    C2[i] = get_clustering("preferential", 97)
    C3[i] = get_clustering("modified preferential", 97)
    C4[i] = get_clustering("random modified", 97)
    
print(np.mean(C1))
print(np.mean(C2))   
print(np.mean(C3))
print(np.mean(C4))

#with plt.style.context(('auplot2')):
plt.hist(C1, bins = 20, label='Random attachment (Problem 1)')
plt.hist(C2, bins = 20, label='BA Scale-Free (Problem 2)')
plt.hist(C3, bins = 20, label='BA Scale-Free (Problem 3)')
plt.hist(C4, bins = 20, label='Random Link attachment (Problem 4)')
plt.title("Histogram of Clustering Coefficients")
plt.xlabel('Clustering Coefficient, C')
plt.ylabel('Bin size')
#plt.ylim(0, 1)
plt.xlim(0, 1)
plt.legend()
plt.show()
