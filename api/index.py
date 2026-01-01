from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import os

app = Flask(__name__)
CORS(app)

base_path = os.path.dirname(__file__)
model_path = os.path.join(base_path, 'model_mobil.pkl')

with open(model_path, 'rb') as file:
    model = pickle.load(file)

@app.route('/')
def home():
    return "Backend AI Ready!"

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        tahun = float(data['tahun'])
        km = float(data['km'])
        
        hasil_prediksi = model.predict([[tahun, km]])
        harga_juta = round(hasil_prediksi[0], 2)
        
        return jsonify({
            'status': 'sukses',
            'pesan': f'Mobil tahun {int(tahun)} dengan KM {int(km)}',
            'estimasi_harga': harga_juta
        })
    except Exception as e:
        return jsonify({'status': 'error', 'pesan': str(e)})
