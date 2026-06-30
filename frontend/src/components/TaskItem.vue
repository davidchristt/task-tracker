<script setup>
import { ref } from 'vue'
import { taskService } from '../services/taskService'

const props = defineProps({
  task: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['updated', 'deleted'])

const updating = ref(false)
const deleting = ref(false)
const isEditing = ref(false)
const editTitle = ref('')
const editDescription = ref('')
const editError = ref(null)

const statusOptions = ['Todo', 'In Progress', 'Done']

const statusStyles = {
  'Todo': 'bg-gray-100 text-gray-700 border-gray-300',
  'In Progress': 'bg-blue-100 text-blue-700 border-blue-300',
  'Done': 'bg-green-100 text-green-700 border-green-300',
}

function startEdit() {
  editTitle.value = props.task.title
  editDescription.value = props.task.description || ''
  editError.value = null
  isEditing.value = true
}

function cancelEdit() {
  isEditing.value = false
  editError.value = null
}

async function saveEdit() {
  const trimmedTitle = editTitle.value.trim()
  if (!trimmedTitle) {
    editError.value = 'Title is required'
    return
  }

  updating.value = true
  editError.value = null

  try {
    const response = await taskService.update(props.task.id, {
      title: trimmedTitle,
      description: editDescription.value.trim() || null,
    })
    emit('updated', response.data)
    isEditing.value = false
  } catch (err) {
    editError.value = 'Failed to update task'
    console.error(err)
  } finally {
    updating.value = false
  }
}

async function changeStatus(event) {
  const newStatus = event.target.value
  if (newStatus === props.task.status) return

  updating.value = true
  try {
    const response = await taskService.update(props.task.id, { status: newStatus })
    emit('updated', response.data)
  } catch (err) {
    console.error('Failed to update status:', err)
    event.target.value = props.task.status
  } finally {
    updating.value = false
  }
}

async function handleDelete() {
  if (!confirm(`Delete task "${props.task.title}"?`)) return

  deleting.value = true
  try {
    await taskService.delete(props.task.id)
    emit('deleted', props.task.id)
  } catch (err) {
    console.error('Failed to delete task:', err)
    deleting.value = false
  }
}
</script>

<template>
  <li class="bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow p-4 border border-gray-200">
    <div v-if="!isEditing">
      <div class="flex items-start justify-between gap-3 mb-3">
        <h3 class="font-semibold text-gray-800 break-words flex-1 min-w-0">
          {{ task.title }}
        </h3>
        <button
          @click="startEdit"
          :disabled="updating || deleting"
          class="text-sm text-blue-600 hover:text-blue-800 font-medium shrink-0 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Edit
        </button>
      </div>

      <p v-if="task.description" class="text-gray-600 text-sm mb-3 break-words">
        {{ task.description }}
      </p>

      <div class="flex flex-wrap items-center gap-2">
        <select
          :value="task.status"
          :disabled="updating || deleting"
          @change="changeStatus"
          :class="[
            'text-xs font-medium px-2 py-1 rounded border focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 cursor-pointer',
            statusStyles[task.status]
          ]"
        >
          <option v-for="option in statusOptions" :key="option" :value="option">
            {{ option }}
          </option>
        </select>

        <button
          @click="handleDelete"
          :disabled="updating || deleting"
          class="text-xs text-red-600 hover:text-red-800 font-medium px-2 py-1 rounded hover:bg-red-50 disabled:opacity-50 disabled:cursor-not-allowed ml-auto"
        >
          {{ deleting ? 'Deleting...' : 'Delete' }}
        </button>
      </div>
    </div>

    <div v-else class="space-y-3">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Title</label>
        <input
          v-model="editTitle"
          type="text"
          maxlength="200"
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Description</label>
        <textarea
          v-model="editDescription"
          rows="2"
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        ></textarea>
      </div>

      <p v-if="editError" class="text-sm text-red-600">{{ editError }}</p>

      <div class="flex gap-2 justify-end">
        <button
          @click="cancelEdit"
          :disabled="updating"
          class="text-sm px-4 py-2 border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50"
        >
          Cancel
        </button>
        <button
          @click="saveEdit"
          :disabled="updating"
          class="text-sm px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:bg-gray-400"
        >
          {{ updating ? 'Saving...' : 'Save' }}
        </button>
      </div>
    </div>
  </li>
</template>