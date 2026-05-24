<template>
  <div class="sky-effects" aria-hidden="true">
    <div class="starfield"></div>
    <div class="starfield starfield-secondary"></div>
    <div class="meteor-shower" id="meteor-shower" ref="meteorShower"></div>
    <div class="ambient-glow ambient-glow-left"></div>
    <div class="ambient-glow ambient-glow-right"></div>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from 'vue';

const meteorShower = ref(null);
let visibilityHandler = null;

onMounted(() => {
  if (!meteorShower.value) return;

  // 页面不可见时暂停流星动画
  visibilityHandler = () => {
    if (!meteorShower.value) return;
    meteorShower.value.style.animationPlayState = document.hidden ? 'paused' : '';
    meteorShower.value.querySelectorAll('.shooting-star').forEach(el => {
      el.style.animationPlayState = document.hidden ? 'paused' : '';
    });
  };
  document.addEventListener('visibilitychange', visibilityHandler);

  const meteorCount = window.innerWidth < 760 ? 4 : 8;
  for (let index = 0; index < meteorCount; index += 1) {
    const meteor = document.createElement("span");
    meteor.className = "shooting-star";
    meteor.style.setProperty("--left", `${55 + Math.random() * 45}%`);
    meteor.style.setProperty("--top", `${-15 + Math.random() * 35}%`);
    meteor.style.setProperty("--delay", `${Math.random() * 8}s`);
    meteor.style.setProperty("--duration", `${3.8 + Math.random() * 3.2}s`);
    meteor.style.setProperty("--tail", `${90 + Math.random() * 90}px`);
    meteor.style.setProperty("--size", `${1.6 + Math.random() * 1.8}px`);
    meteorShower.value.appendChild(meteor);
  }
});

onUnmounted(() => {
  if (visibilityHandler) {
    document.removeEventListener('visibilitychange', visibilityHandler);
  }
});
</script>

<style scoped>
/* 原有的 styles.css 中已有对应的全局类，这里不需要重复 */
</style>
