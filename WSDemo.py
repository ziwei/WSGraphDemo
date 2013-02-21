import cherrypy

try:
    import matplotlib.pyplot as plt
except:
    raise

import networkx as nx

class Find_Cycles:
    
    def index(self):
        # Let's link to another method here.
	
        return '''Show <a href="showgraph">Graph</a>!
	Show <a href="cycledetection">Cycles</a>
	'''
    index.exposed = True
    def cycledetection(self):
	G = nx.read_graphml("input.graphml")
	cycles = nx.simple_cycles(G)
	cyclelist = []
	#print(cycles)
	for cycle in cycles:
	   cyclelist.append("[" + ", ".join(cycle) + "] ")
	return "".join(cyclelist) + '(<a href="./">back</a>)'
    
    cycledetection.exposed = True
    def showgraph(self):
	G = nx.read_graphml("input.graphml")
	potential=[(u,v) for (u,v,d) in G.edges(data=True) if d['Connection'] == "Potential"]
	triggered=[(u,v) for (u,v,d) in G.edges(data=True) if d['Connection'] == "Triggered"]
	pos=nx.spring_layout(G) # positions for all nodes
	# nodes
	nx.draw_networkx_nodes(G,pos,node_size=700)
	# edges
	nx.draw_networkx_edges(G,pos,edgelist=triggered,
                    width=3)
	nx.draw_networkx_edges(G,pos,edgelist=potential,
                    width=3,alpha=0.5,edge_color='b',style='dashed')
	# labels
	nx.draw_networkx_labels(G,pos,font_size=20,font_family='sans-serif')

	plt.axis('off')
	plt.savefig("weighted_graph.png") # save as png
	plt.show() # display
	return '(<a href="./">back</a>)'
    showgraph.exposed = True

import os.path
tutconf = os.path.join(os.path.dirname(__file__), 'tutorial.conf')

if __name__ == '__main__':
    # CherryPy always starts with app.root when trying to map request URIs
    # to objects, so we need to mount a request handler root. A request
    # to '/' will be mapped to HelloWorld().index().
    cherrypy.quickstart(Find_Cycles(), config=tutconf)
else:
    # This branch is for the test suite; you can ignore it.
    cherrypy.tree.mount(Find_Cycles(), config=tutconf)
