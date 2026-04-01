const tabButtons = document.querySelectorAll(".tab-button");
const heroSection = document.querySelector("#home");
const meteorShower = document.querySelector("#meteor-shower");
const revealSections = document.querySelectorAll("[data-reveal-section]");
const root = document.documentElement;
const productTrack = document.querySelector("#product-track");
const productSlides = document.querySelectorAll(".product-slide");
const productDots = document.querySelectorAll(".product-dot");
const productPrev = document.querySelector("#product-prev");
const productNext = document.querySelector("#product-next");
const productStage = document.querySelector(".product-stage");
const navLinks = document.querySelectorAll(".nav a[href^='#']");

let activeProductSlide = 0;
let lenisInstance = null;

const applyProductSlideState = (index) => {
  const totalSlides = productSlides.length;
  activeProductSlide = ((index % totalSlides) + totalSlides) % totalSlides;

  productTrack.style.setProperty("--product-index", activeProductSlide);

  productSlides.forEach((slide, slideIndex) => {
    slide.classList.toggle("is-active", slideIndex === activeProductSlide);
    slide.classList.toggle("is-past", slideIndex < activeProductSlide);
  });

  tabButtons.forEach((button, buttonIndex) => {
    button.classList.toggle("active", buttonIndex === activeProductSlide);
  });

  productDots.forEach((dot, dotIndex) => {
    dot.classList.toggle("is-active", dotIndex === activeProductSlide);
  });
};

const setActiveProductSlide = (nextIndex) => {
  if (!productTrack || !productSlides.length) {
    return;
  }

  const totalSlides = productSlides.length;
  const newIndex = ((nextIndex % totalSlides) + totalSlides) % totalSlides;

  if (newIndex === activeProductSlide) {
    return;
  }

  const canFlip =
    typeof gsap !== "undefined" &&
    productStage &&
    !window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  if (!canFlip) {
    applyProductSlideState(newIndex);
    return;
  }

  let forward = newIndex > activeProductSlide;
  if (activeProductSlide === totalSlides - 1 && newIndex === 0) {
    forward = true;
  }
  if (activeProductSlide === 0 && newIndex === totalSlides - 1) {
    forward = false;
  }

  const dir = forward ? 1 : -1;
  productStage.classList.add("is-page-turning");

  gsap
    .timeline({
      onComplete: () => {
        productStage.classList.remove("is-page-turning");
        gsap.set(productStage, { clearProps: "rotateY,rotateX,scale" });
      },
    })
    .to(productStage, {
      rotateY: dir * -24,
      rotateX: 5,
      scale: 0.93,
      duration: 0.3,
      ease: "power2.in",
      transformOrigin: "50% 50%",
    })
    .add(() => applyProductSlideState(newIndex))
    .fromTo(
      productStage,
      {
        rotateY: dir * 26,
        rotateX: -4,
        scale: 0.93,
      },
      {
        rotateY: 0,
        rotateX: 0,
        scale: 1,
        duration: 0.48,
        ease: "power3.out",
      }
    );
};

tabButtons.forEach((button) => {
  button.addEventListener("click", () => {
    const targetIndex = Number(button.dataset.slide || 0);
    setActiveProductSlide(targetIndex);
  });
});

productDots.forEach((dot) => {
  dot.addEventListener("click", () => {
    const targetIndex = Number(dot.dataset.slide || 0);
    setActiveProductSlide(targetIndex);
  });
});

if (productPrev) {
  productPrev.addEventListener("click", () => {
    setActiveProductSlide(activeProductSlide - 1);
  });
}

if (productNext) {
  productNext.addEventListener("click", () => {
    setActiveProductSlide(activeProductSlide + 1);
  });
}

if (meteorShower) {
  const meteorCount = window.innerWidth < 760 ? 10 : 18;

  for (let index = 0; index < meteorCount; index += 1) {
    const meteor = document.createElement("span");
    meteor.className = "shooting-star";
    meteor.style.setProperty("--left", `${55 + Math.random() * 45}%`);
    meteor.style.setProperty("--top", `${-15 + Math.random() * 35}%`);
    meteor.style.setProperty("--delay", `${Math.random() * 8}s`);
    meteor.style.setProperty("--duration", `${3.8 + Math.random() * 3.2}s`);
    meteor.style.setProperty("--tail", `${90 + Math.random() * 90}px`);
    meteor.style.setProperty("--size", `${1.6 + Math.random() * 1.8}px`);
    meteorShower.appendChild(meteor);
  }
}

