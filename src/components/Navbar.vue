<template>
  <header class="topbar" ref="topbarEl">
    <RouterLink class="brand" :to="{ name: 'home', hash: '#home' }">
      <img v-if="siteIcon" :src="siteIcon" alt="logo" class="brand-icon" />
      <span v-else class="brand-mark">XY</span>
      <span class="brand-text">星雨作坊</span>
    </RouterLink>
    <nav class="nav">
      <RouterLink :to="{ name: 'home', hash: '#about' }">社团简介</RouterLink>
      <RouterLink to="/members">成员</RouterLink>
      <RouterLink to="/projects">作品</RouterLink>
      <RouterLink to="/blog">博客</RouterLink>
      <RouterLink :to="{ name: 'home', hash: '#open-source' }">开源精神</RouterLink>
    </nav>
    <a class="nav-cta" href="/join">加入我们</a>
  </header>
</template>

<script setup>
import { onBeforeUnmount, onMounted, ref } from 'vue'
import { api } from '../services/api.js'

const topbarEl = ref(null)
const siteIcon = ref('')

api.getSiteConfig().then((config) => {
  if (config?.system?.siteIcon) siteIcon.value = config.system.siteIcon
})

let ticking = false

function onScroll() {
  if (ticking) return
  ticking = true
  requestAnimationFrame(() => {
    if (!topbarEl.value) { ticking = false; return }
    const progress = Math.min(window.scrollY / 520, 1)
    topbarEl.value.style.opacity = String(1 - progress * 0.28)
    topbarEl.value.style.background = `rgba(8, 16, 30, ${0.7 - progress * 0.22})`
    ticking = false
  })
}

onMounted(() => {
  onScroll()
  window.addEventListener('scroll', onScroll, { passive: true })
})

onBeforeUnmount(() => {
  window.removeEventListener('scroll', onScroll)
})
</script>

<style scoped>
.topbar {
  transition: opacity 0.18s linear, background 0.18s linear;
}

.brand-icon {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  object-fit: cover;
}
</style>
