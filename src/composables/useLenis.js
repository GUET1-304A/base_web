import Lenis from 'lenis'
import gsap from 'gsap'
import ScrollTrigger from 'gsap/ScrollTrigger'
import { onMounted, onUnmounted } from 'vue'

export function useLenis() {
  let lenisInstance = null
  let rafId = null

  onMounted(() => {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return

    document.documentElement.classList.add("lenis-smooth")

    lenisInstance = new Lenis({
      duration: 1.15,
      easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
      smoothWheel: true,
    })

    gsap.registerPlugin(ScrollTrigger)
    lenisInstance.on("scroll", ScrollTrigger.update)

    gsap.ticker.add((time) => {
      lenisInstance.raf(time * 1000)
    })
    gsap.ticker.lagSmoothing(0)
  })

  onUnmounted(() => {
    if (lenisInstance) {
      lenisInstance.destroy()
      lenisInstance = null
    }
    gsap.ticker.remove(lenisInstance?.raf)
  })

  return { lenisInstance }
}
