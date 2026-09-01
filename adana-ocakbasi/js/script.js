/* Görsel yüklenemezse (örn. ağ engeli) zarif bir yer tutucuya düş. */
function imgFallback(img, emoji) {
  if (img.dataset.fallbackApplied) return;
  img.dataset.fallbackApplied = "1";
  img.onerror = null;
  img.removeAttribute("src");
  img.classList.add("img-fallback");
  var span = document.createElement("span");
  span.className = "img-fallback-icon";
  span.textContent = emoji || "🍽️";
  if (img.parentElement) {
    img.parentElement.style.position = img.parentElement.style.position || "relative";
    img.parentElement.appendChild(span);
  }
}

document.addEventListener('DOMContentLoaded', function () {
  "use strict";

  /* back-to-top visibility */
  var backTop = document.getElementById('backTop');
  function onScroll(){
    backTop.classList.toggle('show', window.scrollY > 500);
  }
  window.addEventListener('scroll', onScroll);
  onScroll();
  backTop.addEventListener('click', function(){ window.scrollTo({top:0, behavior:'smooth'}); });

  /* mobile nav */
  var navToggle = document.getElementById('navToggle');
  var nav = document.getElementById('nav');
  navToggle.addEventListener('click', function(){
    nav.classList.toggle('open');
    navToggle.classList.toggle('open');
  });
  nav.querySelectorAll('a').forEach(function(a){
    a.addEventListener('click', function(){
      nav.classList.remove('open');
      navToggle.classList.remove('open');
    });
  });

  /* menu tabs */
  var tabs = document.querySelectorAll('.menu-tab');
  var panels = document.querySelectorAll('.menu-panel');
  tabs.forEach(function(tab){
    tab.addEventListener('click', function(){
      tabs.forEach(function(t){ t.classList.remove('active'); });
      panels.forEach(function(p){ p.classList.remove('active'); });
      tab.classList.add('active');
      document.getElementById(tab.dataset.target).classList.add('active');
      document.getElementById('menu').scrollIntoView({behavior:'smooth', block:'start'});
    });
  });

  /* reservation form (demo only — no backend, wire this up to your own endpoint) */
  var form = document.getElementById('reservationForm');
  var success = document.getElementById('formSuccess');
  if (form) {
    form.addEventListener('submit', function(e){
      e.preventDefault();
      success.classList.add('show');
      form.reset();
      setTimeout(function(){ success.classList.remove('show'); }, 6000);
    });
  }

  /* scroll reveal */
  var reveals = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(entry){
        if (entry.isIntersecting) {
          entry.target.classList.add('in');
          io.unobserve(entry.target);
        }
      });
    }, {threshold:.12});
    reveals.forEach(function(el){ io.observe(el); });
  } else {
    reveals.forEach(function(el){ el.classList.add('in'); });
  }

  /* footer year */
  var yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();
});
