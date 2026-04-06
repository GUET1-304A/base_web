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
          <h2>{{ siteConfig.products?.title || '产品展示' }}</h2>
          <p>{{ siteConfig.products?.description || '' }}</p>
        </div>

        <div class="product-tabs flip-toolbar" role="tablist" aria-label="产品分类">
          <button 
            v-for="(category, index) in (siteConfig.products?.categories || [])"
            :key="index"
            :class="['tab-button', { active: activeProductSlide === index }]" 
            type="button" 
            @click="setProductSlide(index)"
          >
            {{ category }}
          </button>
        </div>

        <div class="product-stage flip-card" style="--delay: 0.18s; --tilt: 4deg">
          <div class="product-stage-head">
            <div class="product-stage-caption">
              <p class="eyebrow">SLIDE MODE</p>
              <h3>像翻阅作品集一样查看项目章节</h3>
            </div>
            <div class="product-nav">
              <button class="carousel-button" type="button" aria-label="上一页" @click="prevProductSlide">←</button>
              <button class="carousel-button" type="button" aria-label="下一页" @click="nextProductSlide">→</button>
            </div>
          </div>

          <div class="product-slider">
            <div class="product-track">
              <article 
                v-for="(slide, sIndex) in (siteConfig.products?.slides || [])"
                :key="sIndex"
                :class="['product-slide', { 'is-active': activeProductSlide === sIndex }]" 
                :data-slide-index="sIndex"
              >
                <div class="product-story panel">
                  <span class="product-story-tag">{{ slide.tag }}</span>
                  <h3>{{ slide.title }}</h3>
                  <p>{{ slide.description }}</p>
                  <ul v-if="slide.metrics?.length" class="product-story-metrics">
                    <li v-for="(metric, mIndex) in slide.metrics" :key="mIndex">
                      <strong>{{ metric.value }}</strong>
                      <span>{{ metric.label }}</span>
                    </li>
                  </ul>
                </div>
                <div :class="['product-page-grid', { 'product-page-grid-trio': slide.projects?.length >= 3 }]">
                  <component 
                    v-for="(project, pIndex) in slide.projects" 
                    :key="pIndex"
                    :is="project.link ? 'a' : 'article'"
                    class="product-card" 
                    :href="project.link || undefined"
                  >
                    <div :class="['product-cover', project.coverClass || 'aurora']">
                      <img
                        v-if="project.coverImage"
                        :src="project.coverImage"
                        :alt="project.name"
                        class="product-cover-image"
                      />
                    </div>
                    <div class="product-body">
                      <span>{{ project.category }}</span>
                      <h3>{{ project.name }}</h3>
                      <p>{{ project.description }}</p>
                    </div>
                  </component>
                </div>
              </article>
            </div>
          </div>

          <div class="product-dots" aria-label="产品章节分页">
            <button
              v-for="(_, index) in (siteConfig.products?.slides || [])"
              :key="index"
              :class="['product-dot', { 'is-active': activeProductSlide === index }]"
              type="button"
              :aria-label="`切换到第 ${index + 1} 个章节`"
              @click="setProductSlide(index)"
            ></button>
          </div>
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
import { ref, computed } from 'vue'
import Navbar from '../components/Navbar.vue'
import Footer from '../components/Footer.vue'
import { useGsapAnimations } from '../composables/useGsapAnimations.js'
import { defaultSiteConfig } from '../data/defaultConfig.js'
import { api } from '../services/api.js'

const siteConfig = ref(defaultSiteConfig)
const activeProductSlide = ref(0)

const slidesCount = computed(() => siteConfig.value.products?.slides?.length || 4)

const setProductSlide = (index) => {
  const count = slidesCount.value
  const normalized = ((index % count) + count) % count
  activeProductSlide.value = normalized
}

const nextProductSlide = () => {
  setProductSlide(activeProductSlide.value + 1)
}

const prevProductSlide = () => {
  setProductSlide(activeProductSlide.value - 1)
}

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
</script>
