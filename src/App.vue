<template>
  <SkyEffects />
  <router-view />
</template>

<script setup>
import { onMounted } from 'vue'
import SkyEffects from './components/SkyEffects.vue'
import { api } from './services/api.js'

onMounted(async () => {
  try {
    const config = await api.getSiteConfig()
    const icon = config?.system?.siteIcon
    if (icon) {
      let link = document.querySelector("link[rel~='icon']")
      if (!link) {
        link = document.createElement('link')
        link.rel = 'icon'
        document.head.appendChild(link)
      }
      link.href = icon
    }
  } catch {}
})
</script>
