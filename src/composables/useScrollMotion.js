import { onMounted, onUnmounted, ref } from 'vue'

export function useScrollMotion() {
  let cachedViewportHeight = 0
  let cachedHeroData = null
  let cachedSectionsData = []
  let motionTicking = false
  
  const cacheDimensions = () => {
    cachedViewportHeight = window.innerHeight || 1
    const heroSection = document.querySelector("#home")
    const revealSections = document.querySelectorAll("[data-reveal-section]")

    if (heroSection) {
      const rect = heroSection.getBoundingClientRect()
      cachedHeroData = {
        height: rect.height,
        topAbsolute: rect.top + window.scrollY,
      }
    }

    cachedSectionsData = Array.from(revealSections).map((section) => {
      const rect = section.getBoundingClientRect()
      return {
        height: rect.height,
        topAbsolute: rect.top + window.scrollY,
      }
    })
  }

  const updateScrollMotion = () => {
    const scrollY = window.scrollY
    const root = document.documentElement

    // --- 1. Calculations based on cache ---
    let heroProgressVal = null
    if (cachedHeroData) {
      const heroTop = cachedHeroData.topAbsolute - scrollY
      const heroRange = Math.max(cachedHeroData.height * 0.72, 1)
      heroProgressVal = Math.min(Math.max(-heroTop / heroRange, 0), 1).toFixed(4)
    }

    const sectionsData = cachedSectionsData.map((data) => {
      const sectionTop = data.topAbsolute - scrollY
      const distanceFromCenter = sectionTop + data.height / 2 - cachedViewportHeight / 2
      const progress = Math.min(Math.max(distanceFromCenter / cachedViewportHeight, -1), 1).toFixed(4)
      const distance = Math.abs(distanceFromCenter)
      return { progress, distance }
    })

    // --- 2. State Calculation ---
    let activeSectionIndex = -1
    let closestDistance = Number.POSITIVE_INFINITY

    sectionsData.forEach((data, index) => {
      if (data.distance < closestDistance) {
        closestDistance = data.distance
        activeSectionIndex = index
      }
    })

    // --- 3. DOM Writes ---
    if (heroProgressVal !== null) {
      root.style.setProperty("--hero-progress", heroProgressVal)
    }

    const revealSections = document.querySelectorAll("[data-reveal-section]")
    revealSections.forEach((section, index) => {
      const data = sectionsData[index]
      if (data) {
        section.style.setProperty("--section-progress", data.progress)
        section.classList.toggle("is-active-section", index === activeSectionIndex)
        section.classList.toggle("is-dimmed", activeSectionIndex > -1 && index < activeSectionIndex)
      }
    })
  }

  const requestMotionUpdate = () => {
    if (motionTicking) return
    motionTicking = true
    window.requestAnimationFrame(() => {
      updateScrollMotion()
      motionTicking = false
    })
  }

  const onResize = () => {
    cacheDimensions()
    requestMotionUpdate()
  }

  onMounted(() => {
    setTimeout(() => {
      cacheDimensions()
      updateScrollMotion()
    }, 100)
    
    window.addEventListener("scroll", requestMotionUpdate, { passive: true })
    window.addEventListener("resize", onResize)
  })

  onUnmounted(() => {
    window.removeEventListener("scroll", requestMotionUpdate)
    window.removeEventListener("resize", onResize)
  })
}
