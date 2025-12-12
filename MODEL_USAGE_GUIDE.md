# NILM Model - Pickle File Usage Guide

## 📦 What is the Pickle File?

The pickle file (`nilm_rf_model.pkl`) is a saved Random Forest model that can predict which electrical devices are turned ON/OFF based on power consumption data.

### Model Contents:
- **Trained Random Forest Classifier**: The machine learning model
- **Feature Columns**: The input features needed for predictions
- **Class Labels**: The possible prediction outcomes (0-7)
- **Random State**: For reproducibility

## 🎯 How It Works

```
Power Data → Pickle Model → Device States
(voltage, current, power) → [Model] → (bulb: ON/OFF, fan: ON/OFF, iron: ON/OFF)
```

## 🚀 Quick Start

### Step 1: Create the Pickle File

Open `NILM_RF.ipynb` and run all cells, including the new "Save Model as Pickle File" cell. This will create:
```
backend/artifacts/nilm_rf_model.pkl
```

### Step 2: Use in Backend

The backend automatically loads the pickle file and uses it for predictions:

```python
# backend/predictor.py handles loading and predictions
from backend.predictor import NILMPredictor

# Initialize predictor
predictor = NILMPredictor()

# Make prediction
result = predictor.predict_single({
    'voltage': 230,
    'current': 4.78,
    'active_power': 1100,
    'reactive_power': 0,
    'apparent_power': 1100,
    'power_factor': 1.0
})

print(result['device_states'])
# Output: {'bulb': False, 'fan': False, 'iron': True}
```

### Step 3: Use in Frontend

The frontend connects to the backend API to get predictions:

```javascript
// Send power data to backend
const response = await fetch('http://localhost:8000/api/predict', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        voltage: 230,
        current: 4.78,
        active_power: 1100,
        reactive_power: 0,
        apparent_power: 1100,
        power_factor: 1.0
    })
});

const prediction = await response.json();
console.log(prediction.device_states);
// Output: { bulb: false, fan: false, iron: true }
```

## 📊 Input Format

The model expects 6 power metrics as input:

| Field            | Type  | Description                | Example |
|------------------|-------|----------------------------|---------|
| voltage          | float | Voltage in Volts           | 230.5   |
| current          | float | Current in Amperes         | 4.78    |
| active_power     | float | Active Power in Watts      | 1100    |
| reactive_power   | float | Reactive Power in VAR      | 0       |
| apparent_power   | float | Apparent Power in VA       | 1100    |
| power_factor     | float | Power Factor (0-1)         | 1.0     |

## 📤 Output Format

The model returns predictions with device states:

```json
{
  "label": 4,
  "device_states": {
    "bulb": false,
    "fan": false,
    "iron": true
  },
  "probabilities": [
    {
      "label": 4,
      "probability": 0.95,
      "device_states": {"bulb": false, "fan": false, "iron": true}
    }
  ],
  "confidence": 0.95
}
```

## 🔢 Label Meanings

| Label | Bulb | Fan | Iron | Typical Power |
|-------|------|-----|------|---------------|
| 0     | OFF  | OFF | OFF  | 0W            |
| 1     | ON   | OFF | OFF  | 60W           |
| 2     | OFF  | ON  | OFF  | 80W           |
| 3     | ON   | ON  | OFF  | 140W          |
| 4     | OFF  | OFF | ON   | 1100W         |
| 5     | ON   | OFF | ON   | 1160W         |
| 6     | OFF  | ON  | ON   | 1180W         |
| 7     | ON   | ON  | ON   | 1240W         |

## 🧪 Testing the Model

### Test File Usage:

```bash
# Run comprehensive tests
python test_predictions.py
```

This will test:
1. Single predictions
2. Batch predictions
3. DataFrame predictions
4. API format predictions

## 🔌 Backend Integration

### File Structure:
```
backend/
├── artifacts/
│   └── nilm_rf_model.pkl      # The trained model
├── predictor.py                # Prediction logic
├── service.py                  # API service (updated)
└── train_model.py              # Training script
```

