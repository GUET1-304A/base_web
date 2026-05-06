<template>
  <div class="site-shell">
    <Navbar />

    <main>
      <section class="hero section" id="home">
        <div class="hero-copy">
          <p class="eyebrow">{{ siteConfig.hero.eyebrow }}</p>
          <h1>{{ siteConfig.hero.title }}</h1>
          <p class="hero-text">
            {{ siteConfig.hero.description }}
          </p>
          <div class="hero-actions">
            <a class="button button-primary" href="/projects">查看作品</a>
            <a class="button button-secondary" href="#about">了解社团</a>
          </div>
          <ul class="hero-stats">
            <li v-for="(stat, index) in siteConfig.hero.stats" :key="index">
              <strong>{{ stat.value }}</strong>
              <span>{{ stat.label }}</span>
            </li>
          </ul>
          <div class="hero-scroll-cue" aria-hidden="true">
            <span class="hero-scroll-line"></span>
            <span class="hero-scroll-text">Scroll To Explore</span>
          </div>
        </div>

        <div class="hero-visual" aria-hidden="true">
          <div class="orbit orbit-one"></div>
          <div class="orbit orbit-two"></div>
          <div class="orbit orbit-three"></div>
          <div class="hero-core"></div>
          <div class="signal-card">
            <p>{{ siteConfig.hero.signalCard.eyebrow }}</p>
            <strong>{{ siteConfig.hero.signalCard.title }}</strong>
            <span>{{ siteConfig.hero.signalCard.description }}</span>
          </div>
        </div>
      </section>

      <section class="section flip-section" id="about" data-reveal-section>
        <div class="section-heading flip-heading">
          <p class="eyebrow">ABOUT</p>
          <div
            style="
              display: flex;
              align-items: center;
              justify-content: space-between;
              flex-wrap: wrap;
              gap: 1rem;
              margin-bottom: 1rem;
            "
          >
            <h2>{{ siteConfig.about.title }}</h2>
            <a class="button button-secondary" href="/about" style="padding: 8px 16px; font-size: 14px"
              >了解更多</a
            >
          </div>
          <p style="margin-top: 0">
            {{ siteConfig.about.description }}
          </p>
        </div>

        <div class="about-grid">
          <article
            v-for="(item, index) in siteConfig.about.items"
            :key="index"
            class="panel flip-card"
            :style="aboutCardStyle(index)"
          >
            <h3>{{ item.title }}</h3>
            <p>
              {{ item.description }}
            </p>
          </article>
        </div>
      </section>

      <section class="section flip-section" id="members" data-reveal-section>
        <div class="section-heading flip-heading">
          <p class="eyebrow">MEMBERS</p>
          <div
            style="
              display: flex;
              align-items: center;
              justify-content: space-between;
              flex-wrap: wrap;
              gap: 1rem;
              margin-bottom: 1rem;
            "
          >
            <h2>{{ siteConfig.members.title }}</h2>
            <a class="button button-secondary" href="/members" style="padding: 8px 16px; font-size: 14px"
              >了解更多</a
            >
          </div>
          <p style="margin-top: 0">{{ siteConfig.members.description }}</p>
        </div>

        <div class="members-grid">
          <article
            v-for="(group, index) in siteConfig.members.groups"
            :key="index"
            class="member-card flip-card"
            :style="membersCardStyle(index)"
          >
            <span class="member-tag">{{ group.tag }}</span>
            <h3>{{ group.name }}</h3>
            <p>
              {{ group.description }}
            </p>
          </article>
        </div>
      </section>

      <section class="section flip-section" id="products" data-reveal-section>
        <div class="section-heading flip-heading">
          <p class="eyebrow">PROJECTS</p>
          <div
            style="
              display: flex;
              align-items: center;
              justify-content: space-between;
              flex-wrap: wrap;
              gap: 1rem;
              margin-bottom: 1rem;
            "
          >
            <h2>{{ siteConfig.products?.title || '产品展示' }}</h2>
            <a class="button button-secondary" href="/projects" style="padding: 8px 16px; font-size: 14px"
              >查看全部</a
            >
          </div>
          <p style="margin-top: 0">{{ siteConfig.products?.description || '' }}</p>
        </div>

        <!-- 精选项目 -->
        <div class="featured-row">
          <component
            v-for="(project, index) in featuredProjects"
            :key="project.slug || index"
            :is="project.slug ? 'router-link' : (project.link ? 'a' : 'article')"
            class="featured-card flip-card"
            :style="`--delay: ${0.08 + index * 0.1}s`"
            :to="project.slug ? `/project/${project.slug}` : undefined"
            :href="!project.slug ? (project.link || undefined) : undefined"
          >
            <div :class="['featured-cover', project.coverClass || 'aurora']">
              <img
                v-if="project.coverImage"
                :src="project.coverImage"
                :alt="project.name"
                class="featured-cover-image"
              />
              <div class="featured-cover-overlay"></div>
              <span class="featured-badge">精选</span>
            </div>
            <div class="featured-body">
              <span class="featured-category">{{ project.category }}</span>
              <h3>{{ project.name }}</h3>
              <p>{{ project.description }}</p>
              <div v-if="project.techStack?.length" class="featured-tech">
                <span v-for="(tech, tIndex) in project.techStack.slice(0, 4)" :key="tIndex">{{ tech }}</span>
              </div>
            </div>
          </component>
        </div>
      </section>

      <section class="section flip-section" id="open-source" data-reveal-section>
        <div class="section-heading flip-heading">
          <p class="eyebrow">OPEN SOURCE</p>
          <div
            style="
              display: flex;
              align-items: center;
              justify-content: space-between;
              flex-wrap: wrap;
              gap: 1rem;
              margin-bottom: 1rem;
            "
          >
            <h2>{{ siteConfig.openSource?.title || '开源精神' }}</h2>
            <div style="display: flex; gap: 0.75rem; flex-wrap: wrap">
              <a class="button button-secondary" href="/blog" style="padding: 8px 16px; font-size: 14px"
                >博客动态</a
              >
              <a class="button button-secondary" href="/open-source" style="padding: 8px 16px; font-size: 14px"
                >了解更多</a
              >
            </div>
          </div>
          <p style="margin-top: 0">{{ siteConfig.openSource?.description || '' }}</p>
        </div>

        <div class="open-grid">
          <article 
            v-for="(item, index) in (siteConfig.openSource?.items || [])"
            :key="index"
            class="panel flip-card" 
            :style="openSourceCardStyle(index)"
          >
            <h3>{{ item.title }}</h3>
            <p>{{ item.description }}</p>
          </article>
        </div>

        <div class="open-banner flip-card" id="join" style="--delay: 0.34s; --tilt: 4deg">
          <div>
            <p class="eyebrow">{{ siteConfig.openSource?.joinBanner?.eyebrow || 'JOIN US' }}</p>
            <h3>{{ siteConfig.openSource?.joinBanner?.title || '欢迎加入星雨作坊。' }}</h3>
          </div>
          <div class="hero-actions" style="margin-top: 0">
            <a 
              class="button button-primary" 
              :href="siteConfig.openSource?.joinBanner?.primaryButton?.link || '/join'"
            >{{ siteConfig.openSource?.joinBanner?.primaryButton?.text || '加入我们' }}</a>
            <a 
              class="button button-secondary" 
              :href="siteConfig.openSource?.joinBanner?.secondaryButton?.link || '/recruitment'"
            >{{ siteConfig.openSource?.joinBanner?.secondaryButton?.text || '招新信息' }}</a>
          </div>
        </div>
      </section>
    </main>

    <Footer :config="siteConfig.footer" />
  </div>
