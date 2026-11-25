(function () {
  "use strict";

  var header = document.querySelector(".site-header");
  if (header) {
    var onScroll = function () {
      header.classList.toggle("is-scrolled", window.scrollY > 4);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  document.querySelectorAll(".flash").forEach(function (flash) {
    var close = document.createElement("button");
    close.type = "button";
    close.className = "flash-close";
    close.setAttribute("aria-label", "Dismiss message");
    close.textContent = "\u00d7";
    close.addEventListener("click", function () {
      flash.remove();
    });
    flash.appendChild(close);

    if (flash.classList.contains("flash-success")) {
      window.setTimeout(function () {
        flash.classList.add("is-leaving");
        window.setTimeout(function () {
          flash.remove();
        }, 300);
      }, 6000);
    }
  });

  document.querySelectorAll("[data-copy]").forEach(function (button) {
    button.addEventListener("click", function () {
      var value = button.getAttribute("data-copy");
      var original = button.textContent;
      var done = function () {
        button.textContent = "Copied";
        window.setTimeout(function () {
          button.textContent = original;
        }, 1600);
      };
      if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(value).then(done, done);
      } else {
        done();
      }
    });
  });

  var address = document.getElementById("address");
  var counter = document.querySelector('[data-counter-for="address"]');
  if (address && counter) {
    var renderCount = function () {
      counter.textContent = address.value.length + "/255";
    };
    address.addEventListener("input", renderCount);
    renderCount();
  }

  document.querySelectorAll("form.form-card").forEach(function (form) {
    form.addEventListener("submit", function () {
      var submit = form.querySelector('button[type="submit"]');
      if (submit && !submit.disabled) {
        submit.disabled = true;
        submit.textContent = "Saving\u2026";
      }
    });
  });
})();
