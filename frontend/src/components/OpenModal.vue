<template>
  <div class="fixed inset-0 bg-black/60 flex items-center justify-center p-4 z-50" @click.self="$emit('close')">
    <div class="w-full max-w-sm bg-white rounded-2xl shadow-lg p-6 border border-gray-200 text-center">
      <h3 class="text-xl font-bold text-gray-800 mb-1">📬 Your Package</h3>
      <p class="text-sm text-gray-500 mb-6">Locker <strong class="font-semibold text-gray-700">#{{ locker.id }}</strong></p>

      <div class="flex flex-col items-center gap-6">
        <img :src="imageSrc" @error="onImageError" alt="Package" class="w-60 h-60 object-contain package-anim" />
        <p v-if="empty" class="text-gray-500">There is nothing!</p>
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
import { ref, watchEffect } from "vue";
import { auth } from '../stores/auth'
import { lockerAPI } from '../api'

const props = defineProps({
  locker: { type: Object, required: true },
})
defineEmits(['close'])

const defaultImage = new URL('../assets/empty-box.svg', import.meta.url).href;
const imageSrc = ref(defaultImage);
const empty = ref(true);

watchEffect(() => {
  if (props.locker) {
    imageSrc.value = lockerAPI.getImageUrl(props.locker.id, auth.user.id);
    empty.value = false;
    // Log the access whenever the modal is shown with a locker
    if (auth.user && auth.user.id) {
      lockerAPI.logAccess(props.locker.id, auth.user.id).catch(err => {
        console.error('Failed to log locker access', err);
      });
    }
  }
});

function onImageError() {
  // If the image fails to load (e.g., 404 error), set it to the default.
  imageSrc.value = defaultImage;
  empty.value = true
}
</script>

<style scoped>
.package-anim {
  filter: drop-shadow(0 0 12px rgba(198, 120, 44, 0.3));
  animation: float 3s ease-in-out infinite;
}
@keyframes float {
  0%, 100% { transform: translateY(0); }
  50%       { transform: translateY(-6px); }
}
</style>
