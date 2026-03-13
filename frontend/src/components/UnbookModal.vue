<template>
  <div class="fixed inset-0 bg-black/60 flex items-center justify-center p-4 z-50" @click.self="$emit('cancel')">
    <div class="w-full max-w-sm bg-white rounded-2xl shadow-lg p-6 border border-gray-200 flex flex-col gap-4">
      <h3 class="text-xl font-bold text-gray-800">Cancel Booking</h3>
      <p class="text-sm text-gray-500">
        Are you sure you want to cancel the booking for locker <strong class="font-semibold text-gray-700">#{{ locker.id }}</strong>?
      </p>

      <div class="flex justify-end gap-3">
        <button class="px-4 py-2 text-sm font-semibold text-gray-700 bg-gray-200 rounded-lg hover:bg-gray-300" @click="$emit('cancel')">
          Nevermind
        </button>
        <button class="px-4 py-2 text-sm font-semibold text-white bg-red-600 rounded-lg hover:bg-red-700" @click="$emit('confirm', locker)">
          Yes, Cancel
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  locker: { type: Object, required: true },
})
defineEmits(['confirm', 'cancel'])
</script>