</template>

<script setup>
import { ref, computed, nextTick } from 'vue'
import gsap from 'gsap'
import ScrollTrigger from 'gsap/ScrollTrigger'
import Navbar from '../components/Navbar.vue'
import Footer from '../components/Footer.vue'
import { useGsapAnimations } from '../composables/useGsapAnimations.js'
import { defaultSiteConfig } from '../data/defaultConfig.js'
import { api } from '../services/api.js'

const siteConfig = ref(defaultSiteConfig)
const projectsData = ref([])

const featuredProjects = computed(() =>
  projectsData.value.filter(p => p.featured)
)

const aboutCardStyle = (index) => {
  const delays = [0.06, 0.16, 0.26]
  const tilts = [-7, 0, 7]
  const delay = delays[index % delays.length] ?? 0.06
  const tilt = tilts[index % tilts.length] ?? 0
  return `--delay: ${delay}s; --tilt: ${tilt}deg;`
}

const membersCardStyle = (index) => {
  const delays = [0.04, 0.12, 0.2, 0.28]
  const tilts = [-8, -3, 3, 8]
  const delay = delays[index % delays.length] ?? 0.04
  const tilt = tilts[index % tilts.length] ?? 0
  return `--delay: ${delay}s; --tilt: ${tilt}deg;`
}