const updateScrollMotion = () => {
  const viewportHeight = window.innerHeight || 1;

  if (heroSection) {
    const heroRect = heroSection.getBoundingClientRect();
    const heroRange = Math.max(heroRect.height * 0.72, 1);
    const heroProgress = Math.min(Math.max(-heroRect.top / heroRange, 0), 1);
    root.style.setProperty("--hero-progress", heroProgress.toFixed(4));
  }

  revealSections.forEach((section) => {
    const rect = section.getBoundingClientRect();
    const distanceFromCenter = rect.top + rect.height / 2 - viewportHeight / 2;
    const progress = Math.min(Math.max(distanceFromCenter / viewportHeight, -1), 1);
    section.style.setProperty("--section-progress", progress.toFixed(4));
  });

  let activeSectionIndex = -1;
  let closestDistance = Number.POSITIVE_INFINITY;

  revealSections.forEach((section, index) => {
    const rect = section.getBoundingClientRect();
    const distance = Math.abs(rect.top + rect.height / 2 - viewportHeight / 2);

    if (distance < closestDistance) {
      closestDistance = distance;
      activeSectionIndex = index;
    }
  });

  revealSections.forEach((section, index) => {
    section.classList.toggle("is-active-section", index === activeSectionIndex);
    section.classList.toggle("is-dimmed", activeSectionIndex > -1 && index < activeSectionIndex);
  });
};

let motionTicking = false;

const requestMotionUpdate = () => {
  if (motionTicking) {
    return;
  }

  motionTicking = true;
  window.requestAnimationFrame(() => {
    updateScrollMotion();
    motionTicking = false;
  });
};

const initFallbackReveal = () => {
  document.documentElement.classList.add("motion-fallback");

  if (!revealSections.length) {
    return;
  }

  const revealObserver = new IntersectionObserver(
    (entries, observer) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) {
          return;
        }

        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
      });
    },
    {
      threshold: 0.18,
      rootMargin: "0px 0px -8% 0px",
    }
  );

  revealSections.forEach((section) => {
    revealObserver.observe(section);
  });
};

const initNavScrollSpy = () => {
  if (typeof gsap === "undefined" || typeof ScrollTrigger === "undefined") {
    return;
  }

  navLinks.forEach((link) => {
    const href = link.getAttribute("href");
    if (!href || href === "#") {
      return;
    }

    const target = document.querySelector(href);
    if (!target) {
      return;
    }

    ScrollTrigger.create({
      trigger: target,
      start: "top 45%",
      end: "bottom 45%",
      onToggle: (self) => {
        link.classList.toggle("is-active", self.isActive);
      },
    });
  });
};

const initLenis = () => {
  if (typeof Lenis === "undefined" || typeof ScrollTrigger === "undefined") {
    return false;
  }

  document.documentElement.classList.add("lenis-smooth");

  lenisInstance = new Lenis({
    duration: 1.15,
    easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
    smoothWheel: true,
  });

  lenisInstance.on("scroll", ScrollTrigger.update);

  const lenisRaf = (time) => {
    lenisInstance.raf(time);
    requestAnimationFrame(lenisRaf);
  };
  requestAnimationFrame(lenisRaf);

  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", (event) => {
      const href = anchor.getAttribute("href");
      if (!href || href === "#") {
        return;
      }

      const target = document.querySelector(href);
      if (!target) {
        return;
      }

      event.preventDefault();
      lenisInstance.scrollTo(target, {
        offset: -96,
        lerp: 0.08,
      });
    });
  });

  return true;
};

