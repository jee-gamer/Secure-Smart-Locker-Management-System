<template>
  <div class="fixed inset-0 bg-black/60 flex items-center justify-center p-4 z-50" @click.self="$emit('cancel')">
    <div class="w-full max-w-sm bg-white rounded-2xl shadow-lg p-6 border border-gray-200">
      <h3 class="text-xl font-bold text-gray-800 mb-1">📦 Deposit Item</h3>
      <p class="text-sm text-gray-500 mb-6">Locker <strong class="font-semibold text-gray-700">#{{ locker.id }}</strong></p>

      <div class="mb-4 relative">
        <label class="block text-xs font-bold text-gray-600 uppercase tracking-wide mb-2">Send to (Receiver)</label>
        <input type="text"
               v-model="searchQuery"
               @focus="showSuggestions = true"
               @blur="hideSuggestions"
               placeholder="Search for a user..."
               class="w-full px-4 py-2 bg-gray-100 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent">
        <ul v-if="showSuggestions && filteredUsers.length" class="absolute z-10 w-full bg-white border border-gray-300 rounded-lg mt-1 max-h-40 overflow-y-auto">
          <li v-for="u in filteredUsers" :key="u.id" @click="selectUser(u)" class="px-4 py-2 hover:bg-gray-100 cursor-pointer">
            {{ u.username }}
          </li>
        </ul>
        <ul v-if="!filteredUsers.length && searchQuery" class="absolute z-10 w-full bg-white border border-gray-300 rounded-lg mt-1 max-h-40 overflow-y-auto">
          <li class="px-4 py-2 hover:bg-gray-100 cursor-pointer">
            User doesn't exist.
          </li>
        </ul>
      </div>

      <div class="mb-4">
        <label class="block text-xs font-bold text-gray-600 uppercase tracking-wide mb-2">Item Image</label>
        <input type="file" @change="onFileChange" class="w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100"/>
      </div>

      <div v-if="imagePreviewUrl" class="mb-4">
        <img :src="imagePreviewUrl" alt="Image preview" class="max-h-40 rounded-lg mx-auto" />
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
import { ref, computed } from 'vue'

const props = defineProps({
  locker: { type: Object, required: true },
  users:  { type: Array,  required: true },
})
const emit = defineEmits(['confirm', 'cancel'])

const searchQuery = ref('')
const selectedReceiver = ref(null)
const showSuggestions = ref(false)
const error = ref('')
const itemImage = ref(null)
const imagePreviewUrl = ref('')

const filteredUsers = computed(() => {
  const validUsers = props.users.filter(user => user && user.username)

  if (!searchQuery.value) {
    return validUsers
  }

  return validUsers.filter(user =>
    user.username.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

function selectUser(user) {
  selectedReceiver.value = user
  searchQuery.value = user.username
  showSuggestions.value = false
}

function hideSuggestions() {
  // Delay hiding to allow click event to register
  setTimeout(() => {
    showSuggestions.value = false
  }, 200)
}

function onFileChange(e) {
  const file = e.target.files[0]
  itemImage.value = file
  if (file) {
    imagePreviewUrl.value = URL.createObjectURL(file)
  } else {
    imagePreviewUrl.value = ''
  }
}

function confirm() {
  if (!selectedReceiver.value) {
    error.value = 'Please select a receiver'
    return
  }
  emit('confirm', {
    lockerId: props.locker.id,
    receiverId: selectedReceiver.value.id,
    itemImage: itemImage.value,
  })
}
</script>
