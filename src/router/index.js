import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/index.html',
      redirect: '/'
    },
    {
      path: '/admin',
      name: 'admin',
      component: () => import('../views/AdminView.vue'),
      meta: { title: '管理后台 - 星雨作坊' }
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue'),
      meta: { title: '关于我们 - 星雨作坊' }
    },
    {
      path: '/members',
      name: 'members',
      component: () => import('../views/MembersView.vue'),
      meta: { title: '成员介绍 - 星雨作坊' }
    },
    {
      path: '/projects',
      name: 'projects',
      component: () => import('../views/ProjectsView.vue'),
      meta: { title: '项目展示 - 星雨作坊' }
    },
    {
      path: '/blog',
      name: 'blog',
      component: () => import('../views/BlogView.vue'),
      meta: { title: '博客动态 - 星雨作坊' }
    },
    {
      path: '/join',
      name: 'join',
      component: () => import('../views/JoinView.vue'),
      meta: { title: '加入我们 - 星雨作坊' }
    },
    {
      path: '/recruitment',
      name: 'recruitment',
      component: () => import('../views/RecruitmentView.vue'),
      meta: { title: '招新信息 - 星雨作坊' }
    },
    {
      path: '/open-source',
      name: 'open-source',
      component: () => import('../views/OpenSourceView.vue'),
      meta: { title: '开源精神 - 星雨作坊' }
    },
    {
      path: '/timeline',
      name: 'timeline',
      component: () => import('../views/TimelineView.vue'),
      meta: { title: '时间线 - 星雨作坊' }
    },
    {
      path: '/onboarding',
      name: 'onboarding',
      component: () => import('../views/OnboardingView.vue'),
      meta: { title: '新手指南 - 星雨作坊' }
    },
    {
      path: '/yuji',
      name: 'yuji',
      component: () => import('../views/YujiView.vue'),
      meta: { title: '雨记协作板 - 星雨作坊' }
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: '/'
    }
  ],
  scrollBehavior(to, from, savedPosition) {
    if (to.hash) {
      return {
        el: to.hash,
        top: 96,
        behavior: 'smooth',
      }
    }
    return { top: 0 }
  }
})

router.beforeEach((to, from, next) => {
  if (to.meta.title) {
    document.title = to.meta.title
  } else {
    document.title = '星雨作坊 - 把灵感变成作品'
  }
  next()
})

export default router
