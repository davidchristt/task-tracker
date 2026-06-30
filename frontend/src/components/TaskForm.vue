<script setup>
import { ref } from 'vue'
import { taskService } from '../services/taskService'

const emit = defineEmits(['task-created'])

const title = ref('')
const description = ref('')
const status = ref('Todo')
const submitting = ref(false)
const error = ref(null)

async function handleSubmit() {
  if (!title.value.trim()) {
    error.value = 'Title is required'
    return
  }

  submitting.value = true
  error.value = null

  try {
    const response = await taskService.create({
      title: title.value.trim(),
      description: description.value.trim() || null,
      status: status.value,
    })

    emit('task-created', response.data)

    title.value = ''
    description.value = ''
    status.value = 'Todo'
  } catch (err) {
    error.value = 'Failed to create task'
    console.error(err)
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <form @submit.prevent="handleSubmit" class="bg-white rounded-lg shadow-sm p-6 border border-gray-200 mb-6">
    <h2 class="text-lg font-semibold text-gray-800 mb-4">Add New Task</h2>

    <div class="space-y-3">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Title</label>
        <input
          v-model="title"
          type="text"
          maxlength="200"
          placeholder="What needs to be done?"
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Description (optional)</label>
        <textarea
          v-model="description"
          rows="2"
          placeholder="Add more details..."
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        ></textarea>
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Status</label>
        <select
          v-model="status"
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="Todo">Todo</option>
          <option value="In Progress">In Progress</option>
          <option value="Done">Done</option>
        </select>
      </div>

      <p v-if="error" class="text-sm text-red-600">{{ error }}</p>

      <button
        type="submit"
        :disabled="submitting"
        class="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed font-medium"
      >
        {{ submitting ? 'Creating...' : 'Add Task' }}
      </button>
    </div>
  </form>
</template>