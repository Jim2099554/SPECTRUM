import networkx as nx
import plotly.graph_objects as go
from typing import Dict, Any

class NetworkVisualizer:
    def __init__(self):
        """Initialize the directed network visualization system"""
        self.graph = nx.DiGraph()

    def add_interaction(self, caller: str, receiver: str,
                        interaction_type: str, weight: float = 1.0,
                        metadata: Dict[str, Any] = None,
                        caller_type: str = "other",
                        receiver_type: str = "other"):
        """Add a directed call interaction"""
        if not self.graph.has_node(caller):
            self.graph.add_node(caller, type=caller_type)
        if not self.graph.has_node(receiver):
            self.graph.add_node(receiver, type=receiver_type)

        if not self.graph.has_edge(caller, receiver):
            self.graph.add_edge(caller, receiver, weight=0, interactions=[])

        edge_data = self.graph[caller][receiver]
        edge_data["weight"] += weight
        edge_data["interactions"].append({
            "type": interaction_type,
            "metadata": metadata or {}
        })

    def get_network_metrics(self) -> Dict[str, Any]:
        """Calculate network metrics"""
        metrics = {
            "density": nx.density(self.graph),
            "avg_clustering": nx.average_clustering(self.graph.to_undirected())
        }
        if self.graph.number_of_nodes() > 0:
            metrics["centrality"] = {
                "degree": nx.degree_centrality(self.graph),
                "betweenness": nx.betweenness_centrality(self.graph)
            }
        return metrics

    def generate_visualization(self) -> Dict[str, Any]:
        """Generate interactive visualization with arrows and transcription details"""
        if self.graph.number_of_nodes() == 0:
            return {}

        pos = nx.spring_layout(self.graph, seed=42)

        edge_x = []
        edge_y = []
        edge_text = []
        for u, v in self.graph.edges():
            x0, y0 = pos[u]
            x1, y1 = pos[v]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
            fragments = []
            for interaction in self.graph[u][v]['interactions']:
                fragment = interaction["metadata"].get("transcription", "[No transcription]")
                fragments.append(f"- {fragment[:100]}...")
            edge_text.append(f"{u} → {v}:\n" + "\n".join(fragments))

        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=1, color='#888'),
            hoverinfo='text',
            text=edge_text,
            mode='lines')

        node_x = []
        node_y = []
        node_text = []
        node_color = []

        for node in self.graph.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            node_type = self.graph.nodes[node].get("type", "other")
            color = "#d62728" if node_type == "internal" else "#1f77b4"
            node_color.append(color)
            node_text.append(f"{node} (type: {node_type})\nCalls: {self.graph.degree[node]}")

        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            hoverinfo='text',
            text=node_text,
            textposition='top center',
            marker=dict(size=15, color=node_color, line=dict(width=1, color='#444'))
        )

        fig = go.Figure(
            data=[edge_trace, node_trace],
            layout=go.Layout(
                title='Phone Call Network',
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20, l=5, r=5, t=40),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                plot_bgcolor='white'
            )
        )

        return fig.to_dict()
        