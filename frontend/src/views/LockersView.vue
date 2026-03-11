<template>
  <div class="page">
    <!-- Navbar -->
    <header class="navbar">
      <span class="brand">🔐 SSLMS</span>
      <div class="nav-right">
        <span class="welcome">👤 {{ auth.user.username }}</span>
        <button class="btn btn-ghost" @click="handleLogout">Log Out</button>
      </div>
    </header>

    <!-- Main content -->
    <main class="main">
      <h2 class="section-title">Locker Grid</h2>
      <p class="section-sub">Click an available locker to deposit an item. Click your occupied locker to retrieve it.</p>

      <div v-if="loadingLockers" class="loading">Loading lockers…</div>

      <div v-else class="grid">
        <LockerCell
          v-for="locker in lockers"
          :key="locker.id"
          :locker="locker"
          :current-user="auth.user"
          @book="openBookModal"
          @open="openViewModal"
          @unbook="handleUnbook"
        />
      </div>
    </main>

    <!-- Book Modal -->
    <BookModal
      v-if="bookTarget"
      :locker="bookTarget"
      :users="otherUsers"
      @confirm="handleBook"
      @cancel="bookTarget = null"
    />

    <!-- Open/View Modal -->
    <OpenModal
      v-if="viewTarget"
      :locker="viewTarget"
      @close="viewTarget = null"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { auth } from '../stores/auth'
import { lockerAPI, bookingAPI, authAPI } from '../api'
import LockerCell from '../components/LockerCell.vue'
import BookModal from '../components/BookModal.vue'
import OpenModal from '../components/OpenModal.vue'

const router = useRouter()
const lockers = ref([])
const users = ref([])
const loadingLockers = ref(true)
const bookTarget = ref(null)
const viewTarget = ref(null)

const otherUsers = computed(() =>
  users.value.filter(u => u.id !== auth.user.id)
)

async function fetchLockers() {
  loadingLockers.value = true
  try {
    const [lockersRes, usersRes] = await Promise.all([
      lockerAPI.getAll(),
      authAPI.getUsers(),
    ])
    lockers.value = lockersRes.data
    users.value = usersRes.data
  } finally {
    loadingLockers.value = false
  }
}

function openBookModal(locker) {
  bookTarget.value = locker
}

async function openViewModal(locker) {
  // fetch full locker detail including booking info
  const res = await lockerAPI.getOne(locker.id)
  viewTarget.value = res.data
}

async function handleBook({ lockerId, receiverId }) {
  try {
    await bookingAPI.book(auth.user.id, receiverId, lockerId)
    bookTarget.value = null
    await fetchLockers()
  } catch (err) {
    alert(err.response?.data?.error || 'Booking failed')
  }
}

async function handleUnbook(locker) {
  try {
    await bookingAPI.unbook(auth.user.id, locker.id)
    await fetchLockers()
  } catch (err) {
    alert(err.response?.data?.error || 'Unbook failed')
  }
}

function handleLogout() {
  auth.logout()
  router.push('/login')
}

onMounted(fetchLockers)
</script>

<style scoped>
.page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.9rem 2rem;
  background: #1a1d27;
  border-bottom: 1px solid #2d3148;
  position: sticky;
  top: 0;
  z-index: 10;
}
.brand {
  font-size: 1.2rem;
  font-weight: 700;
  color: #6366f1;
}
.nav-right {
  display: flex;
  align-items: center;
  gap: 1rem;
}
.welcome {
  font-size: 0.9rem;
  color: #a0aec0;
}

.main {
  flex: 1;
  padding: 2rem;
  max-width: 900px;
  margin: 0 auto;
  width: 100%;
}
.section-title {
  font-size: 1.4rem;
  font-weight: 700;
  margin-bottom: 0.4rem;
}
.section-sub {
  color: #718096;
  font-size: 0.875rem;
  margin-bottom: 2rem;
}

.loading {
  text-align: center;
  color: #718096;
  padding: 3rem;
}

.grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 1rem;
}
</style>
