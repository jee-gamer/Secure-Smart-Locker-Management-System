<template>
  <div class="overlay" @click.self="$emit('cancel')">
    <div class="modal card">
      <h3 class="modal-title">📦 Deposit Item</h3>
      <p class="modal-sub">Locker <strong>#{{ locker.id }}</strong></p>

      <div class="field">
        <label>Send to (Receiver)</label>
        <select v-model="selectedReceiver">
          <option disabled value="">— Select a user —</option>
          <option v-for="u in users" :key="u.id" :value="u.id">
            {{ u.username }}
          </option>
        </select>
      </div>

      <p v-if="error" class="error-msg">{{ error }}</p>

      <div class="modal-actions">
        <button class="btn btn-ghost" @click="$emit('cancel')">Cancel</button>
        <button class="btn btn-primary" @click="confirm" :disabled="!selectedReceiver">
          Confirm
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  locker: { type: Object, required: true },
  users:  { type: Array,  required: true },
})
const emit = defineEmits(['confirm', 'cancel'])

const selectedReceiver = ref('')
const error = ref('')

function confirm() {
  if (!selectedReceiver.value) {
    error.value = 'Please select a receiver'
    return
  }
  emit('confirm', {
    lockerId: props.locker.id,
    receiverId: selectedReceiver.value,
  })
}
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
  max-width: 400px;
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
.field {
  margin-bottom: 1rem;
}
.modal-actions {
  display: flex;
  gap: 0.75rem;
  justify-content: flex-end;
  margin-top: 1.5rem;
}
</style>
