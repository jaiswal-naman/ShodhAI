function setupPasswordToggles() {
  document.querySelectorAll("[data-password-toggle]").forEach((button) => {
    const input = document.getElementById(button.dataset.passwordToggle);
    if (!input) {
      return;
    }

    button.addEventListener("click", () => {
      const showPassword = input.type === "password";
      input.type = showPassword ? "text" : "password";
      button.textContent = showPassword ? "HIDE" : "SHOW";
      button.setAttribute("aria-label", showPassword ? "Hide password" : "Show password");
    });
  });
}

function setupLoadingForms() {
  const overlay = document.getElementById("spinner-overlay");
  if (!overlay) {
    return;
  }

  document.querySelectorAll("form[data-loading-text]").forEach((form) => {
    form.addEventListener("submit", () => {
      const loadingText = form.dataset.loadingText || "Working...";
      const message = overlay.querySelector("p");
      const submitButton = form.querySelector("button[type='submit']");

      if (message) {
        message.textContent = loadingText;
      }

      if (submitButton) {
        submitButton.disabled = true;
        submitButton.textContent = loadingText;
      }

      overlay.style.display = "flex";
    });
  });
}

function setupPasswordValidation() {
  document.querySelectorAll("form[data-validate-password]").forEach((form) => {
    form.addEventListener("submit", (event) => {
      const password = form.querySelector("input[name='password']");
      if (password && password.value.length > 72) {
        event.preventDefault();
        password.setCustomValidity("Password cannot exceed 72 characters.");
        password.reportValidity();
      }
    });
  });
}

setupPasswordToggles();
setupLoadingForms();
setupPasswordValidation();
