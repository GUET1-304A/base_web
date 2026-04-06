<template>
  <footer class="footer">
    <p>{{ config?.brand || '星雨作坊 Xingyu Studio' }}</p>
    <p>{{ config?.slogan || '以协作连接灵感，以开源延续成长。' }}</p>
  </footer>
</template>

<script setup>
defineProps({
  config: {
    type: Object,
    default: () => ({})
  }
})
</script>

<style scoped>
</style>
