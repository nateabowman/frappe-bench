import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'
import VueApexCharts from 'vue-apexcharts'
import App from './App.vue'
import './index.css'

// Router configuration
const router = createRouter({
  history: createWebHistory('/field/'),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: () => import('./pages/Home.vue'),
    },
    {
      path: '/daily-log',
      name: 'DailyLog',
      component: () => import('./pages/DailyLog.vue'),
    },
    {
      path: '/daily-log/:id',
      name: 'DailyLogDetail',
      component: () => import('./pages/DailyLogDetail.vue'),
    },
    {
      path: '/punch-list',
      name: 'PunchList',
      component: () => import('./pages/PunchList.vue'),
    },
    {
      path: '/punch-list/:id',
      name: 'PunchListDetail',
      component: () => import('./pages/PunchListDetail.vue'),
    },
    {
      path: '/inspection',
      name: 'Inspection',
      component: () => import('./pages/Inspection.vue'),
    },
    {
      path: '/job-sites',
      name: 'JobSites',
      component: () => import('./pages/JobSites.vue'),
    },
    {
      path: '/job-site/:id',
      name: 'JobSiteDetail',
      component: () => import('./pages/JobSiteDetail.vue'),
    },
  ],
})

const pinia = createPinia()
const app = createApp(App)

app.use(pinia)
app.use(router)
app.component('apexchart', VueApexCharts)
app.mount('#app')

// Register service worker for PWA
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/field/sw.js').catch(console.error)
}
