<template>
  <header class="topbar">
    <RouterLink class="brand" :to="{ name: 'home', hash: '#home' }">
      <span class="brand-mark">XY</span>
      <span class="brand-text">星雨作坊</span>
    </RouterLink>
    <nav class="nav">
      <RouterLink :to="{ name: 'home', hash: '#about' }">社团简介</RouterLink>
      <RouterLink :to="{ name: 'home', hash: '#members' }">人员介绍</RouterLink>
      <RouterLink :to="{ name: 'home', hash: '#products' }">产品展示</RouterLink>
      <RouterLink :to="{ name: 'home', hash: '#open-source' }">开源精神</RouterLink>
    </nav>
    <a class="nav-cta" href="/pages/join.html">加入我们</a>
  </header>
</template>

<script setup>
</script>

<style scoped>
</style>
