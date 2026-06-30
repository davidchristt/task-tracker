<script setup>
import TaskList from './components/TaskList.vue'
</script>

<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="max-w-2xl mx-auto px-4">
      <header class="mb-8">
        <h1 class="text-3xl font-bold text-gray-800">Task Tracker</h1>
        <p class="text-gray-600 mt-1">Manage your tasks efficiently</p>
      </header>

      <TaskList />
    </div>
  </div>
</template>