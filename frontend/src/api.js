import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:5000',
})

api.interceptors.response.use(
  (res) => res,
  (err) => {
    const message = err.response?.data?.error || 'Request failed'
    return Promise.reject(new Error(message))
  }
)

export const authAPI = {
  register: (username, password) =>
    api.post('/users/register', { username, password }),
  login: (username, password) =>
    api.post('/users/login', { username, password }),
  getUsers: () => api.get('/users/'),
}

export const lockerAPI = {
  getAll: () => api.get('/lockers/'),
  getOne: (id) => api.get(`/lockers/${id}`),
  getImageUrl: (locker_id, user_id) => `${api.defaults.baseURL}/lockers/${locker_id}/image/${user_id}`,
}

export const bookingAPI = {
  book: (formData) =>
    api.post('/bookings/', formData),
  unbook: (user_id, locker_id) =>
    api.delete('/bookings/', { data: { user_id, locker_id } }),
  getActive: () => api.get('/bookings/get-active')
}
