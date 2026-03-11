<template>
  <div class="locker-cell" :class="cellClass" @click="handleClick">
    <div class="locker-id">#{{ locker.id }}</div>
    <div class="locker-icon">{{ icon }}</div>
    <div class="locker-status">{{ statusLabel }}</div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  locker: { type: Object, required: true },
  currentUser: { type: Object, required: true },
})

const emit = defineEmits(['book', 'open', 'unbook'])

const isAvailable = computed(() => props.locker.status === 'available')

// A locker is "mine as sender" if we sent something there (we can unbook)
// A locker is "mine as receiver" if we are the receiver (we can open/view)
// We get sender_id/receiver_id only from the detail endpoint,
// but the list endpoint only has id/status.
// So we pass booking info via the enriched locker object when available.
const iAmSender = computed(() =>
  props.locker.sender_id === props.currentUser.id
)
const iAmReceiver = computed(() =>
  props.locker.receiver_id === props.currentUser.id
)

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

const cellClass = computed(() => ({
  'available': isAvailable.value,
  'occupied': !isAvailable.value,
  'mine-receiver': iAmReceiver.value,
  'mine-sender': iAmSender.value,
}))

function handleClick() {
  if (isAvailable.value) {
    emit('book', props.locker)
  } else if (iAmReceiver.value) {
    emit('open', props.locker)
  } else if (iAmSender.value) {
    emit('unbook', props.locker)
  }
  // else: occupied by someone else — do nothing
}
</script>

<style scoped>
.locker-cell {
  background: #1a1d27;
  border: 2px solid #2d3148;
  border-radius: 12px;
  padding: 1rem 0.5rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.4rem;
  cursor: default;
  transition: transform 0.15s, border-color 0.2s, box-shadow 0.2s;
  user-select: none;
  aspect-ratio: 1;
  justify-content: center;
}

.available {
  border-color: #2d3148;
  cursor: pointer;
}
.available:hover {
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99,102,241,0.15);
  transform: translateY(-2px);
}

.mine-receiver {
  border-color: #68d391;
  background: #1a2c23;
  cursor: pointer;
}
.mine-receiver:hover {
  box-shadow: 0 0 0 3px rgba(104,211,145,0.2);
  transform: translateY(-2px);
}

.mine-sender {
  border-color: #f6ad55;
  background: #2c2013;
  cursor: pointer;
}
.mine-sender:hover {
  box-shadow: 0 0 0 3px rgba(246,173,85,0.2);
  transform: translateY(-2px);
}

.occupied {
  border-color: #4a5568;
  opacity: 0.6;
}

.locker-id {
  font-size: 0.7rem;
  color: #4a5568;
  font-weight: 600;
}
.locker-icon {
  font-size: 1.8rem;
  line-height: 1;
}
.locker-status {
  font-size: 0.72rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: #a0aec0;
}

.mine-receiver .locker-status { color: #68d391; }
.mine-sender  .locker-status  { color: #f6ad55; }
.available    .locker-status  { color: #6366f1; }
</style>
