<template>
  <div class="max-w-6xl mx-auto p-4 md:p-8">
    <div class="flex items-center justify-between mb-8">
      <h2 class="text-3xl font-extrabold text-gray-900 border-b-4 border-indigo-500 pb-2">Admin Logs</h2>
      <router-link to="/lockers" class="text-indigo-600 hover:text-indigo-800 font-semibold" v-if="auth.user?.role === 'admin'">Back to Lockers</router-link>
    </div>

    <!-- Tabs -->
    <div class="mb-6 flex gap-4 border-b border-gray-200 pb-2">
      <button
        @click="activeTab = 'bookings'"
        :class="['px-4 py-2 font-semibold text-sm rounded-t-lg transition-colors', activeTab === 'bookings' ? 'bg-indigo-50 text-indigo-700 border-b-2 border-indigo-700' : 'text-gray-500 hover:bg-gray-50']"
      >
        Booking Logs
      </button>
      <button
        @click="activeTab = 'access'"
        :class="['px-4 py-2 font-semibold text-sm rounded-t-lg transition-colors', activeTab === 'access' ? 'bg-indigo-50 text-indigo-700 border-b-2 border-indigo-700' : 'text-gray-500 hover:bg-gray-50']"
      >
        Access Logs (Views)
      </button>
    </div>

    <div v-if="loading" class="text-center py-10">
      <div class="inline-block animate-spin rounded-full h-8 w-8 border-4 border-indigo-500 border-t-transparent"></div>
      <p class="mt-2 text-gray-500">Loading logs...</p>
    </div>

    <div v-else class="overflow-x-auto bg-white rounded-xl shadow border border-gray-100">
      <!-- Booking Logs Table -->
      <table v-if="activeTab === 'bookings'" class="min-w-full divide-y divide-gray-200">
        <thead class="bg-indigo-50/50">
          <tr>
            <th class="px-6 py-4 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">ID</th>
            <th class="px-6 py-4 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Locker</th>
            <th class="px-6 py-4 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Sender</th>
            <th class="px-6 py-4 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Receiver</th>
            <th class="px-6 py-4 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Booked At</th>
            <th class="px-6 py-4 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Unbooked At</th>
            <th class="px-6 py-4 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Status</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100 bg-white">
          <tr v-for="log in logs" :key="log.id" class="hover:bg-gray-50 transition-colors">
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">#{{ log.id }}</td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                Locker {{ log.locker_id }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ log.sender }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ log.receiver }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ formatDate(log.start_time) }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ log.end_time ? formatDate(log.end_time) : '-' }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm">
               <span v-if="!log.end_time" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                Active
              </span>
              <span v-else class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-600">
                Completed
              </span>
            </td>
          </tr>
          <tr v-if="logs.length === 0">
            <td colspan="7" class="px-6 py-8 text-center text-gray-500">No logs found</td>
          </tr>
        </tbody>
      </table>

      <!-- Access Logs Table -->
      <table v-if="activeTab === 'access'" class="min-w-full divide-y divide-gray-200">
        <thead class="bg-indigo-50/50">
          <tr>
            <th class="px-6 py-4 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Log ID</th>
            <th class="px-6 py-4 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">User</th>
            <th class="px-6 py-4 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Locker</th>
            <th class="px-6 py-4 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Action</th>
            <th class="px-6 py-4 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Time Accessed</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100 bg-white">
          <tr v-for="alog in accessLogs" :key="alog.id" class="hover:bg-gray-50 transition-colors">
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">#{{ alog.id }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ alog.username }}</td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                Locker {{ alog.locker_id }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              <span v-if="alog.action === 'opened'" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                OPENED
              </span>
              <span v-else-if="alog.action === 'unauthorized_attempt'" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
                UNAUTHORIZED ATTEMPT
              </span>
              <span v-else class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                {{ alog.action.toUpperCase() }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ formatDate(alog.timestamp) }}</td>
          </tr>
          <tr v-if="accessLogs.length === 0">
            <td colspan="5" class="px-6 py-8 text-center text-gray-500">No access logs found</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { logAPI } from '../api'
import { auth } from '../stores/auth'
import { useRouter } from 'vue-router'

const activeTab = ref('bookings')
const logs = ref([])
const accessLogs = ref([])
const loading = ref(true)
const router = useRouter()

function formatDate(dateString) {
  if (!dateString) return ''
  // SQLite CURRENT_TIMESTAMP generates UTC formats like '2026-04-09 06:18:11'
  // and JS Date parser interprets 'YYYY-MM-DD HH:MM:SS' specifically as LOCAL TIME unless specified otherwise.
  // We append 'Z' (Zulu/UTC) if not already explicitly presented, to ensure reliable timezone conversion.
  const utcDateStr = dateString.endsWith('Z') ? dateString : dateString.replace(' ', 'T') + 'Z'
  const date = new Date(utcDateStr)
  return new Intl.DateTimeFormat('en-US', {
    month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit', second: '2-digit'
  }).format(date)
}

onMounted(async () => {
  if (auth.user?.role !== 'admin') {
    router.push('/lockers')
    return
  }

  try {
    const [bookingRes, accessRes] = await Promise.all([
      logAPI.getBookingLogs(auth.user.id),
      logAPI.getAccessLogs(auth.user.id)
    ]);

    logs.value = bookingRes.data.data;
    accessLogs.value = accessRes.data.data;
  } catch (err) {
    alert(err.message || 'Failed to load logs')
  } finally {
    loading.value = false
  }
})
</script>
