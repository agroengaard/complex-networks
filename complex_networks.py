 


import time
import numpy as np
import random as rm
import matplotlib.pyplot as plt
import networkx as nx
import aulibrary as au


class Network:
    """
    ===========================================================================
    || Class for creating a complex network by growing it from an initial    ||
    || number of links and nodes                                             ||
    ===========================================================================
    """
    def __init__(self, growth_type="random"):
        
        print("Network initialized")
        
        self.growth_type = growth_type
        self.links = [1, 2, 1, 3, 2, 3]                  # Initial links vector ("Seed")
        self.total_growth = 0                            # Number of total growth iterations this network has experienced
        self.m     = 2                                   # Number of new links pr. new node
        self.N     = 3                                   # Number of inital nodes
        self.L     = 3                                   # Number of initial links
        self.lamb3 = 1                                   # Lambda value (Problem 3)
        
    def grow(self, growth_iterations):
        """
        -----------------------------------------------------------------------
        | Method for growing the network by the growth type chosen            |  
        | in the variable "self.growth_type".                                 |
        -----------------------------------------------------------------------
        | INPUT:                                                              |
        |    growth_iterations (int) : The number of new growth iterations    |
        |                              to apply to the network                |
        |_____________________________________________________________________|
        """
        print("Growing network by {} growth".format(self.growth_type))
        
        self.total_growth += growth_iterations
        
        new = np.empty((self.m*2,), int)                                       # Initializing the New links vector

        for i in range(0, growth_iterations):   
            self.N += 1                                                        # Making a new node
            self.L += self.m                                                   # Total links increases by m  
            Ln = [0]*self.m                                                    # Resetting nodes to be linked every it.      
            while len(Ln) != len(set(Ln)):                                     # Until links not identical 
            
                if self.growth_type == "random":
                    Ln = rm.sample(set(self.links), self.m)                    # (1) - Random
                    
                elif self.growth_type == "preferential":
                    Ln = rm.sample(self.links, self.m)                         # (2)- Preferential  
                    
                elif self.growth_type == "modified preferential":
                    k_n = dict([[x, self.links.count(x)] for x in set(self.links)]) # (3) Counting k for each node                     
                    ki = list(k_n.values())                                    # (3) Getting the values    
                    Pi_n = [(i+self.lamb3)/(sum(ki)+self.lamb3*self.N) for i in ki] # (3)     
                    Ln = rm.choices(list(set(self.links)), Pi_n , k=self.m)    # (3) - Modified Preferential 
                    
                elif self.growth_type == "random modified":
                    rn =  rm.choice(list(enumerate(self.links[::2])))[0]       # (4) - Finding random node  
                    Ln = self.links[(rn*2):(rn*2)+2]                           # (4) - The link from the random node
                    
            new[::2] = self.N                                                  # New node vector
            new[1::2] = Ln                                                     # New links vector
            self.links.extend(new)                                             # Adding new links to links    
        k_n = dict([[x, self.links.count(x)] for x in set(self.links)])        # Counting k for each node                     
        self.ki = list(k_n.values())                                                # Getting the values    

        self.link_pairs = np.reshape(self.links, (self.L, 2))                  # Rearranging the links vector as pairs


    def calculate_numerical_probability_distribution(self):
        
        print("Calculating numerical probability distribution")
        
        start = time.time()
        p = dict([[x, self.ki.count(x)] for x in set(self.ki)])
        p_keys   = list(p.keys())
        N_k = list(p.values())
        self.p_k = np.zeros(len(N_k))
        for i in range(0,len(N_k)):
            self.p_k[i] = N_k[i]/self.N

        end = time.time()
        print("Numerical probability distribution, calculation time:")
        print(end - start)


    def calculate_clustering_coefficient(self):
        
        print("Calculating adjency matrix")
        
        start = time.time()
        adj = np.zeros((self.N, self.N))          # Initializing adjecency matrix

        for i in range(len(self.link_pairs)):   # Creating adjecency matrix
            c1 = self.link_pairs[i,0]
            c2 = self.link_pairs[i,1]
            adj[c1-1,c2-1] = 1
            adj[c2-1,c1-1] = 1

        adj3 = np.dot(np.dot(adj,adj),adj)
        adjs = np.diag(adj3)
         
        print("Calculating clustering coefficient")
        
        C_i = np.zeros(self.N)              # Local clustering coefficient
        for i in range(0, self.N):
            C_i[i] = (adjs[i]/(self.ki[i]*(self.ki[i]-1))) 
        self.C = sum(C_i)/self.N                 # Network average clustering coefficient
               

        end = time.time()
        print("Clustering Coefficient calculation time:")
        print(end - start)
        
      
    def plot_network(self):
        """
        -----------------------------------------------------------------------
        | Method for plotting the network. Node size scales with the number   |
        | of links a node has                                                 |
        -----------------------------------------------------------------------
        """
        
        msize = (np.array(self.ki)*50)              # Creating markersize vector 

        Nodes = np.linspace(1, self.N, self.N, dtype = int)

        G = nx.Graph()
        G.add_nodes_from(Nodes)
        G.add_edges_from(self.link_pairs)
      
        fig = plt.figure(figsize=(9, 9), facecolor='#212946')
        ax = fig.add_subplot(111)
        ax.set_facecolor('#212946')
          
      
 
    #    fig.patch.set_facecolor('black')
    #    ax.set_facecolor(au.AUblue)
        pos = nx.spring_layout(G, iterations=200)
        options = {
            "node_color": range(self.N),
            "with_labels": True,
           # "line_color": "grey",
            "width": 0.2,
            "node_size": msize,
            "cmap": au.AUBlueBlue_r,
            "font_family": "AU Passata",
            "font_color": "black",
            "font_weight": "bold"
        }
        nx.draw(G, pos, **options,alpha=0.7)
        textstr = '\n'.join((
               r'$\mathrm{N}=%.0f$' % (self.N, ),
               r'$\mathrm{C}=%.2f$' % (self.C, ),
        #      r'$\mathrm{D}=%.2f$' % (D, )
        ))
        props = dict(boxstyle='round', facecolor=au.AUlightblue, edgecolor = au.AUblues, alpha=0.6)
        ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14, verticalalignment='top', bbox=props)
        plt.title("Network visualization", fontproperties= au.AUb, fontsize=18, color=au.AUblue)
        plt.suptitle(self.growth_type + " Network", fontproperties= au.AUb, y=0.92, fontsize=14, color=au.AUlightblue)
        fig.tight_layout()



if __name__ == "__main__":
    
    n = Network("random")
    n.grow(97)
    n.calculate_numerical_probability_distribution()
    n.calculate_clustering_coefficient()
    n.plot_network()
    
    
 
    n2 = Network("preferential")
    n2.grow(97)
    n2.calculate_numerical_probability_distribution()
    n2.calculate_clustering_coefficient()
    n2.plot_network()  
      
      
        
        
        
        
        
        
        
        
        
        
        