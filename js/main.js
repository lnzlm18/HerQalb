document.addEventListener('DOMContentLoaded',function(){
  // set year
  const y = new Date().getFullYear();
  const el = document.getElementById('year'); if(el) el.textContent = y;

  // mobile nav toggle
  const toggle = document.querySelector('.nav-toggle');
  const nav = document.querySelector('.main-nav');
  if(toggle && nav){
    toggle.addEventListener('click', ()=>{
      const expanded = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!expanded));
      nav.style.display = expanded ? 'none' : 'block';
    });
  }

  // simple form handling (no backend) — show friendly message
  const form = document.getElementById('contactForm');
  const msg = document.getElementById('formMsg');
  if(form){
    form.addEventListener('submit', function(e){
      e.preventDefault();
      msg.textContent = 'Thanks — we received your request. We will be in touch soon.';
      form.reset();
    });
    const sub = document.getElementById('subscribe');
    if(sub){
      sub.addEventListener('click', ()=>{ msg.textContent = 'Subscribed — check your email for confirmation.' });
    }
  }
});
