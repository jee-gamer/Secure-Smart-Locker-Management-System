import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:5000',
})

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
}

export const bookingAPI = {
  book: (user_id, receiver_id, locker_id) =>
    api.post('/bookings/', { user_id, receiver_id, locker_id }),
  unbook: (user_id, locker_id) =>
    api.delete('/bookings/', { data: { user_id, locker_id } }),
  getActive: () => api.get('/bookings/get-active')
}
