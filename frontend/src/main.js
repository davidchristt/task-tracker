import { createApp } from 'vue'
import App from './App.vue'
import './assets/main.css'

console.log('API URL:', import.meta.env.VITE_API_URL)

createApp(App).mount('#app')

