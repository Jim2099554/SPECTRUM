from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import json
from core.analysis.network_visualizer import NetworkVisualizer
from core.analysis.content_analyzer import ContentAnalyzer

app = FastAPI()

# Initialize analyzers
network_viz = NetworkVisualizer()
content_analyzer = ContentAnalyzer()

class Conversation(BaseModel):
    speaker1: str
    speaker2: str
    content: str

@app.post("/analyze_call")
async def analyze_call(conv: Conversation):
    # Analyze content for risks
    analysis = content_analyzer.analyze_conversation(conv.content)
    
    # Add interaction to network with risk level as weight
    risk_weight = analysis['risk_level'] / 100.0  # Normalize to 0-1
    network_viz.add_interaction(
        conv.speaker1, 
        conv.speaker2, 
        "call", 
        risk_weight,
        {
            "risk_level": analysis['risk_level'],
            "risk_factors": analysis['risk_factors'],
            "sentiment": analysis['sentiment']
        }
    )
    
    return JSONResponse({
        "analysis": analysis,
        "network_metrics": network_viz.get_network_metrics()
    })

@app.get("/", response_class=HTMLResponse)
async def root():
    # Get visualization data
    viz_data = network_viz.generate_visualization()
    
    # Create HTML with embedded Plotly and form
    html_content = f"""
    <html>
        <head>
            <title>Call Analysis Dashboard</title>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .container {{ display: flex; gap: 20px; }}
                .form-container {{ flex: 1; }}
                .viz-container {{ flex: 2; }}
                .result-container {{ margin-top: 20px; }}
            </style>
        </head>
        <body>
            <h1>Call Analysis Dashboard</h1>
            <div class="container">
                <div class="form-container">
                    <h2>Analyze Call</h2>
                    <form id="callForm" onsubmit="analyzeCall(event)">
                        <p>
                            <label for="speaker1">Speaker 1:</label><br>
                            <input type="text" id="speaker1" required>
                        </p>
                        <p>
                            <label for="speaker2">Speaker 2:</label><br>
                            <input type="text" id="speaker2" required>
                        </p>
                        <p>
                            <label for="content">Conversation:</label><br>
                            <textarea id="content" rows="5" required></textarea>
                        </p>
                        <button type="submit">Analyze</button>
                    </form>
                    <div id="result" class="result-container"></div>
                </div>
                <div class="viz-container">
                    <h2>Network Visualization</h2>
                    <div id="graph"></div>
                </div>
            </div>
            
            <script>
                // Initial visualization
                var vizData = {json.dumps(viz_data)};
                Plotly.newPlot('graph', vizData.data, vizData.layout);
                
                async function analyzeCall(event) {{
                    event.preventDefault();
                    
                    const response = await fetch('/analyze_call', {{
                        method: 'POST',
                        headers: {{'Content-Type': 'application/json'}},
                        body: JSON.stringify({{
                            speaker1: document.getElementById('speaker1').value,
                            speaker2: document.getElementById('speaker2').value,
                            content: document.getElementById('content').value
                        }})
                    }});
                    
                    const data = await response.json();
                    
                    // Update result display
                    const result = document.getElementById('result');
                    result.innerHTML = `
                        <h3>Analysis Results:</h3>
                        <p>Risk Level: <strong>${data.analysis.risk_level}%</strong></p>
                        <p>Risk Factors: ${data.analysis.risk_factors.join(', ')}</p>
                        <p>Sentiment: ${data.analysis.sentiment.label} 
                           (${Math.round(data.analysis.sentiment.score * 100)}%)</p>
                    `;
                    
                    // Refresh visualization
                    location.reload();
                }}
            </script>
        </body>
    </html>
    """
    return html_content
