<template>
  <div class="fixed inset-0 bg-black/60 flex items-center justify-center p-4 z-50" @click.self="$emit('close')">
    <div class="w-full max-w-sm bg-white rounded-2xl shadow-lg p-6 border border-gray-200 text-center">
      <h3 class="text-xl font-bold text-gray-800 mb-1">📬 Your Package</h3>
      <p class="text-sm text-gray-500 mb-6">Locker <strong class="font-semibold text-gray-700">#{{ locker.id }}</strong></p>

      <div class="flex flex-col items-center gap-6">
        <img :src="getImageUrl(locker.item_image_path)" alt="Package" class="w-36 h-36 package-anim" />

        <div class="w-full bg-gray-100 rounded-lg p-4 text-left space-y-2 border border-gray-200">
          <div class="flex justify-between items-baseline">
            <span class="text-xs font-bold text-gray-500 uppercase tracking-wider">From</span>
            <span class="text-base font-semibold text-gray-800">{{ locker.sender_username || '—' }}</span>
          </div>
          <div class="flex justify-between items-baseline">
            <span class="text-xs font-bold text-gray-500 uppercase tracking-wider">To</span>
            <span class="text-base font-semibold text-gray-800">{{ locker.receiver_username || '—' }}</span>
          </div>
        </div>
      </div>

      <div class="flex justify-end mt-6">
        <button class="px-4 py-2 text-sm font-semibold text-gray-700 bg-gray-200 rounded-lg hover:bg-gray-300" @click="$emit('close')">Close</button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  locker: { type: Object, required: true },
})
defineEmits(['close'])

function getImageUrl(path) {
  if (!path) {
    return new URL('../assets/package.svg', import.meta.url).href
  }
  return `http://localhost:5000/uploads/${path.split(/[\\/]/).pop()}`
}
</script>

<style scoped>
.package-anim {
  filter: drop-shadow(0 0 12px rgba(99, 102, 241, 0.3));
  animation: float 3s ease-in-out infinite;
}
@keyframes float {
  0%, 100% { transform: translateY(0); }
  50%       { transform: translateY(-6px); }
}
</style>