### Starting the Backend:

```bash
python run_backend.py
```

The backend will:
1. Load `nilm_rf_model.pkl`
2. Start API server on `http://localhost:8000`
3. Accept prediction requests
4. Stream real-time predictions via WebSocket

## 🌐 Frontend Integration

### API Endpoints:

1. **POST /api/predict** - Single prediction
   ```javascript
   fetch('http://localhost:8000/api/predict', {
       method: 'POST',
       headers: { 'Content-Type': 'application/json' },
       body: JSON.stringify(powerData)
   })
   ```

2. **WebSocket /ws** - Real-time stream
   ```javascript
   const ws = new WebSocket('ws://localhost:8000/ws');
   ws.onmessage = (event) => {
       const prediction = JSON.parse(event.data);
       updateDeviceUI(prediction.device_states);
   };
   ```

3. **GET /api/latest** - Latest predictions
   ```javascript
   fetch('http://localhost:8000/api/latest')
   ```

### React Example:

```typescript
import { useState, useEffect } from 'react';

function DeviceMonitor() {
    const [devices, setDevices] = useState({
        bulb: false,
        fan: false,
        iron: false
    });

    useEffect(() => {
        const ws = new WebSocket('ws://localhost:8000/ws');
        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            setDevices(data.device_states);
        };
        return () => ws.close();
    }, []);

    return (
        <div>
            <h2>Device Status</h2>
            <div>Bulb: {devices.bulb ? '💡 ON' : '⚫ OFF'}</div>
            <div>Fan: {devices.fan ? '🌀 ON' : '⚫ OFF'}</div>
            <div>Iron: {devices.iron ? '🔥 ON' : '⚫ OFF'}</div>
        </div>
    );
}
```

## 🔄 Model Updates

### Retraining the Model:

1. Update the dataset: `full dataset.csv`
2. Run the notebook: `NILM_RF.ipynb`
3. The pickle file will be updated
4. Restart the backend to load the new model

### Using Command Line:

```bash
python backend/train_model.py --data "full dataset.csv" --artifact backend/artifacts/nilm_rf_model.pkl
```

## 🐛 Troubleshooting

### Model File Not Found
```
❌ Error: Model file not found: backend/artifacts/nilm_rf_model.pkl
```
**Solution**: Run all cells in `NILM_RF.ipynb` to create the pickle file.

### Missing Features
```
❌ Error: Missing required features
```
**Solution**: Ensure your input data includes all required fields (voltage, current, power, pf, kwh).

### Backend Won't Start
```
❌ Error: Address already in use
```
**Solution**: Stop any running backend processes or change the port:
```bash
PORT=8001 python run_backend.py
```

## 📚 Additional Resources

- **test_predictions.py**: Comprehensive testing examples
- **FRONTEND_INTEGRATION.py**: Frontend integration guide
- **backend/predictor.py**: Prediction implementation
- **NILM_RF.ipynb**: Model training notebook

## 🎓 Example Use Cases

### 1. Real-time Monitoring
Stream MQTT data → Backend API → Frontend displays device states

### 2. Historical Analysis
Load CSV data → Batch predictions → Save results to database

### 3. Energy Management
Detect device usage → Calculate costs → Generate reports

### 4. Anomaly Detection
Monitor predictions → Alert on unusual patterns → Log events

## ✅ Checklist

- [ ] Run `NILM_RF.ipynb` to create pickle file
- [ ] Verify file exists: `backend/artifacts/nilm_rf_model.pkl`
- [ ] Test predictions: `python test_predictions.py`
- [ ] Start backend: `python run_backend.py`
- [ ] Test API: `curl http://localhost:8000/api/status`
- [ ] Connect frontend to backend API
- [ ] Verify real-time predictions via WebSocket

## 🎉 Success!

Once everything is set up, you'll have:
- ✅ Trained model saved as pickle file
- ✅ Backend API serving predictions
- ✅ Frontend displaying device states in real-time
- ✅ Complete NILM system working end-to-end

---

**Need Help?** Check the example files or run the test scripts!
