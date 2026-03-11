<template>
  <div class="auth-page">
    <div class="card auth-card">
      <h1 class="auth-title">🔐 SSLMS</h1>
      <p class="auth-sub">Smart Secure Locker Management</p>

      <form @submit.prevent="handleLogin">
        <div class="field">
          <label>Username</label>
          <input v-model="username" type="text" placeholder="Enter username" autocomplete="username" />
        </div>
        <div class="field">
          <label>Password</label>
          <input v-model="password" type="password" placeholder="Enter password" autocomplete="current-password" />
        </div>

        <p v-if="error" class="error-msg">{{ error }}</p>

        <button class="btn btn-primary full-width" type="submit" :disabled="loading">
          {{ loading ? 'Logging in…' : 'Log In' }}
        </button>
      </form>

      <p class="switch-link">
        Don't have an account?
        <RouterLink to="/register">Register</RouterLink>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { authAPI } from '../api'
import { auth } from '../stores/auth'

const router = useRouter()
const username = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

async function handleLogin() {
  error.value = ''
  loading.value = true
  try {
    const res = await authAPI.login(username.value, password.value)
    auth.login(res.data.user)
    router.push('/lockers')
  } catch (err) {
    error.value = err.response?.data?.error || 'Login failed'
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
</style>
