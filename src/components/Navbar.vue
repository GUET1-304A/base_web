<template>
  <header
    class="topbar"
    :style="{
      '--topbar-opacity': topbarOpacity,
      '--topbar-bg-opacity': topbarBackgroundOpacity
    }"
  >
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
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { api } from '../services/api.js'

const scrollY = ref(0)
const siteIcon = ref('')

api.getSiteConfig().then((config) => {
  if (config?.system?.siteIcon) siteIcon.value = config.system.siteIcon
})

const topbarOpacity = computed(() => {
  const progress = Math.min(scrollY.value / 520, 1)
  return String(1 - progress * 0.28)
})

const topbarBackgroundOpacity = computed(() => {
  const progress = Math.min(scrollY.value / 520, 1)
  return String(0.7 - progress * 0.22)
})

function updateScrollY() {
  scrollY.value = window.scrollY || 0
}

onMounted(() => {
  updateScrollY()
  window.addEventListener('scroll', updateScrollY, { passive: true })
})

onBeforeUnmount(() => {
  window.removeEventListener('scroll', updateScrollY)
})
</script>

<style scoped>
.topbar {
  opacity: var(--topbar-opacity, 1);
  background: rgba(8, 16, 30, var(--topbar-bg-opacity, 0.7));
  transition: opacity 0.18s linear, background 0.18s linear;
}

.brand-icon {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  object-fit: cover;
}
</style>
