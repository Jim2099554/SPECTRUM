import networkx as nx
import plotly.graph_objects as go
from typing import Dict, Any

class NetworkVisualizer:
    def __init__(self):
        """Initialize the network visualization system"""
        self.graph = nx.Graph()
        
    def add_interaction(self, speaker1: str, speaker2: str, 
                       interaction_type: str, weight: float = 1.0,
                       metadata: Dict[str, Any] = None):
        """Add an interaction between two speakers to the network"""
        if not self.graph.has_edge(speaker1, speaker2):
            self.graph.add_edge(speaker1, speaker2, 
                              weight=weight,
                              interactions=[])
        
        edge_data = self.graph[speaker1][speaker2]
        edge_data["weight"] += weight
        edge_data["interactions"].append({
            "type": interaction_type,
            "metadata": metadata or {}
        })
    
    def get_network_metrics(self) -> Dict[str, Any]:
        """Calculate various network metrics"""
        metrics = {
            "density": nx.density(self.graph),
            "avg_clustering": nx.average_clustering(self.graph)
        }
        
        # Only calculate centrality metrics if we have nodes
        if self.graph.number_of_nodes() > 0:
            metrics["centrality"] = {
                "degree": nx.degree_centrality(self.graph)
            }
            if self.graph.number_of_nodes() > 1:
                metrics["centrality"].update({
                    "betweenness": nx.betweenness_centrality(self.graph)
                })
        
        return metrics
    
    def generate_visualization(self) -> Dict[str, Any]:
        """Generate an interactive network visualization"""
        if self.graph.number_of_nodes() == 0:
            return {}
            
        # Calculate layout
        pos = nx.spring_layout(self.graph)
        
        # Create edge trace
        edge_x = []
        edge_y = []
        for edge in self.graph.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
            
        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=1, color='#888'),
            hoverinfo='none',
            mode='lines')
        
        # Create node trace
        node_x = []
        node_y = []
        node_text = []
        for node in self.graph.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            node_text.append(node)
            
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            hoverinfo='text',
            text=node_text,
            textposition='top center',
            marker=dict(
                size=15,
                color='#1f77b4',
                line=dict(width=1, color='#444')))
        
        # Create figure
        fig = go.Figure(
            data=[edge_trace, node_trace],
            layout=go.Layout(
                title='Communication Network',
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20, l=5, r=5, t=40),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                plot_bgcolor='white'
            )
        )
        
        return fig.to_dict()
