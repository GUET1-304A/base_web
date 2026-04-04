import gsap from 'gsap'
import ScrollTrigger from 'gsap/ScrollTrigger'
import { onMounted, onUnmounted } from 'vue'

export function useGsapAnimations() {
  let ctx = null

  onMounted(() => {
    gsap.registerPlugin(ScrollTrigger)
    
    ctx = gsap.context(() => {
      const heroSection = document.querySelector("#home")
      const revealSections = document.querySelectorAll("[data-reveal-section]")

      // ScrollSpy for navbar
      const navLinks = document.querySelectorAll(".nav a[href^='#']")
      navLinks.forEach((link) => {
        const href = link.getAttribute("href")
        if (!href || href === "#") return
        const target = document.querySelector(href)
        if (!target) return

        ScrollTrigger.create({
          trigger: target,
          start: "top 45%",
          end: "bottom 45%",
          onToggle: (self) => {
            link.classList.toggle("is-active", self.isActive)
          },
        })
      })

      if (heroSection) {
        const heroChildren = gsap.utils.toArray(".hero-copy > *")
        gsap.from(heroChildren, {
          opacity: 0,
          y: 56,
          rotateX: 8,
          transformOrigin: "50% 0",
          duration: 1.05,
          stagger: 0.09,
          ease: "power3.out",
          delay: 0.12,
        })

        gsap.from(".hero-visual", {
          opacity: 0,
          scale: 0.9,
          y: 40,
          duration: 1.2,
          ease: "power3.out",
          delay: 0.08,
        })

        gsap.timeline({
          scrollTrigger: {
            trigger: heroSection,
            start: "top top",
            end: "bottom top",
            scrub: 1.25,
            invalidateOnRefresh: true,
          },
        })
        .to(".hero-copy", {
          y: -96,
          opacity: 0.28,
          rotateX: -14,
          transformOrigin: "50% 0%",
          ease: "none",
        }, 0)
        .to(".hero-visual", {
          y: 110,
          scale: 0.88,
          opacity: 0.42,
          rotateX: 8,
          transformOrigin: "50% 100%",
          ease: "none",
        }, 0)
      }

      revealSections.forEach((section) => {
        const heading = section.querySelector(".flip-heading")
        const toolbar = section.querySelector(".flip-toolbar")
        const cards = section.querySelectorAll(".flip-card")

        // 避免重复添加 edge
        if (!section.querySelector(".page-flip-edge")) {
          const pageEdge = document.createElement("div")
          pageEdge.className = "page-flip-edge"
          pageEdge.setAttribute("aria-hidden", "true")
          section.insertBefore(pageEdge, section.firstChild)
        }
        
        const pageEdge = section.querySelector(".page-flip-edge")

        ScrollTrigger.create({
          trigger: section,
          start: "top 78%",
          onEnter: () => section.classList.add("is-visible"),
          once: true,
        })

        const timeline = gsap.timeline({
          scrollTrigger: {
            trigger: section,
            start: "top 90%",
            end: "top 28%",
            scrub: 1.35,
            invalidateOnRefresh: true,
          },
        })

        timeline.fromTo(pageEdge, 
          { rotateX: 105, opacity: 0, scaleY: 0.2, transformOrigin: "50% 100%" },
          { rotateX: 48, opacity: 0.5, scaleY: 1, ease: "none" }, 0
        )

        if (heading) {
          timeline.fromTo(heading,
            { yPercent: 22, opacity: 0, rotateX: 22, rotateY: -12, filter: "blur(14px)", transformOrigin: "0% 0%" },
            { yPercent: 0, opacity: 1, rotateX: 0, rotateY: 0, filter: "blur(0px)", ease: "none" }, 0
          )
        }

        if (toolbar) {
          timeline.fromTo(toolbar,
            { yPercent: 16, opacity: 0, rotateX: 16, filter: "blur(10px)", transformOrigin: "50% 0" },
            { yPercent: 0, opacity: 1, rotateX: 0, filter: "blur(0px)", ease: "none" }, 0.06
          )
        }

        cards.forEach((card, index) => {
          const tiltMatch = card.style.getPropertyValue("--tilt").trim()
          const rotateYFrom = tiltMatch ? parseFloat(tiltMatch) : 0

          timeline.fromTo(card,
            { yPercent: 18, opacity: 0, rotateX: 26, rotateY: rotateYFrom * 0.65, filter: "blur(12px)", transformOrigin: "50% 0" },
            { yPercent: 0, opacity: 1, rotateX: 0, rotateY: 0, filter: "blur(0px)", ease: "none" }, 0.12 + index * 0.07
          )
        })
      })
      
      // Request refresh
      setTimeout(() => {
        ScrollTrigger.refresh()
      }, 100)
    })
  })

  onUnmounted(() => {
    if (ctx) {
      ctx.revert() // 自动清理 ScrollTrigger 和动画
    }
  })
}
