<template>
  <div class="overlay" @click.self="$emit('close')">
    <div class="modal card">
      <h3 class="modal-title">📬 Your Package</h3>
      <p class="modal-sub">Locker <strong>#{{ locker.id }}</strong></p>

      <div class="package-display">
        <img src="../assets/package.svg" alt="Package" class="package-img" />
        <div class="package-info">
          <div class="info-row">
            <span class="info-label">From</span>
            <span class="info-value">{{ locker.sender_username || '—' }}</span>
          </div>
          <div class="info-row">
            <span class="info-label">To</span>
            <span class="info-value">{{ locker.receiver_username || '—' }}</span>
          </div>
        </div>
      </div>

      <div class="modal-actions">
        <button class="btn btn-ghost" @click="$emit('close')">Close</button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  locker: { type: Object, required: true },
})
defineEmits(['close'])
</script>

<style scoped>
.overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.65);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
  padding: 1rem;
}
.modal {
  width: 100%;
  max-width: 420px;
}
.modal-title {
  font-size: 1.2rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
}
.modal-sub {
  color: #718096;
  font-size: 0.875rem;
  margin-bottom: 1.5rem;
}
.package-display {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
}
.package-img {
  width: 140px;
  height: 140px;
  object-fit: contain;
  filter: drop-shadow(0 0 18px rgba(99,102,241,0.4));
  animation: float 3s ease-in-out infinite;
}
@keyframes float {
  0%, 100% { transform: translateY(0); }
  50%       { transform: translateY(-8px); }
}
.package-info {
  width: 100%;
  background: #0f1117;
  border-radius: 10px;
  padding: 1rem 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}
.info-row {
  display: flex;
  justify-content: space-between;
  font-size: 0.9rem;
}
.info-label {
  color: #718096;
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.78rem;
  letter-spacing: 0.05em;
}
.info-value {
  color: #e2e8f0;
  font-weight: 600;
}
.modal-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 1.5rem;
}
</style>
