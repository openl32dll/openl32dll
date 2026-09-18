// openl32dll — küçük UI davranışları (mobil menü, aktif link)
document.addEventListener("DOMContentLoaded", function () {
  var toggle = document.querySelector(".nav-toggle");
  var links = document.querySelector(".nav-links");

  if (toggle && links) {
    toggle.addEventListener("click", function () {
      links.classList.toggle("open");
      var expanded = links.classList.contains("open");
      toggle.setAttribute("aria-expanded", expanded ? "true" : "false");
    });

    links.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        links.classList.remove("open");
        toggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  var year = document.querySelector("[data-year]");
  if (year) {
    year.textContent = new Date().getFullYear();
  }

  var contactForm = document.getElementById("contact-form");
  var status = document.getElementById("form-status");

  if (contactForm && status) {
    contactForm.addEventListener("submit", function (event) {
      event.preventDefault();

      var submitBtn = contactForm.querySelector("button[type=submit]");
      submitBtn.disabled = true;
      submitBtn.textContent = "Gönderiliyor...";
      status.style.color = "";
      status.textContent = "Mesajın gönderiliyor...";

      fetch(contactForm.action, {
        method: "POST",
        body: new FormData(contactForm),
        headers: { Accept: "application/json" },
      })
        .then(function (response) {
          if (response.ok) {
            contactForm.reset();
            status.style.color = "var(--accent-3)";
            status.textContent = "Teşekkürler! Mesajın iletildi, en kısa sürede dönüş yapacağım.";
          } else {
            throw new Error("Gönderim başarısız");
          }
        })
        .catch(function () {
          status.style.color = "var(--danger)";
          status.textContent = "Mesaj gönderilemedi. Doğrudan openl32dll.dev@gmail.com adresine yazabilirsin.";
        })
        .finally(function () {
          submitBtn.disabled = false;
          submitBtn.textContent = "Mesajı Gönder";
        });
    });
  }
});
