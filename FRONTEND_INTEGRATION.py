"""
Frontend Integration Guide for NILM Predictions

This file demonstrates how the frontend can interact with the backend API
to get predictions from the pickle model.
"""

import json

# ============================================================================
# EXAMPLE 1: How Frontend Sends Data to Backend
# ============================================================================

def frontend_example_single_prediction():
    """
    Example: Frontend sends power data to backend API
    
    In your frontend (JavaScript/TypeScript):
    
    ```javascript
    // Send power data to backend for prediction
    async function getPrediction(powerData) {
        const response = await fetch('http://localhost:8000/api/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                voltage: 230.5,
                current: 4.78,
                active_power: 1100,
                reactive_power: 0,
                apparent_power: 1100,
                power_factor: 1.0
            })
        });
        
        const result = await response.json();
        return result;
    }
    
    // Use the prediction
    const prediction = await getPrediction({
        voltage: 230.5,
        current: 4.78,
        active_power: 1100,
        reactive_power: 0,
        apparent_power: 1100,
        power_factor: 1.0
    });
    
    console.log('Devices:', prediction.device_states);
    // Output: { bulb: false, fan: false, iron: true }
    ```
    """
    
    # Python equivalent (for testing)
    request_data = {
        "voltage": 230.5,
        "current": 4.78,
        "active_power": 1100,
        "reactive_power": 0,
        "apparent_power": 1100,
        "power_factor": 1.0
    }
    
    print("=" * 70)
    print("FRONTEND REQUEST TO BACKEND API")
    print("=" * 70)
    print(f"\nPOST http://localhost:8000/api/predict")
    print(f"\nBody:")
    print(json.dumps(request_data, indent=2))
    
    # Expected response
    expected_response = {
        "label": 4,
        "device_states": {
            "bulb": False,
            "fan": False,
            "iron": True
        },
        "probabilities": [
            {
                "label": 4,
                "probability": 0.95,
                "device_states": {"bulb": False, "fan": False, "iron": True}
            }
        ],
        "confidence": 0.95
    }
    
    print(f"\nExpected Response:")
    print(json.dumps(expected_response, indent=2))


# ============================================================================
# EXAMPLE 2: Real-time Updates (WebSocket)
# ============================================================================

def frontend_example_websocket():
    """
    Example: Frontend receives real-time predictions via WebSocket
    
    In your frontend (JavaScript/TypeScript):
    
    ```javascript
    // Connect to WebSocket for real-time predictions
    const ws = new WebSocket('ws://localhost:8000/ws');
    
    ws.onmessage = (event) => {
        const prediction = JSON.parse(event.data);
        
        // Update UI with device states
        updateDeviceUI({
            bulb: prediction.device_states.bulb,
            fan: prediction.device_states.fan,
            iron: prediction.device_states.iron
        });
        
        // Update power display
        updatePowerDisplay(prediction.power);
    };
    
    ws.onerror = (error) => {
        console.error('WebSocket error:', error);
    };
    ```
    """
    
    print("\n" + "=" * 70)
    print("FRONTEND WEBSOCKET CONNECTION")
    print("=" * 70)
    print(f"\nConnect: ws://localhost:8000/ws")
    print(f"\nReceived Message Example:")
    
    websocket_message = {
        "timestamp": "2025-12-11T10:30:45Z",
        "voltage": 230.5,
        "current": 4.78,
        "active_power": 1100,
        "reactive_power": 0,
        "apparent_power": 1100,
        "power_factor": 1.0,
        "device_states": {
            "bulb": False,
            "fan": False,
            "iron": True
        },
        "label": 4,
        "confidence": 0.95
    }
    
    print(json.dumps(websocket_message, indent=2))


# ============================================================================
# EXAMPLE 3: React Component Example
# ============================================================================

