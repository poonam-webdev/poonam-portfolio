// ---------- header scroll shadow ----------
const header = document.getElementById('siteHeader');
window.addEventListener('scroll', () => {
  header.classList.toggle('scrolled', window.scrollY > 20);
});

// ---------- mobile nav toggle ----------
const navToggle = document.getElementById('navToggle');
const navLinks = document.getElementById('navLinks');
navToggle.addEventListener('click', () => {
  navToggle.classList.toggle('open');
  navLinks.classList.toggle('open');
});
navLinks.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
  navToggle.classList.remove('open');
  navLinks.classList.remove('open');
}));

// ---------- scroll reveal ----------
const io = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.classList.add('in');
      io.unobserve(e.target);
    }
  });
}, { threshold: 0.15 });
document.querySelectorAll('.reveal').forEach(el => io.observe(el));

// ---------- active nav link on scroll ----------
const sections = document.querySelectorAll('section[id]');
const navA = document.querySelectorAll('.navlinks a');
const navObs = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      navA.forEach(a => a.classList.toggle('active', a.getAttribute('href') === '#' + entry.target.id));
    }
  });
}, { rootMargin: '-40% 0px -55% 0px' });
sections.forEach(s => navObs.observe(s));

// ---------- contact form -> Flask -> MongoDB ----------
const form = document.getElementById('contactForm');
const statusEl = document.getElementById('formStatus');

if (form) {
  form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const submitBtn = form.querySelector('button[type="submit"]');
    const payload = {
      name: form.name.value.trim(),
      email: form.email.value.trim(),
      message: form.message.value.trim(),
    };

    statusEl.textContent = '';
    statusEl.className = 'form-status';
    submitBtn.disabled = true;
    submitBtn.textContent = 'Sending…';

    try {
      const res = await fetch('/api/contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      const data = await res.json();

      if (res.ok && data.ok) {
        statusEl.textContent = data.message || 'Thanks! Your message has been received.';
        statusEl.classList.add('ok');
        form.reset();
      } else {
        statusEl.textContent = data.error || 'Something went wrong. Please try again.';
        statusEl.classList.add('error');
      }
    } catch (err) {
      statusEl.textContent = 'Could not reach the server. Please try emailing directly.';
      statusEl.classList.add('error');
    } finally {
      submitBtn.disabled = false;
      submitBtn.textContent = 'Send message';
    }
  });
}