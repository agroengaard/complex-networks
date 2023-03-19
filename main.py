 






from network import NetworkGrowthAnalysis
from clustering_statistics import ClusteringDistribution


if __name__ == "__main__":
    
    NetworkGrowthAnalysis("random", 97)
    NetworkGrowthAnalysis("preferential", 97)
    NetworkGrowthAnalysis("modified preferential", 97)
    NetworkGrowthAnalysis("random modified", 97)
    
    cd = ClusteringDistribution(10)  
    cd.calculate_n_tests()  
    cd.plot_histogram()  
    