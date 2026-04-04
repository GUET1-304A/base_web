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
            <a class="button button-primary" href="/pages/projects.html">查看作品</a>
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
            <a class="button button-secondary" href="/pages/about.html" style="padding: 8px 16px; font-size: 14px"
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
            <a class="button button-secondary" href="/pages/members.html" style="padding: 8px 16px; font-size: 14px"
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
          <h2>产品展示</h2>
          <p>以下内容为官网展示模板，你后续可以替换为社团真实项目名称、截图、简介与仓库链接。</p>
        </div>

        <div class="product-tabs flip-toolbar" role="tablist" aria-label="产品分类">
          <button :class="['tab-button', { active: activeProductSlide === 0 }]" type="button" @click="setProductSlide(0)">
            精选总览
          </button>
          <button :class="['tab-button', { active: activeProductSlide === 1 }]" type="button" @click="setProductSlide(1)">
            网站平台
          </button>
          <button :class="['tab-button', { active: activeProductSlide === 2 }]" type="button" @click="setProductSlide(2)">
            效率工具
          </button>
          <button :class="['tab-button', { active: activeProductSlide === 3 }]" type="button" @click="setProductSlide(3)">
            品牌内容
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
              <article :class="['product-slide', { 'is-active': activeProductSlide === 0 }]" data-slide-index="0">
                <div class="product-story panel">
                  <span class="product-story-tag">精选总览</span>
                  <h3>从灵感、工具到传播，形成完整作品链路</h3>
                  <p>
                    星雨作坊的产品并不是孤立存在的单点项目，而是围绕真实需求持续迭代的作品群。我们希望每一项作品都能成为下一项作品的起点。
                  </p>
                  <ul class="product-story-metrics">
                    <li><strong>03</strong><span>核心章节</span></li>
                    <li><strong>06</strong><span>示例作品</span></li>
                    <li><strong>∞</strong><span>持续迭代</span></li>
                  </ul>
                </div>
                <div class="product-page-grid product-page-grid-trio">
                  <a class="product-card" href="/pages/onboarding.html">
                    <div class="product-cover aurora"></div>
                    <div class="product-body">
                      <span>网站平台</span>
                      <h3>星图导航</h3>
                      <p>为新成员与访客整理社团资讯、活动日历与学习路线的门户网站。</p>
                    </div>
                  </a>
                  <a class="product-card" href="/pages/yuji.html">
                    <div class="product-cover meteor"></div>
                    <div class="product-body">
                      <span>效率工具</span>
                      <h3>雨记协作板</h3>
                      <p>支持任务拆分、进度同步与复盘记录的轻量化协作工具。</p>
                    </div>
                  </a>
                  <a class="product-card" href="/pages/timeline.html">
                    <div class="product-cover nebula"></div>
                    <div class="product-body">
                      <span>品牌内容</span>
                      <h3>星雨年刊</h3>
                      <p>沉淀年度作品、社团故事和成员成长轨迹的数字刊物与视觉专题。</p>
                    </div>
                  </a>
                </div>
              </article>

              <article :class="['product-slide', { 'is-active': activeProductSlide === 1 }]" data-slide-index="1">
                <div class="product-story panel">
                  <span class="product-story-tag">网站平台</span>
                  <h3>把服务入口和活动体验做成可持续迭代的平台</h3>
                  <p>这一类项目强调信息组织、交互体验与系统稳定性，通常会面向成员、访客或校园用户提供长期使用的服务入口。</p>
                </div>
                <div class="product-page-grid">
                  <a class="product-card" href="/pages/onboarding.html">
                    <div class="product-cover aurora"></div>
                    <div class="product-body">
                      <span>网站平台</span>
                      <h3>星图导航</h3>
                      <p>为新成员与访客整理社团资讯、活动日历与学习路线的门户网站。</p>
                    </div>
                  </a>
                  <article class="product-card">
                    <div class="product-cover cosmos"></div>
                    <div class="product-body">
                      <span>网站平台</span>
                      <h3>活动报名系统</h3>
                      <p>用于活动预告、报名管理和数据统计，帮助组织流程更顺畅。</p>
                    </div>
                  </article>
                </div>
              </article>

              <article :class="['product-slide', { 'is-active': activeProductSlide === 2 }]" data-slide-index="2">
                <div class="product-story panel">
                  <span class="product-story-tag">效率工具</span>
                  <h3>把协作过程也设计成产品，让创作效率持续提升</h3>
                  <p>这类作品更关注成员内部的协同、记录与复盘，希望通过轻量工具减少沟通成本，让创作和执行更流畅。</p>
                </div>
                <div class="product-page-grid">
                  <a class="product-card" href="/pages/yuji.html">
                    <div class="product-cover meteor"></div>
                    <div class="product-body">
                      <span>效率工具</span>
                      <h3>雨记协作板</h3>
                      <p>支持任务拆分、进度同步与复盘记录的轻量化协作工具。</p>
                    </div>
                  </a>
                  <article class="product-card">
                    <div class="product-cover pulse"></div>
                    <div class="product-body">
                      <span>效率工具</span>
                      <h3>灵感收集箱</h3>
                      <p>面向社团成员的灵感归档空间，方便记录选题、链接和碎片创意。</p>
                    </div>
                  </article>
                </div>
              </article>

              <article :class="['product-slide', { 'is-active': activeProductSlide === 3 }]" data-slide-index="3">
                <div class="product-story panel">
                  <span class="product-story-tag">品牌内容</span>
                  <h3>让作品被看见，也让社团的成长被长久保存</h3>
                  <p>这一部分更关注视觉表达、内容包装和公开传播，让社团成果能够以更完整、更动人的方式被外界感知。</p>
                </div>
                <div class="product-page-grid">
                  <a class="product-card" href="/pages/timeline.html">
                    <div class="product-cover nebula"></div>
                    <div class="product-body">
                      <span>品牌内容</span>
                      <h3>星雨年刊</h3>
                      <p>沉淀年度作品、社团故事和成员成长轨迹的数字刊物与视觉专题。</p>
                    </div>
                  </a>
                  <a class="product-card" href="/pages/blog.html">
                    <div class="product-cover horizon"></div>
                    <div class="product-body">
                      <span>品牌内容</span>
                      <h3>开放分享计划</h3>
                      <p>将讲座回顾、教程文章和项目经验整理成公开可访问的内容合集。</p>
                    </div>
                  </a>
                </div>
              </article>
            </div>
          </div>

          <div class="product-dots" aria-label="产品章节分页">
            <button
              v-for="index in 4"
              :key="index"
              :class="['product-dot', { 'is-active': activeProductSlide === index - 1 }]"
              type="button"
              :aria-label="`切换到第 ${index} 个章节`"
              @click="setProductSlide(index - 1)"
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
            <h2>开源精神</h2>
            <a class="button button-secondary" href="/pages/open-source.html" style="padding: 8px 16px; font-size: 14px"
              >了解更多</a
            >
          </div>
          <p style="margin-top: 0">对星雨作坊来说，开源不只是把代码放出来，更是把过程、思考和经验主动分享出去。</p>
        </div>

        <div class="open-grid">
          <article class="panel flip-card" style="--delay: 0.06s; --tilt: -7deg">
            <h3>共享知识</h3>
            <p>把文档、教程、设计稿和项目复盘留下来，让后来者可以站在前人的经验上继续前进。</p>
          </article>
          <article class="panel flip-card" style="--delay: 0.16s; --tilt: 0deg">
            <h3>鼓励协作</h3>
            <p>欢迎成员互相 review、共同维护项目，也欢迎外部同学提出 issue、建议和改进方案。</p>
          </article>
          <article class="panel flip-card" style="--delay: 0.26s; --tilt: 7deg">
            <h3>持续迭代</h3>
            <p>开源意味着作品不是一次性交付，而是会随着需求、反馈与技术演进不断完善。</p>
          </article>
        </div>

        <div class="open-banner flip-card" id="join" style="--delay: 0.34s; --tilt: 4deg">
          <div>
            <p class="eyebrow">JOIN US</p>
            <h3>如果你也相信“做作品比只谈想法更重要”，欢迎加入星雨作坊。</h3>
          </div>
          <div class="hero-actions" style="margin-top: 0">
            <a class="button button-primary" href="/pages/join.html">加入我们</a>
            <a class="button button-secondary" href="/pages/recruitment.html">招新信息</a>
          </div>
        </div>
      </section>
    </main>

    <Footer />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Navbar from '../components/Navbar.vue'
import Footer from '../components/Footer.vue'
import { useGsapAnimations } from '../composables/useGsapAnimations.js'
import { useLenis } from '../composables/useLenis.js'
import { useScrollMotion } from '../composables/useScrollMotion.js'
import { defaultSiteConfig } from '../data/defaultConfig.js'
import { api } from '../services/api.js'

const siteConfig = ref(defaultSiteConfig)
const activeProductSlide = ref(0)
const setProductSlide = (index) => {
  const normalized = ((index % 4) + 4) % 4
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
  const delay = delays[index] ?? 0.06
  const tilt = tilts[index] ?? 0
  return `--delay: ${delay}s; --tilt: ${tilt}deg;`
}

const membersCardStyle = (index) => {
  const delays = [0.04, 0.12, 0.2, 0.28]
  const tilts = [-8, -3, 3, 8]
  const delay = delays[index] ?? 0.04
  const tilt = tilts[index] ?? 0
  return `--delay: ${delay}s; --tilt: ${tilt}deg;`
}

useLenis()
useGsapAnimations()
useScrollMotion()

api.getSiteConfig().then((config) => {
  if (config) siteConfig.value = config
})
</script>
