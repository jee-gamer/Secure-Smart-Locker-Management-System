<template>
  <div class="flex flex-col items-center justify-center aspect-square rounded-xl border-2 p-2 gap-1 transition-all duration-200 user-select-none"
       :class="cellClass" @click="handleClick">
    <div class="text-xs font-semibold text-gray-400">#{{ locker.id }}</div>
    <div class="text-3xl leading-none">{{ icon }}</div>
    <div class="text-xs font-bold uppercase tracking-wider" :class="statusLabelClass">{{ statusLabel }}</div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  locker: { type: Object, required: true },
  currentUser: { type: Object, required: true },
  booking: { type: Object }
})

const emit = defineEmits(['book', 'open', 'unbook'])

const isAvailable = computed(() => props.locker.status === 'available')
const iAmSender = computed(() => {
  return props.booking && props.booking.user_id === props.currentUser.id
})
const iAmReceiver = computed(() => {
  return props.booking && props.booking.receiver_id === props.currentUser.id
})

const icon = computed(() => {
  if (isAvailable.value) return '🔓'
  if (iAmReceiver.value) return '📦'
  if (iAmSender.value) return '📤'
  return '🔒'
})

const statusLabel = computed(() => {
  if (isAvailable.value) return 'Available'
  if (iAmReceiver.value) return 'For you'
  if (iAmSender.value) return 'Sent'
  return 'Occupied'
})

const statusLabelClass = computed(() => ({
  'text-indigo-500': isAvailable.value,
  'text-green-500': iAmReceiver.value,
  'text-orange-500': iAmSender.value,
  'text-gray-500': !isAvailable.value && !iAmReceiver.value && !iAmSender.value,
}))

const cellClass = computed(() => {
  if (isAvailable.value) {
    return 'bg-white border-gray-300 cursor-pointer hover:border-indigo-500 hover:shadow-md hover:-translate-y-0.5'
  }
  if (iAmReceiver.value) {
    return 'bg-green-50 border-green-400 cursor-pointer hover:shadow-lg hover:shadow-green-100 hover:-translate-y-0.5'
  }
  if (iAmSender.value) {
    return 'bg-orange-50 border-orange-400 cursor-pointer hover:shadow-lg hover:shadow-orange-100 hover:-translate-y-0.5'
  }
  return 'bg-gray-100 border-gray-300 opacity-70 cursor-not-allowed'
})

function handleClick() {
  if (isAvailable.value) {
    emit('book', props.locker)
  } else if (iAmReceiver.value) {
    emit('open', props.locker)
  } else if (iAmSender.value) {
    // In this app logic, sender can unbook.
    emit('unbook', props.locker)
  }
  // else: occupied by someone else — do nothing
}
</script>