def frontend_react_component_example():
    """
    Example React component that uses the prediction API
    
    ```typescript
    import React, { useState, useEffect } from 'react';
    
    interface DeviceStates {
        bulb: boolean;
        fan: boolean;
        iron: boolean;
    }
    
    interface Prediction {
        label: number;
        device_states: DeviceStates;
        confidence: number;
    }
    
    const DeviceMonitor: React.FC = () => {
        const [prediction, setPrediction] = useState<Prediction | null>(null);
        const [isLoading, setIsLoading] = useState(false);
        
        useEffect(() => {
            // Connect to WebSocket for real-time updates
            const ws = new WebSocket('ws://localhost:8000/ws');
            
            ws.onmessage = (event) => {
                const data = JSON.parse(event.data);
                setPrediction(data);
            };
            
            return () => ws.close();
        }, []);
        
        const getPrediction = async (powerData: any) => {
            setIsLoading(true);
            try {
                const response = await fetch('http://localhost:8000/api/predict', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(powerData)
                });
                const result = await response.json();
                setPrediction(result);
            } catch (error) {
                console.error('Prediction error:', error);
            } finally {
                setIsLoading(false);
            }
        };
        
        return (
            <div className="device-monitor">
                <h2>Device Status</h2>
                {prediction && (
                    <div className="devices">
                        <DeviceCard 
                            name="Bulb" 
                            isOn={prediction.device_states.bulb}
                        />
                        <DeviceCard 
                            name="Fan" 
                            isOn={prediction.device_states.fan}
                        />
                        <DeviceCard 
                            name="Iron" 
                            isOn={prediction.device_states.iron}
                        />
                    </div>
                )}
                <div className="confidence">
                    Confidence: {(prediction?.confidence * 100).toFixed(1)}%
                </div>
            </div>
        );
    };
    ```
    """
    
    print("\n" + "=" * 70)
    print("REACT COMPONENT EXAMPLE")
    print("=" * 70)
    print("\nSee the TypeScript code above for a complete React component example")
    print("that uses the NILM prediction API.")


# ============================================================================
# EXAMPLE 4: API Endpoints Available
# ============================================================================

def show_api_endpoints():
    """Show all available API endpoints"""
    
    print("\n" + "=" * 70)
    print("AVAILABLE API ENDPOINTS")
    print("=" * 70)
    
    endpoints = [
        {
            "method": "POST",
            "path": "/api/predict",
            "description": "Get prediction for single power measurement",
            "body": {
                "voltage": 230.5,
                "current": 4.78,
                "active_power": 1100,
                "reactive_power": 0,
                "apparent_power": 1100,
                "power_factor": 1.0
            }
        },
        {
            "method": "GET",
            "path": "/api/status",
            "description": "Get backend service status",
            "body": None
        },
        {
            "method": "GET",
            "path": "/api/latest",
            "description": "Get latest predictions from live data",
            "body": None
        },
        {
            "method": "WebSocket",
            "path": "/ws",
            "description": "Real-time prediction stream",
            "body": None
        }
    ]
    
    for endpoint in endpoints:
        print(f"\n{endpoint['method']} {endpoint['path']}")
        print(f"  {endpoint['description']}")
        if endpoint['body']:
            print(f"  Body: {json.dumps(endpoint['body'])}")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("\n" + " NILM Frontend Integration Guide ".center(70, "="))
    
    frontend_example_single_prediction()
    frontend_example_websocket()
    frontend_react_component_example()
    show_api_endpoints()
    
    print("\n" + "=" * 70)
    print("📚 QUICK START:")
    print("=" * 70)
    print("""
1. Train and save the model:
   - Open NILM_RF.ipynb
   - Run all cells including the 'Save Model as Pickle File' cell
   
2. Start the backend:
   python run_backend.py
   
3. Test predictions:
   python test_predictions.py
   
4. In your frontend, connect to:
   - HTTP API: http://localhost:8000/api/predict
   - WebSocket: ws://localhost:8000/ws
   
5. Send power data and receive device predictions!
    """)
    print("=" * 70)
