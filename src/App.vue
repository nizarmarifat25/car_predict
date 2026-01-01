<template>
  <div class="main-container">
    <div class="blob blob-1"></div>
    <div class="blob blob-2"></div>
    <div class="blob blob-3"></div>

    <div class="glass-card">
      <div class="card-header">
        <span class="badge">AI PROJECT</span>
        <button
          v-if="tahun || km"
          @click="resetForm"
          class="reset-btn"
          title="Reset Form"
        >
          ↺
        </button>

        <h1 class="title">
          Car Price <span class="gradient-text">Predictor</span>
        </h1>
        <p class="subtitle">
          Estimasi harga mobil bekas dengan algoritma Linear Regression
        </p>
      </div>

      <div class="input-section">
        <div class="input-wrapper">
          <input v-model="tahun" type="number" placeholder=" " id="tahun" />
          <label for="tahun">Tahun Pembuatan (Misal: 2018)</label>
          <div class="icon">📅</div>
        </div>

        <div class="input-wrapper">
          <input v-model="km" type="number" placeholder=" " id="km" />
          <label for="km">Jarak Tempuh (KM)</label>
          <div class="icon">🚀</div>
        </div>

        <button @click="prediksiHarga" :disabled="loading" class="glow-btn">
          <div v-if="loading" class="loader"></div>
          <span v-else>Analisa Harga Sekarang ⚡</span>
        </button>
      </div>

      <transition name="pop">
        <div v-if="errorMsg" class="error-toast">
          {{ errorMsg }}
        </div>
      </transition>

      <transition name="slide-up">
        <div v-if="hasil" class="result-display">
          <div class="result-label">ESTIMASI HARGA PASAR</div>
          <div class="price-tag">
            <span class="currency">Rp</span>
            <span class="amount">{{ displayHarga }}</span>
            <span class="unit">Juta</span>
          </div>
          <div class="specs">
            <span>{{ hasil.pesan }}</span>
          </div>
        </div>
      </transition>

      <div v-if="history.length > 0" class="history-section">
        <div class="divider"><span>Riwayat Pencarian</span></div>
        <transition-group name="list" tag="div" class="history-list">
          <div
            v-for="(item, index) in history"
            :key="index"
            class="history-item"
          >
            <div class="hist-info">
              <span class="hist-year">{{ item.tahun }}</span>
              <span class="hist-km">{{ item.km }} KM</span>
            </div>
            <div class="hist-price">Rp {{ item.harga }} Jt</div>
          </div>
        </transition-group>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";

const tahun = ref("");
const km = ref("");
const loading = ref(false);
const hasil = ref(null);
const errorMsg = ref("");
const displayHarga = ref(0);
const history = ref([]);

const animateValue = (start, end, duration) => {
  let startTimestamp = null;
  const step = (timestamp) => {
    if (!startTimestamp) startTimestamp = timestamp;
    const progress = Math.min((timestamp - startTimestamp) / duration, 1);
    const easeOutQuart = 1 - Math.pow(1 - progress, 4);
    displayHarga.value = (start + (end - start) * easeOutQuart).toFixed(2);
    if (progress < 1) window.requestAnimationFrame(step);
  };
  window.requestAnimationFrame(step);
};

const resetForm = () => {
  tahun.value = "";
  km.value = "";
  hasil.value = null;
  displayHarga.value = 0;
  errorMsg.value = "";
};

// --- FUNGSI PREDIKSI (API) ---
const prediksiHarga = async () => {
  if (!tahun.value || !km.value) {
    errorMsg.value = "⚠️ Waduh, datanya diisi dulu dong bre!";
    return;
  }

  loading.value = true;
  hasil.value = null;
  errorMsg.value = "";
  displayHarga.value = 0;

  await new Promise((r) => setTimeout(r, 800));

  try {
    const response = await axios.post("/api/predict", {
      tahun: tahun.value,
      km: km.value,
    });

    hasil.value = response.data;
    animateValue(0, response.data.estimasi_harga, 1500);

    history.value.unshift({
      tahun: tahun.value,
      km: km.value,
      harga: response.data.estimasi_harga,
    });

    if (history.value.length > 3) history.value.pop(); 
  } catch (error) {
    console.error(error);
    errorMsg.value = "Gagal connect ke AI. Cek server Python nya!";
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Outfit:wght@300;500;700;900&display=swap");
body,
html {
  margin: 0 !important;
  padding: 0 !important;
  width: 100%;
  height: 100%;
  background-color: #0f172a; 
  overflow-x: hidden; 
}

#app {
  width: 100%;
  min-height: 100vh;
  margin: 0;
  padding: 0;
}

.main-container {
  font-family: "Outfit", sans-serif;
  min-height: 100vh;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #0f172a;
  overflow: hidden;
  position: relative;
  color: white;
  padding: 20px;
  box-sizing: border-box;
}

.blob {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.6;
  z-index: 0;
  animation: float 10s infinite alternate;
}
.blob-1 {
  width: 400px;
  height: 400px;
  background: #764ba2;
  top: -50px;
  left: -100px;
}
.blob-2 {
  width: 300px;
  height: 300px;
  background: #667eea;
  bottom: -50px;
  right: -50px;
  animation-delay: -5s;
}
.blob-3 {
  width: 200px;
  height: 200px;
  background: #ec4899;
  bottom: 20%;
  left: 20%;
  animation-duration: 15s;
}

@keyframes float {
  0% {
    transform: translate(0, 0) scale(1);
  }
  100% {
    transform: translate(30px, 50px) scale(1.1);
  }
}

.glass-card {
  position: relative;
  z-index: 10;
  width: 100%;
  max-width: 420px;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 24px;
  padding: 40px 30px;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
  text-align: center;
}

.card-header {
  position: relative;
  margin-bottom: 20px;
}

.reset-btn {
  position: absolute;
  top: 0;
  right: 0;
  background: rgba(255, 255, 255, 0.1);
  border: none;
  color: #94a3b8;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  cursor: pointer;
  transition: 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
}
.reset-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  transform: rotate(180deg);
}

