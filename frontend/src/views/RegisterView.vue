<template>
  <div class="auth-page">
    <div class="card auth-card">
      <h1 class="auth-title">🔐 SSLMS</h1>
      <p class="auth-sub">Create your account</p>

      <form @submit.prevent="handleRegister">
        <div class="field">
          <label>Username</label>
          <input v-model="username" type="text" placeholder="Choose a username" autocomplete="username" />
        </div>
        <div class="field">
          <label>Password</label>
          <input v-model="password" type="password" placeholder="Choose a password" autocomplete="new-password" />
        </div>

        <p v-if="error" class="error-msg">{{ error }}</p>
        <p v-if="success" class="success-msg">{{ success }}</p>

        <button class="btn btn-primary full-width" type="submit" :disabled="loading">
          {{ loading ? 'Registering…' : 'Register' }}
        </button>
      </form>

      <p class="switch-link">
        Already have an account?
        <RouterLink to="/login">Log In</RouterLink>
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

<style scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}
.auth-card {
  width: 100%;
  max-width: 420px;
}
.auth-title {
  font-size: 1.8rem;
  font-weight: 700;
  text-align: center;
  margin-bottom: 0.25rem;
}
.auth-sub {
  text-align: center;
  color: #718096;
  font-size: 0.85rem;
  margin-bottom: 1.75rem;
}
.field {
  margin-bottom: 1rem;
}
.full-width {
  width: 100%;
  margin-top: 1.25rem;
  padding: 0.7rem;
}
.switch-link {
  text-align: center;
  margin-top: 1.25rem;
  font-size: 0.875rem;
  color: #718096;
}
.switch-link a {
  color: #6366f1;
  font-weight: 600;
  margin-left: 0.25rem;
}
.success-msg {
  color: #68d391;
  font-size: 0.85rem;
  margin-top: 0.5rem;
}
</style>
