# 🚀 NILM Pickle Model - Quick Reference

## ✅ Model Saved Successfully!
**Location**: `backend/artifacts/nilm_rf_model.pkl` (0.99 MB)

---

## 📊 Input Format (6 features required)
```python
{
    'voltage': 230.5,           # Volts
    'current': 4.78,            # Amperes
    'active_power': 1100,       # Watts
    'reactive_power': 0,        # VAR
    'apparent_power': 1100,     # VA
    'power_factor': 1.0         # 0-1
}
```

---

## 📤 Output Format
```python
{
    'label': 4,                 # Class: 1-7
    'device_states': {
        'bulb': False,
        'fan': False,
        'iron': True
    },
    'confidence': 0.95          # 0-1
}
```

---

## 🐍 Python Usage (Backend)

```python
from backend.predictor import NILMPredictor

predictor = NILMPredictor()
result = predictor.predict_single({
    'voltage': 230,
    'current': 4.78,
    'active_power': 1100,
    'reactive_power': 0,
    'apparent_power': 1100,
    'power_factor': 1.0
})
print(result['device_states'])
```

---

## 🌐 JavaScript Usage (Frontend)

```javascript
// REST API
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

// WebSocket
const ws = new WebSocket('ws://localhost:8000/ws');
ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log(data.device_states);
};
```

---

## ⚡ Quick Commands

```bash
# Test the model
python test_predictions.py

# Start backend
python run_backend.py

# Retrain model (in notebook)
# Run all cells in NILM_RF.ipynb

# Check model info
python -c "import pickle; m=pickle.load(open('backend/artifacts/nilm_rf_model.pkl','rb')); print('Features:', m['feature_columns'])"
```

---

## 🎯 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/predict` | Get prediction |
| GET | `/api/latest` | Latest predictions |
| GET | `/api/status` | Service status |
| WS | `/ws` | Real-time stream |

---

## 🔢 Label Meanings

| Label | Bulb | Fan | Iron | Power |
|-------|------|-----|------|-------|
| 1 | ✅ | ❌ | ❌ | 60W |
| 2 | ❌ | ✅ | ❌ | 80W |
| 3 | ✅ | ✅ | ❌ | 140W |
| 4 | ❌ | ❌ | ✅ | 1100W |
| 5 | ✅ | ❌ | ✅ | 1160W |
| 6 | ❌ | ✅ | ✅ | 1180W |
| 7 | ✅ | ✅ | ✅ | 1240W |

---

## 📚 Documentation

- **IMPLEMENTATION_SUMMARY.md** - Complete overview
- **MODEL_USAGE_GUIDE.md** - Detailed guide
- **FRONTEND_INTEGRATION.py** - Frontend examples
- **test_predictions.py** - Working examples

---

## ✨ You're Ready!

✅ Model trained and saved  
✅ Backend API ready  
✅ Frontend integration ready  
✅ Tests passing  
✅ Documentation complete  

**Start using predictions now!** 🎉
