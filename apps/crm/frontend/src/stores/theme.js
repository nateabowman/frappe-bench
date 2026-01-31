import { useStorage } from '@vueuse/core'
import { watch } from 'vue'

export const theme = useStorage('theme', 'light')
export const glassmorphismEnabled = useStorage('glassmorphism-enabled', true)

// Glassmorphism theme variables
const glassThemeVars = {
  light: {
    '--glass-bg': 'rgba(255, 255, 255, 0.7)',
    '--glass-bg-hover': 'rgba(255, 255, 255, 0.85)',
    '--glass-bg-active': 'rgba(255, 255, 255, 0.9)',
    '--glass-bg-subtle': 'rgba(255, 255, 255, 0.5)',
    '--glass-bg-strong': 'rgba(255, 255, 255, 0.9)',
    '--glass-border': 'rgba(255, 255, 255, 0.18)',
    '--glass-border-hover': 'rgba(255, 255, 255, 0.25)',
    '--glass-border-subtle': 'rgba(255, 255, 255, 0.1)',
    '--glass-shadow': '0 8px 32px 0 rgba(31, 38, 135, 0.37)',
    '--glass-shadow-sm': '0 4px 16px 0 rgba(31, 38, 135, 0.2)',
    '--glass-shadow-lg': '0 12px 48px 0 rgba(31, 38, 135, 0.5)',
    '--glass-overlay': 'rgba(0, 0, 0, 0.1)',
    '--glass-overlay-dark': 'rgba(0, 0, 0, 0.3)'
  },
  dark: {
    '--glass-bg': 'rgba(30, 30, 30, 0.7)',
    '--glass-bg-hover': 'rgba(30, 30, 30, 0.85)',
    '--glass-bg-active': 'rgba(30, 30, 30, 0.9)',
    '--glass-bg-subtle': 'rgba(30, 30, 30, 0.5)',
    '--glass-bg-strong': 'rgba(30, 30, 30, 0.9)',
    '--glass-border': 'rgba(255, 255, 255, 0.1)',
    '--glass-border-hover': 'rgba(255, 255, 255, 0.18)',
    '--glass-border-subtle': 'rgba(255, 255, 255, 0.05)',
    '--glass-shadow': '0 8px 32px 0 rgba(0, 0, 0, 0.5)',
    '--glass-shadow-sm': '0 4px 16px 0 rgba(0, 0, 0, 0.3)',
    '--glass-shadow-lg': '0 12px 48px 0 rgba(0, 0, 0, 0.7)',
    '--glass-overlay': 'rgba(0, 0, 0, 0.3)',
    '--glass-overlay-dark': 'rgba(0, 0, 0, 0.6)'
  }
}

function applyGlassTheme(themeValue) {
  const root = document.documentElement
  const vars = glassThemeVars[themeValue] || glassThemeVars.light
  
  Object.entries(vars).forEach(([key, value]) => {
    root.style.setProperty(key, value)
  })
}

export function toggleTheme() {
  const currentTheme = document.documentElement.getAttribute('data-theme')
  theme.value = currentTheme === 'dark' ? 'light' : 'dark'
  document.documentElement.setAttribute('data-theme', theme.value)
  if (glassmorphismEnabled.value) {
    applyGlassTheme(theme.value)
  }
}

export function setTheme(value) {
  theme.value = value || theme.value
  if (['light', 'dark'].includes(theme.value)) {
    document.documentElement.setAttribute('data-theme', theme.value)
    if (glassmorphismEnabled.value) {
      applyGlassTheme(theme.value)
    }
  }
}

export function toggleGlassmorphism() {
  glassmorphismEnabled.value = !glassmorphismEnabled.value
  if (glassmorphismEnabled.value) {
    applyGlassTheme(theme.value)
    document.documentElement.classList.add('glassmorphism-enabled')
  } else {
    document.documentElement.classList.remove('glassmorphism-enabled')
  }
}

// Watch for theme changes and apply glass variables
watch(
  [theme, glassmorphismEnabled],
  () => {
    if (glassmorphismEnabled.value) {
      applyGlassTheme(theme.value)
      document.documentElement.classList.add('glassmorphism-enabled')
    } else {
      document.documentElement.classList.remove('glassmorphism-enabled')
    }
  },
  { immediate: true }
)

// Initialize on load
if (typeof document !== 'undefined') {
  const currentTheme = document.documentElement.getAttribute('data-theme') || theme.value
  setTheme(currentTheme)
  if (glassmorphismEnabled.value) {
    document.documentElement.classList.add('glassmorphism-enabled')
  }
}
