import { reactive } from 'vue'

const stored = localStorage.getItem('auth_user')

export const auth = reactive({
  user: stored ? JSON.parse(stored) : null,

  login(user) {
    this.user = user
    localStorage.setItem('auth_user', JSON.stringify(user))
  },

  logout() {
    this.user = null
    localStorage.removeItem('auth_user')
  },

  get isLoggedIn() {
    return this.user !== null
  }
})
