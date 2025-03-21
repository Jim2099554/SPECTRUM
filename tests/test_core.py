import sys
from pathlib import Path

# Add project root to Python path
sys.path.append(str(Path(__file__).parent.parent))

from core.analysis.network_visualizer import NetworkVisualizer

def test_network():
    print("Starting Spectrum Network Visualization Test...")
    
    # Initialize network visualizer
    network_viz = NetworkVisualizer()
    
    # Add test interactions
    print("\n1. Adding test interactions...")
    network_viz.add_interaction(
        "Alice", "Bob", "call", 1.0, 
        {"duration": "5:30", "topic": "meeting"}
    )
    network_viz.add_interaction(
        "Bob", "Charlie", "call", 1.0,
        {"duration": "3:45", "topic": "follow-up"}
    )
    network_viz.add_interaction(
        "Charlie", "Alice", "call", 0.5,
        {"duration": "2:15", "topic": "confirmation"}
    )
    
    # Calculate and display metrics
    print("\n2. Network Metrics:")
    metrics = network_viz.get_network_metrics()
    print(f"Network density: {metrics['density']:.2f}")
    print(f"Average clustering: {metrics['avg_clustering']:.2f}")
    
    # Generate visualization
    print("\n3. Generating network visualization...")
    viz_data = network_viz.generate_visualization()
    print("Visualization data generated successfully")
    
    print("\nTest completed successfully!")

if __name__ == "__main__":
    test_network()
