import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const taskService = {
  getAll() {
    return api.get('/tasks')
  },

  create(taskData) {
    return api.post('/tasks', taskData)
  },

  update(taskId, taskData) {
    return api.put(`/tasks/${taskId}`, taskData)
  },

  delete(taskId) {
    return api.delete(`/tasks/${taskId}`)
  },
}