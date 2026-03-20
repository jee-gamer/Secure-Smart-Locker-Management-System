<template>
  <div class="min-h-screen flex flex-col bg-gray-50">
    <!-- Navbar -->
    <header class="sticky top-0 z-10 bg-white/80 backdrop-blur-md border-b border-gray-200">
      <div class="mx-auto max-w-5xl px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          <span class="text-xl font-bold text-indigo-600">🔐 SSLMS</span>
          <div class="flex items-center gap-4">
            <span v-if="auth.user" class="text-sm font-medium text-gray-600">👤 {{ auth.user.username }}</span>
            <button class="px-4 py-2 text-sm font-semibold text-gray-700 bg-gray-200 rounded-lg hover:bg-gray-300" @click="handleLogout">Log Out</button>
          </div>
        </div>
      </div>
    </header>

    <!-- Main content -->
    <main class="flex-1 w-full max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h2 class="text-2xl font-bold text-gray-800 mb-2">Locker Grid</h2>
      <p class="text-sm text-gray-500 mb-8">Click an available locker to deposit an item. Click your occupied locker to retrieve it.</p>

      <div v-if="loadingLockers" class="text-center text-gray-500 py-12">Loading lockers…</div>

      <div v-else class="grid grid-cols-5 gap-4">
        <LockerCell
          v-for="locker in lockers"
          :key="locker.id"
          :locker="locker"
          :current-user="auth.user"
          :booking="bookingForLocker(locker.id)"
          @book="openBookModal"
          @open="openViewModal"
          @unbook="openUnbookModal"
        />
      </div>
    </main>

    <!-- Modals -->
    <BookModal v-if="bookTarget" :locker="bookTarget" :users="otherUsers" @confirm="handleBook" @cancel="bookTarget = null" />
    <OpenModal v-if="viewTarget" :locker="viewTarget" @close="viewTarget = null" />
    <UnbookModal v-if="unbookTarget" :locker="unbookTarget" @confirm="handleUnbook" @cancel="unbookTarget = null" />
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
import UnbookModal from '../components/UnbookModal.vue'

const router = useRouter()
const lockers = ref([])
const users = ref([])
const bookings = ref([])
const loadingLockers = ref(true)
const bookTarget = ref(null)
const viewTarget = ref(null)
const unbookTarget = ref(null)

const otherUsers = computed(() =>
  users.value.filter(u => u.id !== auth.user.id)
)

async function fetchLockers() {
  loadingLockers.value = true
  try {
    const [lockersRes, usersRes, bookingsRes] = await Promise.all([
      lockerAPI.getAll(),
      authAPI.getUsers(),
      bookingAPI.getActive()
    ])
    lockers.value = lockersRes.data
    users.value = usersRes.data
    bookings.value = bookingsRes.data
  } finally {
    loadingLockers.value = false
  }
}

function bookingForLocker(locker_id) {
  return bookings.value.find(b => b.locker_id === locker_id)
}

function openBookModal(locker) {
  bookTarget.value = locker
}

function openUnbookModal(locker) {
  unbookTarget.value = locker
}

async function openViewModal(locker) {
  // fetch full locker detail including booking info
  const res = await lockerAPI.getOne(locker.id)
  viewTarget.value = res.data
}

async function handleBook({ lockerId, receiverId, itemImage }) {
  const formData = new FormData();
  formData.append('user_id', auth.user.id);
  formData.append('receiver_id', receiverId);
  formData.append('locker_id', lockerId);
  if (itemImage) {
    formData.append('item_image', itemImage);
  }

  try {
    await bookingAPI.book(formData);
    bookTarget.value = null
    await fetchLockers()
  } catch (err) {
    alert(err.response?.data?.error || 'Booking failed')
  }
}

async function handleUnbook(locker) {
  try {
    await bookingAPI.unbook(auth.user.id, locker.id)
    unbookTarget.value = null
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

