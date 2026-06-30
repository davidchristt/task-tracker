<script setup>
import { ref, computed, onMounted } from 'vue'
import { taskService } from '../services/taskService'
import TaskForm from './TaskForm.vue'
import TaskItem from './TaskItem.vue'

const tasks = ref([])
const loading = ref(false)
const error = ref(null)
const showForm = ref(false)

const taskStats = computed(() => {
  return {
    total: tasks.value.length,
    todo: tasks.value.filter(t => t.status === 'Todo').length,
    inProgress: tasks.value.filter(t => t.status === 'In Progress').length,
    done: tasks.value.filter(t => t.status === 'Done').length,
  }
})

async function fetchTasks() {
  loading.value = true
  error.value = null
  try {
    const response = await taskService.getAll()
    tasks.value = response.data
  } catch (err) {
    error.value = 'Failed to load tasks'
    console.error(err)
  } finally {
    loading.value = false
  }
}

function handleTaskCreated(newTask) {
  tasks.value.unshift(newTask)
  showForm.value = false
}

function handleTaskUpdated(updatedTask) {
  const index = tasks.value.findIndex(t => t.id === updatedTask.id)
  if (index !== -1) {
    tasks.value[index] = updatedTask
  }
}

function handleTaskDeleted(taskId) {
  tasks.value = tasks.value.filter(t => t.id !== taskId)
}

function toggleForm() {
  showForm.value = !showForm.value
}

onMounted(() => {
  fetchTasks()
})
</script>

<template>
  <div>
    <div class="flex items-center justify-between mb-4">
      <div v-if="!loading && !error && tasks.length > 0" class="flex flex-wrap items-center gap-2 text-sm">
        <span class="font-medium text-gray-700">{{ taskStats.total }} tasks</span>
        <span class="text-gray-400">·</span>
        <span class="text-gray-600">{{ taskStats.todo }} Todo</span>
        <span class="text-gray-400">·</span>
        <span class="text-blue-600">{{ taskStats.inProgress }} In Progress</span>
        <span class="text-gray-400">·</span>
        <span class="text-green-600">{{ taskStats.done }} Done</span>
      </div>
      <div v-else></div>

      <button
        @click="toggleForm"
        class="flex items-center gap-1 px-3 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 font-medium text-sm shrink-0"
      >
        <span class="text-lg leading-none">{{ showForm ? '−' : '+' }}</span>
        <span>{{ showForm ? 'Cancel' : 'Add Task' }}</span>
      </button>
    </div>

    <Transition name="slide-fade">
        <TaskForm v-if="showForm" @task-created="handleTaskCreated" />
    </Transition>

    <div v-if="loading" class="text-center text-gray-500 py-8">
      Loading tasks...
    </div>

    <div v-else-if="error" class="text-center text-red-600 py-8">
      {{ error }}
    </div>

    <div v-else-if="tasks.length === 0" class="text-center py-12 bg-white rounded-lg border-2 border-dashed border-gray-300">
      <svg xmlns="http://www.w3.org/2000/svg" class="mx-auto h-12 w-12 text-gray-400 mb-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
      </svg>
      <p class="text-gray-700 font-medium">No tasks yet</p>
      <p class="text-gray-500 text-sm mt-1">Click "Add Task" above to create your first task.</p>
    </div>

    <ul v-else class="space-y-3">
      <TaskItem
        v-for="task in tasks"
        :key="task.id"
        :task="task"
        @updated="handleTaskUpdated"
        @deleted="handleTaskDeleted"
      />
    </ul>
  </div>
</template>

<style scoped>
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.25s ease;
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>