const openSourceCardStyle = (index) => {
  const delays = [0.06, 0.16, 0.26]
  const tilts = [-7, 0, 7]
  const delay = delays[index % delays.length] ?? 0.06
  const tilt = tilts[index % tilts.length] ?? 0
  return `--delay: ${delay}s; --tilt: ${tilt}deg;`
}

useGsapAnimations()

api.getSiteConfig().then((config) => {
  if (config) siteConfig.value = config
})

api.getPage('projects').then((data) => {
  if (data?.projects) projectsData.value = data.projects
  nextTick(() => {
    gsap.registerPlugin(ScrollTrigger)
    const section = document.querySelector('#products')
    if (!section) return
    const cards = section.querySelectorAll('.featured-card')
    cards.forEach((card, index) => {
      gsap.fromTo(card,
        { yPercent: 18, opacity: 0, rotateX: 26, filter: 'blur(12px)', transformOrigin: '50% 0' },
        { yPercent: 0, opacity: 1, rotateX: 0, filter: 'blur(0px)', duration: 0.9, ease: 'power3.out', delay: 0.15 + index * 0.1 }
      )
    })
  })
})
</script>

<style scoped>
/* ===== 精选项目横排 ===== */
.featured-row {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}

.featured-card {
  display: flex;
  flex-direction: column;
  background: rgba(11, 26, 46, 0.6);
  border: 1px solid var(--panel-border);
  border-radius: 18px;
  overflow: hidden;
  text-decoration: none;
  transition: all 0.35s ease;
}

.featured-card:hover {
  border-color: var(--primary);
  transform: translateY(-4px);
  box-shadow: 0 16px 36px rgba(0, 0, 0, 0.3);
}

.featured-cover {
  position: relative;
  min-height: 220px;
  flex-shrink: 0;
  overflow: hidden;
}

.featured-cover-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.featured-cover-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(5, 14, 28, 0.85) 0%, transparent 60%);
}

.featured-badge {
  position: absolute;
  top: 14px;
  right: 14px;
  padding: 5px 14px;
  background: rgba(255, 215, 0, 0.9);
  color: #1a1a1a;
  border-radius: 999px;
  font-size: 11px;
  font-weight: 700;
  z-index: 2;
}

.featured-cover.aurora {
  background: linear-gradient(135deg, #4a90e2 0%, #67b26f 100%);
}

.featured-cover.meteor {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.featured-cover.nebula {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.featured-cover.cosmos {
  background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
}

.featured-cover.pulse {
  background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%);
}

.featured-cover.horizon {
  background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
}

.featured-body {
  padding: 22px 24px 26px;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.featured-category {
  display: inline-block;
  width: fit-content;
  padding: 4px 12px;
  background: rgba(121, 168, 255, 0.12);
  border-radius: 999px;
  font-size: 11px;
  font-weight: 600;
  color: var(--primary);
  margin-bottom: 10px;
}

.featured-body h3 {
  font-size: 22px;
  font-weight: 700;
  color: var(--text);
  margin: 0 0 8px;
  line-height: 1.3;
}

.featured-body p {
  color: var(--muted);
  font-size: 14px;
  line-height: 1.6;
  flex: 1;
  margin: 0;
}

.featured-tech {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: 14px;
}

.featured-tech span {
  padding: 4px 10px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--panel-border);
  border-radius: 6px;
  font-size: 11px;
  color: var(--muted);
}

/* ===== 响应式 ===== */
@media (max-width: 1080px) {
  .featured-row {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .featured-row {
    gap: 16px;
  }

  .featured-cover {
    min-height: 180px;
  }

  .featured-body h3 {
    font-size: 20px;
  }
}
</style>
