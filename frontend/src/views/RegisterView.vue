<template>
  <div class="min-h-screen flex items-center justify-center p-4">
    <div class="w-full max-w-md bg-white rounded-2xl shadow-lg p-8 border border-gray-200">
      <h1 class="text-3xl font-bold text-center text-gray-800 mb-1">🔐 SSLMS</h1>
      <p class="text-center text-gray-500 text-sm mb-6">Create your account</p>

      <form @submit.prevent="handleRegister">
        <div class="mb-4">
          <label class="block text-xs font-bold text-gray-600 uppercase tracking-wide mb-2">Username</label>
          <input v-model="username" type="text" placeholder="Choose a username" autocomplete="username"
                 class="w-full px-4 py-2 bg-gray-100 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent" />
        </div>
        <div class="mb-5">
          <label class="block text-xs font-bold text-gray-600 uppercase tracking-wide mb-2">Password</label>
          <input v-model="password" type="password" placeholder="Choose a password" autocomplete="new-password"
                 class="w-full px-4 py-2 bg-gray-100 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent" />
        </div>

        <p v-if="error" class="text-red-500 text-xs text-center mb-4">{{ error }}</p>
        <p v-if="success" class="text-green-500 text-xs text-center mb-4">{{ success }}</p>

        <button class="w-full bg-indigo-600 text-white font-bold py-3 px-4 rounded-lg hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-transform transform hover:-translate-y-0.5 disabled:opacity-50 disabled:transform-none"
                type="submit" :disabled="loading">
          {{ loading ? 'Registering…' : 'Register' }}
        </button>
      </form>

      <p class="text-center text-sm text-gray-500 mt-6">
        Already have an account?
        <RouterLink to="/login" class="font-semibold text-indigo-600 hover:text-indigo-700 ml-1">Log In</RouterLink>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { authAPI } from '../api'

const router = useRouter()
const username = ref('')
const password = ref('')
const error = ref('')
const success = ref('')
const loading = ref(false)

async function handleRegister() {
  error.value = ''
  success.value = ''
  loading.value = true
  try {
    await authAPI.register(username.value, password.value)
    success.value = 'Account created! Redirecting to login…'
    setTimeout(() => router.push('/login'), 1200)
  } catch (err) {
    error.value = err.response?.data?.error || 'Registration failed'
  } finally {
    loading.value = false
  }
}
</script>