const initGsapMotion = () => {
  gsap.registerPlugin(ScrollTrigger);

  ScrollTrigger.defaults({
    toggleActions: "play none none none",
  });

  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    initFallbackReveal();
    return;
  }

  initLenis();

  if (heroSection) {
    const heroChildren = gsap.utils.toArray(".hero-copy > *");
    gsap.from(heroChildren, {
      opacity: 0,
      y: 56,
      rotateX: 8,
      transformOrigin: "50% 0",
      duration: 1.05,
      stagger: 0.09,
      ease: "power3.out",
      delay: 0.12,
    });

    gsap.from(".hero-visual", {
      opacity: 0,
      scale: 0.9,
      y: 40,
      duration: 1.2,
      ease: "power3.out",
      delay: 0.08,
    });

    gsap.timeline({
      scrollTrigger: {
        trigger: heroSection,
        start: "top top",
        end: "bottom top",
        scrub: 1.25,
        invalidateOnRefresh: true,
      },
    })
      .to(
        ".hero-copy",
        {
          y: -96,
          opacity: 0.28,
          rotateX: -14,
          transformOrigin: "50% 0%",
          ease: "none",
        },
        0
      )
      .to(
        ".hero-visual",
        {
          y: 110,
          scale: 0.88,
          opacity: 0.42,
          rotateX: 8,
          transformOrigin: "50% 100%",
          ease: "none",
        },
        0
      );
  }

  revealSections.forEach((section) => {
    const heading = section.querySelector(".flip-heading");
    const toolbar = section.querySelector(".flip-toolbar");
    const cards = section.querySelectorAll(".flip-card");

    const pageEdge = document.createElement("div");
    pageEdge.className = "page-flip-edge";
    pageEdge.setAttribute("aria-hidden", "true");
    section.insertBefore(pageEdge, section.firstChild);

    ScrollTrigger.create({
      trigger: section,
      start: "top 78%",
      onEnter: () => section.classList.add("is-visible"),
      once: true,
    });

    const timeline = gsap.timeline({
      scrollTrigger: {
        trigger: section,
        start: "top 90%",
        end: "top 28%",
        scrub: 1.35,
        invalidateOnRefresh: true,
      },
    });

    timeline.fromTo(
      pageEdge,
      {
        rotateX: 105,
        opacity: 0,
        scaleY: 0.2,
        transformOrigin: "50% 100%",
      },
      {
        rotateX: 48,
        opacity: 0.5,
        scaleY: 1,
        ease: "none",
      },
      0
    );

    if (heading) {
      timeline.fromTo(
        heading,
        {
          yPercent: 22,
          opacity: 0,
          rotateX: 22,
          rotateY: -12,
          filter: "blur(14px)",
          transformOrigin: "0% 0%",
        },
        {
          yPercent: 0,
          opacity: 1,
          rotateX: 0,
          rotateY: 0,
          filter: "blur(0px)",
          ease: "none",
        },
        0
      );
    }

    if (toolbar) {
      timeline.fromTo(
        toolbar,
        {
          yPercent: 16,
          opacity: 0,
          rotateX: 16,
          filter: "blur(10px)",
          transformOrigin: "50% 0",
        },
        {
          yPercent: 0,
          opacity: 1,
          rotateX: 0,
          filter: "blur(0px)",
          ease: "none",
        },
        0.06
      );
    }

    cards.forEach((card, index) => {
      const tiltMatch = card.style.getPropertyValue("--tilt").trim();
      const rotateYFrom = tiltMatch ? parseFloat(tiltMatch) : 0;

      timeline.fromTo(
        card,
        {
          yPercent: 18,
          opacity: 0,
          rotateX: 26,
          rotateY: rotateYFrom * 0.65,
          filter: "blur(12px)",
          transformOrigin: "50% 0",
        },
        {
          yPercent: 0,
          opacity: 1,
          rotateX: 0,
          rotateY: 0,
          filter: "blur(0px)",
          ease: "none",
        },
        0.12 + index * 0.07
      );
    });
  });

  initNavScrollSpy();

  ScrollTrigger.addEventListener("refresh", updateScrollMotion);
  ScrollTrigger.refresh();
};

updateScrollMotion();
applyProductSlideState(0);

if (typeof gsap !== "undefined" && typeof ScrollTrigger !== "undefined") {
  initGsapMotion();
} else {
  initFallbackReveal();
}

window.addEventListener("scroll", requestMotionUpdate, { passive: true });
window.addEventListener("resize", () => {
  requestMotionUpdate();
  if (typeof ScrollTrigger !== "undefined") {
    ScrollTrigger.refresh();
  }
});
