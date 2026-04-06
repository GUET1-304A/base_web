<template>
  <div class="blog-page">
    <Navbar />
    
    <main class="blog-main">
      <section class="blog-hero">
        <div class="hero-glow"></div>
        <span class="hero-eyebrow">{{ pageData.hero?.eyebrow || '数字纪事' }}</span>
        <h1 class="hero-title">{{ pageData.hero?.title || '博客与动态' }}</h1>
        <p class="hero-subtitle">{{ pageData.hero?.subtitle || '分享我们的技术探索、设计思考和社团故事。' }}</p>
      </section>

      <section class="categories-section">
        <div class="categories-container">
          <button 
            v-for="cat in (pageData.categories || defaultCategories)" 
            :key="cat"
            :class="['category-btn', { active: activeCategory === cat }]"
            @click="activeCategory = cat"
          >
            {{ cat }}
          </button>
        </div>
      </section>

      <section class="posts-section">
        <div class="posts-container">
          <component 
            v-for="(post, index) in filteredPosts" 
            :key="index"
            :is="post.link ? 'a' : 'article'"
            class="post-card"
            :href="post.link || undefined"
            :target="isExternalLink(post.link) ? '_blank' : undefined"
            :rel="isExternalLink(post.link) ? 'noreferrer' : undefined"
          >
            <div class="post-meta">
              <span class="post-category">{{ post.category }}</span>
              <span class="post-date">{{ post.date }}</span>
            </div>
            <h2>{{ post.title }}</h2>
            <p>{{ post.excerpt }}</p>
            <div class="post-footer">
              <span class="read-time">{{ post.readTime }}</span>
              <span class="read-more">阅读全文 →</span>
            </div>
          </component>
        </div>
      </section>
    </main>
    
    <Footer />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { api } from '../services/api.js'
import Navbar from '../components/Navbar.vue'
import Footer from '../components/Footer.vue'

const pageData = ref({})
const activeCategory = ref('全部')

const defaultCategories = ['全部', '技术', '设计', '开源', '活动']

const defaultPosts = [
  { title: '2024 年度技术栈回顾', excerpt: '回顾我们这一年采用的技术选型和实践经验', category: '技术', date: '2024-12-15', readTime: '8 分钟' },
  { title: '从零搭建设计系统', excerpt: '分享我们如何为社团项目建立统一的设计语言', category: '设计', date: '2024-11-20', readTime: '12 分钟' },
  { title: '开源协作的最佳实践', excerpt: '我们在开源项目中总结的协作流程与规范', category: '开源', date: '2024-10-08', readTime: '6 分钟' }
]

const filteredPosts = computed(() => {
  const posts = pageData.value.posts || defaultPosts
  if (activeCategory.value === '全部') return posts
  return posts.filter(p => p.category === activeCategory.value)
})

function isExternalLink(link) {
  return typeof link === 'string' && /^https?:\/\//i.test(link)
}

onMounted(async () => {
  try {
    const data = await api.getPage('blog')
    if (data) pageData.value = data
  } catch (error) {
    console.warn('Failed to load blog page:', error)
  }
})
</script>

<style scoped>
.blog-page { background: var(--bg); min-height: 100vh; }
.blog-main { padding-top: 120px; }

.blog-hero {
  max-width: 1000px;
  margin: 0 auto 60px;
  padding: 0 32px;
  text-align: center;
  position: relative;
}

.hero-glow {
  position: absolute;
  top: -100px;
  left: 50%;
  transform: translateX(-50%);
  width: 100%;
  height: 400px;
  background: radial-gradient(circle, rgba(121, 168, 255, 0.1) 0%, transparent 70%);
  pointer-events: none;
}

.hero-eyebrow {
  display: block;
  color: var(--primary);
  font-size: 12px;
  font-weight: 500;
  letter-spacing: 0.4em;
  text-transform: uppercase;
  margin-bottom: 16px;
}

.hero-title {
  font-size: clamp(36px, 6vw, 56px);
  font-weight: 900;
  margin-bottom: 16px;
}

.hero-subtitle {
  color: var(--muted);
  font-size: 18px;
}

.categories-section {
  max-width: 800px;
  margin: 0 auto 48px;
  padding: 0 32px;
}

.categories-container {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  justify-content: center;
}

.category-btn {
  padding: 8px 20px;
  border: 1px solid var(--panel-border);
  border-radius: 999px;
  background: transparent;
  color: var(--muted);
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.category-btn:hover { border-color: var(--primary); color: var(--text); }
.category-btn.active { background: var(--primary); border-color: var(--primary); color: #04101f; }

.posts-section {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 32px 120px;
}

.posts-container {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.post-card {
  padding: 32px;
  background: rgba(11, 26, 46, 0.6);
  border: 1px solid var(--panel-border);
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.3s;
}

.post-card:hover {
  border-color: var(--primary);
  transform: translateX(8px);
}

.post-meta {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 16px;
}

.post-category {
  padding: 4px 12px;
  background: rgba(121, 168, 255, 0.15);
  border-radius: 999px;
  font-size: 12px;
  color: var(--primary);
}

.post-date {
  color: var(--muted);
  font-size: 13px;
}

.post-card h2 {
  font-size: 22px;
  font-weight: 700;
  margin-bottom: 12px;
}

.post-card p {
  color: var(--muted);
  font-size: 15px;
  line-height: 1.6;
  margin-bottom: 20px;
}

.post-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.read-time { color: var(--muted); font-size: 13px; }
.read-more { color: var(--primary); font-size: 14px; font-weight: 500; }
</style>
