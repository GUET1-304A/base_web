<template>
  <div class="awards-page">
    <Navbar />

    <main class="awards-main">
      <!-- Loading -->
      <div v-if="loading" class="loading-state">
        <p>加载中...</p>
      </div>

      <template v-else>
        <!-- Hero -->
        <section class="awards-hero">
          <div class="hero-glow"></div>
          <h1 class="hero-title">{{ pageData.awards?.title || '比赛奖项' }}</h1>
          <p class="hero-subtitle">{{ pageData.awards?.description || '社团成员在各类比赛中获得的荣誉与成果。' }}</p>
        </section>

        <!-- Awards Grid -->
        <section v-if="awardItems.length" class="awards-section">
          <div class="awards-grid">
            <div v-for="(award, index) in awardItems" :key="index" class="award-card" @click="openDetail(award)">
              <div class="award-image-wrapper">
                <img v-if="award.image" :src="award.image" :alt="award.title" class="award-image" />
                <div v-else class="award-placeholder">
                  <span class="placeholder-icon">🏆</span>
                </div>
              </div>
              <div class="award-info">
                <h3>{{ award.title }}</h3>
                <p v-if="award.description" class="award-desc">{{ award.description }}</p>
              </div>
            </div>
          </div>
        </section>

        <section v-else class="empty-section">
          <div class="empty-state">
            <span class="empty-icon">🏆</span>
            <h2>暂无奖项记录</h2>
            <p>奖项内容将在后台添加后展示</p>
            <router-link to="/projects" class="btn-secondary">返回项目展示</router-link>
          </div>
        </section>
      </template>
    </main>

    <!-- Detail Modal -->
    <div v-if="detailItem" class="detail-modal" @click.self="closeDetail">
      <div class="detail-modal-content">
        <button class="detail-close" @click="closeDetail">×</button>
        <div class="detail-layout">
          <div v-if="detailItem.image" class="detail-image-wrap">
            <img :src="detailItem.image" :alt="detailItem.title" class="detail-image" />
          </div>
          <div class="detail-text">
            <h2>{{ detailItem.title }}</h2>
            <MarkdownRenderer v-if="detailItem.description" :text="detailItem.description" class="detail-desc" />
          </div>
        </div>
      </div>
    </div>

    <Footer />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { api } from '../services/api.js'
import Navbar from '../components/Navbar.vue'
import Footer from '../components/Footer.vue'
import MarkdownRenderer from '../components/MarkdownRenderer.vue'

const pageData = ref({})
const loading = ref(true)
const detailItem = ref(null)

const awardItems = computed(() => pageData.value.awards?.items || [])

function openDetail(award) {
  detailItem.value = award
}

function closeDetail() {
  detailItem.value = null
}

onMounted(async () => {
  try {
    const data = await api.getPage('projects')
    if (data) pageData.value = data
  } catch (error) {
    console.warn('Failed to load awards:', error)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.awards-page {
  background: var(--bg);
  min-height: 100vh;
}

.awards-main {
  padding-top: 120px;
}

/* Loading */
.loading-state {
  text-align: center;
  padding: 120px 32px;
  color: var(--muted);
  font-size: 16px;
}

/* Hero */
.awards-hero {
  max-width: 900px;
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
  height: 500px;
  background: radial-gradient(circle, rgba(121, 168, 255, 0.12) 0%, transparent 70%);
  pointer-events: none;
}

.hero-title {
  font-size: clamp(36px, 7vw, 56px);
  font-weight: 900;
  letter-spacing: -0.03em;
  margin-bottom: 16px;
}

.hero-subtitle {
  color: var(--muted);
  font-size: 18px;
  max-width: 600px;
  margin: 0 auto;
  line-height: 1.6;
}

/* Awards Grid */
.awards-section {
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 32px 100px;
}

.awards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 24px;
}

.award-card {
  background: rgba(11, 26, 46, 0.6);
  border: 1px solid var(--panel-border);
  border-radius: 16px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.award-card {
  cursor: pointer;
}

.award-card:hover {
  border-color: var(--primary);
  transform: translateY(-4px);
}

.award-image-wrapper {
  width: 100%;
  aspect-ratio: 4 / 3;
  overflow: hidden;
  background: rgba(0, 0, 0, 0.3);
}

.award-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
  display: block;
  transition: transform 0.3s;
}

.award-card:hover .award-image {
  transform: scale(1.04);
}

.award-placeholder {
  width: 100%;
  height: 100%;
  display: grid;
  place-items: center;
}

.placeholder-icon {
  font-size: 56px;
  opacity: 0.3;
}

.award-info {
  padding: 16px 20px;
}

.award-desc {
  font-size: 13px;
  color: var(--muted);
  line-height: 1.6;
  margin: 8px 0 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.award-info h3 {
  font-size: 15px;
  font-weight: 600;
  color: var(--text);
  margin: 0;
  line-height: 1.5;
}

/* Empty State */
.empty-section {
  max-width: 900px;
  margin: 0 auto;
  padding: 0 32px 100px;
}

.empty-state {
  text-align: center;
  padding: 80px 32px;
  background: rgba(11, 26, 46, 0.4);
  border: 1px solid var(--panel-border);
  border-radius: 20px;
}

.empty-icon {
  font-size: 64px;
  display: block;
  margin-bottom: 20px;
}

.empty-state h2 {
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 8px;
}

.empty-state p {
  color: var(--muted);
  font-size: 15px;
  margin-bottom: 28px;
}

/* Detail Modal */
.detail-modal {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.85);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.2s ease;
  padding: 24px;
}

.detail-modal-content {
  position: relative;
  max-width: 720px;
  width: 100%;
  max-height: 85vh;
  background: rgba(12, 24, 42, 0.96);
  border: 1px solid var(--panel-border);
  border-radius: 20px;
  /* 整个内容作为一个滚动容器，统一滚动 */
  overflow-y: auto;
}

.detail-close {
  position: sticky;
  top: 12px;
  float: right;
  margin: 12px 16px 0 0;
  background: rgba(0, 0, 0, 0.5);
  border: none;
  color: #fff;
  font-size: 22px;
  cursor: pointer;
  z-index: 10;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: grid;
  place-items: center;
  opacity: 0.8;
  transition: opacity 0.2s;
  line-height: 1;
}

.detail-close:hover {
  opacity: 1;
}

.detail-image-wrap {
  width: 100%;
  text-align: center;
  background: rgba(0, 0, 0, 0.3);
}

.detail-image {
  max-width: 100%;
  max-height: 55vh;
  width: auto;
  height: auto;
  display: block;
  margin: 0 auto;
}

.detail-text {
  padding: 8px 28px 32px;
}

.detail-text h2 {
  font-size: 20px;
  font-weight: 700;
  color: var(--text);
  margin: 0 0 14px;
}

.detail-desc {
  font-size: 15px;
  color: var(--muted);
  line-height: 1.8;
  margin: 0;
  /* 防止超长文本横向溢出 */
  overflow-wrap: break-word;
  word-break: break-word;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.btn-secondary {
  display: inline-block;
  padding: 14px 32px;
  border-radius: 999px;
  font-size: 15px;
  font-weight: 600;
  text-decoration: none;
  border: 1px solid var(--panel-border);
  color: var(--text);
  transition: all 0.2s;
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.05);
}

/* Responsive */
@media (max-width: 768px) {
  .awards-grid {
    grid-template-columns: 1fr;
  }
}
</style>