.badge {
  background: rgba(102, 126, 234, 0.2);
  color: #a3bffa;
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 1px;
}
.title {
  font-size: 2.2rem;
  font-weight: 800;
  margin: 15px 0 5px;
  line-height: 1.1;
}
.gradient-text {
  background: linear-gradient(to right, #667eea, #764ba2, #ec4899);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}
.subtitle {
  color: #94a3b8;
  font-size: 0.9rem;
  font-weight: 300;
  margin-bottom: 10px;
}

.input-section {
  display: flex;
  flex-direction: column;
  gap: 30px; 
  margin-top: 25px;
}
.input-wrapper {
  position: relative;
}

.input-wrapper input {
  width: 100%;
  background: rgba(0, 0, 0, 0.3); 
  border: 1px solid rgba(255, 255, 255, 0.2);
  padding: 16px 16px 16px 50px;
  border-radius: 12px;
  color: white;
  font-size: 1rem;
  outline: none;
  font-family: "Outfit", sans-serif;
  transition: all 0.3s ease;
  box-sizing: border-box; 
}
.input-wrapper input:focus {
  border-color: #667eea;
  background: rgba(0, 0, 0, 0.5);
  box-shadow: 0 0 15px rgba(102, 126, 234, 0.2);
}

.input-wrapper label {
  position: absolute;
  left: 50px;
  top: 50%;
  transform: translateY(-50%);
  color: #94a3b8;
  pointer-events: none;
  transition: 0.3s ease;
  font-size: 0.95rem;
  background: transparent; 
}

.input-wrapper .icon {
  position: absolute;
  left: 18px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 1.2rem;
  opacity: 0.7;
}

.input-wrapper input:focus ~ label,
.input-wrapper input:not(:placeholder-shown) ~ label {
  top: -25px; 
  left: 0;
  font-size: 0.85rem;
  color: #a3bffa;
  font-weight: 600;
  letter-spacing: 0.5px;
  transform: translateY(0);
}

.glow-btn {
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  border: none;
  padding: 16px;
  border-radius: 12px;
  color: white;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  margin-top: 10px;
  width: 100%;
  transition: transform 0.2s, box-shadow 0.2s;
  font-family: "Outfit", sans-serif;
}
.glow-btn:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 0 10px 25px rgba(118, 75, 162, 0.5);
}
.glow-btn:disabled {
  opacity: 0.7;
  cursor: wait;
}

.result-display {
  margin-top: 30px;
  padding: 20px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.2);
}
.result-label {
  font-size: 0.7rem;
  letter-spacing: 2px;
  color: #94a3b8;
  margin-bottom: 5px;
}
.price-tag {
  display: flex;
  align-items: baseline;
  justify-content: center;
  gap: 5px;
}
.currency {
  font-size: 1.5rem;
  color: #a3bffa;
}
.amount {
  font-size: 3.5rem;
  font-weight: 900;
  background: linear-gradient(to top, #a3bffa, #ffffff);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}
.unit {
  font-size: 1.2rem;
  font-weight: 600;
  color: #a3bffa;
}
.specs {
  color: #94a3b8;
  font-size: 0.85rem;
  margin-top: 5px;
}

.history-section {
  margin-top: 30px;
}
.divider {
  display: flex;
  align-items: center;
  color: #64748b;
  font-size: 0.8rem;
  margin-bottom: 15px;
}
.divider::before,
.divider::after {
  content: "";
  flex: 1;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}
.divider span {
  padding: 0 10px;
}

.history-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 15px;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 10px;
  margin-bottom: 8px;
  border: 1px solid rgba(255, 255, 255, 0.05);
  font-size: 0.9rem;
}
.hist-year {
  font-weight: 700;
  color: white;
  margin-right: 5px;
}
.hist-km {
  color: #94a3b8;
  font-size: 0.8rem;
}
.hist-price {
  color: #a3bffa;
  font-weight: 600;
}

.loader {
  width: 20px;
  height: 20px;
  border: 3px solid #fff;
  border-bottom-color: transparent;
  border-radius: 50%;
  display: inline-block;
  animation: rotation 1s linear infinite;
}
@keyframes rotation {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.slide-up-enter-active {
  transition: all 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.slide-up-enter-from {
  opacity: 0;
  transform: translateY(30px) scale(0.9);
}

.list-enter-active,
.list-leave-active {
  transition: all 0.5s ease;
}
.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateX(-30px);
}

.error-toast {
  color: #ff6b6b;
  margin-top: 15px;
  font-weight: 500;
}
</style>
