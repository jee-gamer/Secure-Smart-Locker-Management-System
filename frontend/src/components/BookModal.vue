<template>
  <div class="fixed inset-0 bg-black/60 flex items-center justify-center p-4 z-50" @click.self="$emit('cancel')">
    <div class="w-full max-w-sm bg-white rounded-2xl shadow-lg p-6 border border-gray-200">
      <h3 class="text-xl font-bold text-gray-800 mb-1">📦 Deposit Item</h3>
      <p class="text-sm text-gray-500 mb-6">Locker <strong class="font-semibold text-gray-700">#{{ locker.id }}</strong></p>

      <div class="mb-4">
        <label class="block text-xs font-bold text-gray-600 uppercase tracking-wide mb-2">Send to (Receiver)</label>
        <select v-model="selectedReceiver"
                class="w-full px-4 py-2 bg-gray-100 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent">
          <option disabled value="">— Select a user —</option>
          <option v-for="u in users" :key="u.id" :value="u.id">
            {{ u.username }}
          </option>
        </select>
      </div>

      <p v-if="error" class="text-red-500 text-xs text-center mb-4">{{ error }}</p>

      <div class="flex justify-end gap-3 mt-6">
        <button class="px-4 py-2 text-sm font-semibold text-gray-700 bg-gray-200 rounded-lg hover:bg-gray-300" @click="$emit('cancel')">Cancel</button>
        <button class="px-4 py-2 text-sm font-semibold text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 disabled:opacity-50" @click="confirm" :disabled="!selectedReceiver">
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

