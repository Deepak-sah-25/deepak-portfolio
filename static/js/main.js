/**
 * Deepak Sah - Portfolio JavaScript
 * Modern Interactive Behaviors & High Performance Animations
 */

document.addEventListener('DOMContentLoaded', () => {
  // 1. Preloader Handling
  const preloader = document.getElementById('preloader');
  if (preloader) {
    window.addEventListener('load', () => {
      setTimeout(() => {
        preloader.classList.add('loaded');
      }, 350);
    });
    // Fallback if load event already fired
    setTimeout(() => {
      preloader.classList.add('loaded');
    }, 1200);
  }

  // 2. Navbar Scroll Behavior & Active Links
  const header = document.querySelector('.site-header');
  const navLinks = document.querySelectorAll('.nav-link');
  const sections = document.querySelectorAll('section[id]');
  const backToTop = document.getElementById('backToTop');

  window.addEventListener('scroll', () => {
    const scrollY = window.scrollY;

    // Header blur/shrink
    if (header) {
      if (scrollY > 50) {
        header.classList.add('scrolled');
      } else {
        header.classList.remove('scrolled');
      }
    }

    // Back to top button visibility
    if (backToTop) {
      if (scrollY > 500) {
        backToTop.classList.add('show');
      } else {
        backToTop.classList.remove('show');
      }
    }

    // Active Section Tracking
    let currentId = '';
    sections.forEach(section => {
      const sectionTop = section.offsetTop - 120;
      const sectionHeight = section.offsetHeight;
      if (scrollY >= sectionTop && scrollY < sectionTop + sectionHeight) {
        currentId = section.getAttribute('id');
      }
    });

    navLinks.forEach(link => {
      link.classList.remove('active');
      if (link.getAttribute('href') === `#${currentId}`) {
        link.classList.add('active');
      }
    });
  });

  if (backToTop) {
    backToTop.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // 3. Typewriter Effect for Hero
  const typewriterElement = document.getElementById('typewriterText');
  if (typewriterElement) {
    const phrases = [
      'Django Developer',
      'Django Backend Developer',
      'Full-Stack Web Developer',
      'Backend Systems Specialist',
      'Multi-Tenant SaaS Architect',
      'PostgreSQL & API Engineer'
    ];
    let phraseIdx = 0;
    let charIdx = 0;
    let isDeleting = false;
    const typingSpeed = 100;
    const deletingSpeed = 40;
    const pauseDelay = 1800;

    function typeLoop() {
      const currentPhrase = phrases[phraseIdx];
      
      if (isDeleting) {
        typewriterElement.textContent = currentPhrase.substring(0, charIdx - 1);
        charIdx--;
      } else {
        typewriterElement.textContent = currentPhrase.substring(0, charIdx + 1);
        charIdx++;
      }

      if (!isDeleting && charIdx === currentPhrase.length) {
        isDeleting = true;
        setTimeout(typeLoop, pauseDelay);
        return;
      } else if (isDeleting && charIdx === 0) {
        isDeleting = false;
        phraseIdx = (phraseIdx + 1) % phrases.length;
        setTimeout(typeLoop, 400);
        return;
      }

      setTimeout(typeLoop, isDeleting ? deletingSpeed : typingSpeed);
    }

    typeLoop();
  }

  // 4. Scroll Reveal Animations (Intersection Observer)
  const revealElements = document.querySelectorAll('.reveal-init');
  if ('IntersectionObserver' in window) {
    const revealObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('reveal-active');
          observer.unobserve(entry.target);
        }
      });
    }, {
      rootMargin: '0px 0px -60px 0px',
      threshold: 0.12
    });

    revealElements.forEach(el => revealObserver.observe(el));
  } else {
    // Fallback: immediately show elements
    revealElements.forEach(el => {
      el.classList.add('reveal-active');
    });
  }

  // 5. Floating Code Card 3D Tilt Effect on Desktop
  const heroVisual = document.querySelector('.hero-visual');
  const floatingCodeCard = document.querySelector('.floating-code-card');

  if (heroVisual && floatingCodeCard && window.innerWidth > 992) {
    heroVisual.addEventListener('mousemove', (e) => {
      const rect = heroVisual.getBoundingClientRect();
      const x = e.clientX - rect.left - rect.width / 2;
      const y = e.clientY - rect.top - rect.height / 2;
      
      const tiltX = (y / (rect.height / 2)) * -10;
      const tiltY = (x / (rect.width / 2)) * 12;

      floatingCodeCard.style.transform = `perspective(1000px) rotateX(${tiltX}deg) rotateY(${tiltY}deg) translateY(-8px)`;
    });

    heroVisual.addEventListener('mouseleave', () => {
      floatingCodeCard.style.transform = '';
    });
  }

  // 6. Enhanced Skills Animation: Smooth Numerical Count-up & Gradual Bar Fill ("Slowly Slowly Increase")
  const skillsGrid = document.querySelector('.skills-grid');
  const skillCards = document.querySelectorAll('.skill-card');
  const skillTabs = document.querySelectorAll('.tab-btn[data-category]');

  function animateSkillCard(card, delay = 0) {
    const percentageEl = card.querySelector('.skill-percentage');
    const barFill = card.querySelector('.skill-bar-fill');
    if (!percentageEl || !barFill) return;

    const rawTarget = percentageEl.getAttribute('data-target') ||
                      card.getAttribute('data-proficiency') ||
                      (barFill.getAttribute('data-width') ? barFill.getAttribute('data-width').replace('%', '') : '90');
    const targetProficiency = Math.min(Math.max(parseInt(rawTarget, 10) || 90, 0), 100);

    // Cancel any running animations or pending delays on this card
    if (card._animFrame) {
      cancelAnimationFrame(card._animFrame);
      card._animFrame = null;
    }
    if (card._delayTimeout) {
      clearTimeout(card._delayTimeout);
      card._delayTimeout = null;
    }

    // Reset visually to 0 before starting animation
    percentageEl.textContent = '0%';
    barFill.style.width = '0%';

    card._delayTimeout = setTimeout(() => {
      const duration = 1800; // 1.8 seconds smooth relaxed climb
      let startTime = null;

      function step(timestamp) {
        if (!startTime) startTime = timestamp;
        const elapsed = timestamp - startTime;
        const progress = Math.min(elapsed / duration, 1);

        // easeOutCubic curve for relaxed and steady acceleration slowing into target
        const ease = 1 - Math.pow(1 - progress, 3);
        const currentVal = Math.round(ease * targetProficiency);

        percentageEl.textContent = `${currentVal}%`;
        barFill.style.width = `${(ease * targetProficiency).toFixed(1)}%`;

        if (progress < 1) {
          card._animFrame = requestAnimationFrame(step);
        } else {
          percentageEl.textContent = `${targetProficiency}%`;
          barFill.style.width = `${targetProficiency}%`;
          card._animFrame = null;
        }
      }

      card._animFrame = requestAnimationFrame(step);
    }, delay);
  }

  function triggerSkillsCascade() {
    const visibleCards = Array.from(skillCards).filter(
      card => card.style.display !== 'none' && !card.classList.contains('hidden')
    );
    visibleCards.forEach((card, index) => {
      // Staggered delay for sleek wave effect (capped at 400ms max delay)
      const delay = Math.min(index * 45, 400);
      animateSkillCard(card, delay);
    });
  }

  // IntersectionObserver to trigger animation when skills section enters viewport
  if (skillsGrid) {
    let skillsAnimated = false;
    if ('IntersectionObserver' in window) {
      const skillsObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
          if (entry.isIntersecting && !skillsAnimated) {
            skillsAnimated = true;
            triggerSkillsCascade();
            observer.unobserve(entry.target);
          }
        });
      }, {
        rootMargin: '0px 0px -40px 0px',
        threshold: 0.15
      });
      skillsObserver.observe(skillsGrid);
    } else {
      triggerSkillsCascade();
    }
  }

  // Interactive Skill Category Tabs with re-animation
  if (skillTabs.length > 0) {
    skillTabs.forEach(tab => {
      tab.addEventListener('click', () => {
        skillTabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');

        const targetCategory = tab.getAttribute('data-category');
        let visibleCount = 0;

        skillCards.forEach(card => {
          const cardCat = card.getAttribute('data-category');
          if (targetCategory === 'all' || cardCat === targetCategory) {
            card.style.display = 'block';
            const delay = Math.min(visibleCount * 45, 360);
            animateSkillCard(card, delay);
            visibleCount++;
          } else {
            card.style.display = 'none';
          }
        });
      });
    });
  }

  // 7. Project Details Modal Logic
  const modalOverlay = document.getElementById('projectModal');
  const modalCloseBtn = document.getElementById('modalCloseBtn');
  const modalTitle = document.getElementById('modalTitle');
  const modalSubtitle = document.getElementById('modalSubtitle');
  const modalSummary = document.getElementById('modalSummary');
  const modalDescription = document.getElementById('modalDescription');
  const modalFeaturesList = document.getElementById('modalFeaturesList');
  const modalTechTags = document.getElementById('modalTechTags');
  const openModalButtons = document.querySelectorAll('.open-project-modal');

  function openProjectModal(projectId) {
    fetch(`/api/projects/${projectId}/`)
      .then(res => res.json())
      .then(data => {
        modalTitle.textContent = data.title;
        modalSubtitle.textContent = `${data.project_type} • Role: ${data.role}`;
        modalSummary.textContent = data.summary;
        modalDescription.textContent = data.description;

        // Render features
        modalFeaturesList.innerHTML = '';
        if (data.features && data.features.length) {
          data.features.forEach(feat => {
            const li = document.createElement('li');
            li.textContent = feat;
            modalFeaturesList.appendChild(li);
          });
        }

        // Render tech tags
        modalTechTags.innerHTML = '';
        if (data.technologies && data.technologies.length) {
          data.technologies.forEach(tech => {
            const span = document.createElement('span');
            span.className = 'tech-pill';
            span.textContent = tech;
            modalTechTags.appendChild(span);
          });
        }

        // Render live link
        const modalLinks = document.getElementById('modalLinks');
        if (modalLinks) {
          modalLinks.innerHTML = '';
          if (data.live_url) {
            const a = document.createElement('a');
            a.href = data.live_url;
            a.target = '_blank';
            a.rel = 'noopener noreferrer';
            a.className = 'btn-primary-glow';
            a.innerHTML = '<span>Visit Live Website ↗</span>';
            modalLinks.appendChild(a);
          }
        }

        modalOverlay.classList.add('active');
        document.body.style.overflow = 'hidden';
      })
      .catch(err => {
        console.error('Error loading project details:', err);
      });
  }

  function closeProjectModal() {
    modalOverlay.classList.remove('active');
    document.body.style.overflow = '';
  }

  openModalButtons.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      const projId = btn.getAttribute('data-project-id');
      if (projId) openProjectModal(projId);
    });
  });

  // Whole project card click: open live URL directly in new tab, or open modal if no live URL
  const projectCards = document.querySelectorAll('.project-card');
  projectCards.forEach(card => {
    card.addEventListener('click', (e) => {
      if (e.target.closest('button') || e.target.closest('a')) {
        return;
      }
      const liveUrl = card.getAttribute('data-live-url');
      if (liveUrl) {
        window.open(liveUrl, '_blank', 'noopener,noreferrer');
      } else {
        const modalId = card.getAttribute('data-modal-id');
        if (modalId) {
          openProjectModal(modalId);
        }
      }
    });
  });

  if (modalCloseBtn) {
    modalCloseBtn.addEventListener('click', closeProjectModal);
  }

  if (modalOverlay) {
    modalOverlay.addEventListener('click', (e) => {
      if (e.target === modalOverlay) closeProjectModal();
    });
  }

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modalOverlay && modalOverlay.classList.contains('active')) {
      closeProjectModal();
    }
  });

  // 8. Contact Form AJAX Submission & Toast
  const contactForm = document.getElementById('contactForm');
  const toastNotice = document.getElementById('toastNotice');
  const toastText = document.getElementById('toastText');
  const submitBtn = document.getElementById('submitBtn');

  function showToast(messageHtml, isSuccess = true) {
    if (!toastNotice || !toastText) return;
    toastText.innerHTML = messageHtml;
    toastNotice.querySelector('.toast-icon').textContent = isSuccess ? '✓' : '⚠';
    toastNotice.classList.add('show');
    setTimeout(() => {
      toastNotice.classList.remove('show');
    }, 6500);
  }

  if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
      e.preventDefault();
      
      const formData = new FormData(contactForm);
      const actionUrl = contactForm.getAttribute('action');

      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = `<span>Sending...</span>`;
      }

      fetch(actionUrl, {
        method: 'POST',
        body: formData,
        headers: {
          'X-Requested-With': 'XMLHttpRequest'
        }
      })
      .then(res => res.json().then(data => ({ ok: res.ok, data })))
      .then(({ ok, data }) => {
        if (ok && data.success) {
          let toastHtml = `<span>${data.message}</span>`;
          if (data.whatsapp_url) {
            toastHtml += ` <br><a href="${data.whatsapp_url}" target="_blank" rel="noopener noreferrer" style="color: #4ade80; text-decoration: underline; font-weight: 700; margin-top: 4px; display: inline-block;">📱 Also ping Deepak on WhatsApp ↗</a>`;
          }
          showToast(toastHtml, true);
          contactForm.reset();
        } else {
          showToast(data.message || 'An error occurred while submitting.', false);
        }
      })
      .catch(err => {
        console.error('Submission error:', err);
        showToast('Network error. Please try again.', false);
      })
      .finally(() => {
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.innerHTML = `<span>Send Message ↗</span>`;
        }
      });
    });
  }

  // 11. Sticky Floating Contact Speed Dial Logic
  const floatingWrapper = document.getElementById('floatingContactWrapper');
  const floatingTrigger = document.getElementById('floatingContactTrigger');
  const floatingMenu = document.getElementById('floatingContactMenu');
  const floatingContactAnchor = document.getElementById('floatingContactAnchor');

  if (floatingTrigger && floatingWrapper) {
    function toggleFloatingMenu() {
      const isActive = floatingWrapper.classList.toggle('active');
      floatingTrigger.setAttribute('aria-expanded', isActive ? 'true' : 'false');
      if (floatingMenu) {
        floatingMenu.setAttribute('aria-hidden', isActive ? 'false' : 'true');
      }
    }

    function closeFloatingMenu() {
      floatingWrapper.classList.remove('active');
      floatingTrigger.setAttribute('aria-expanded', 'false');
      if (floatingMenu) {
        floatingMenu.setAttribute('aria-hidden', 'true');
      }
    }

    floatingTrigger.addEventListener('click', (e) => {
      e.stopPropagation();
      toggleFloatingMenu();
    });

    // Close on click outside
    document.addEventListener('click', (e) => {
      if (!floatingWrapper.contains(e.target)) {
        closeFloatingMenu();
      }
    });

    // Close on Escape key
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && floatingWrapper.classList.contains('active')) {
        closeFloatingMenu();
        floatingTrigger.focus();
      }
    });

    // Smooth scroll for Contact anchor inside menu
    if (floatingContactAnchor) {
      floatingContactAnchor.addEventListener('click', (e) => {
        closeFloatingMenu();
        const contactSection = document.getElementById('contact');
        if (contactSection) {
          e.preventDefault();
          contactSection.scrollIntoView({ behavior: 'smooth' });
        }
      });
    }
  }

  // 12. Mobile Navigation Drawer Interactivity
  const mobileMenuBtn = document.getElementById('mobileMenuBtn');
  const mobileNavDrawer = document.getElementById('mobileNavDrawer');
  const mobileNavLinks = document.querySelectorAll('.mobile-nav-link, .mobile-nav-cta-btn');

  if (mobileMenuBtn && mobileNavDrawer) {
    function toggleMobileNav(e) {
      if (e) e.stopPropagation();
      const isOpen = mobileNavDrawer.classList.toggle('open');
      mobileMenuBtn.classList.toggle('active', isOpen);
      mobileMenuBtn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
      mobileNavDrawer.setAttribute('aria-hidden', isOpen ? 'false' : 'true');
    }

    function closeMobileNav() {
      mobileNavDrawer.classList.remove('open');
      mobileMenuBtn.classList.remove('active');
      mobileMenuBtn.setAttribute('aria-expanded', 'false');
      mobileNavDrawer.setAttribute('aria-hidden', 'true');
    }

    mobileMenuBtn.addEventListener('click', toggleMobileNav);

    mobileNavLinks.forEach(link => {
      link.addEventListener('click', () => {
        closeMobileNav();
      });
    });

    document.addEventListener('click', (e) => {
      if (!mobileNavDrawer.contains(e.target) && !mobileMenuBtn.contains(e.target)) {
        closeMobileNav();
      }
    });

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && mobileNavDrawer.classList.contains('open')) {
        closeMobileNav();
        mobileMenuBtn.focus();
      }
    });
  }
});

