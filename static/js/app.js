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
      const detail = overlay.querySelector("[data-spinner-steps]");
      const submitButton = form.querySelector("button[type='submit']");
      const defaultStages = [
        "Creating analyst perspectives",
        "Running live source research",
        "Writing the report body",
        "Exporting DOCX and PDF"
      ];
      const stages = (form.dataset.loadingStages || "")
        .split("|")
        .map((stage) => stage.trim())
        .filter(Boolean);
      const activeStages = stages.length ? stages : defaultStages;
      let index = 0;

      if (message) {
        message.textContent = loadingText;
      }
      if (detail) {
        detail.textContent = activeStages[index];
        window.setInterval(() => {
          index = Math.min(index + 1, activeStages.length - 1);
          detail.textContent = activeStages[index];
        }, 4800);
      }

      if (submitButton) {
        submitButton.disabled = true;
        submitButton.textContent = loadingText;
      }

      overlay.style.display = "flex";
    });
  });
}

function setupTopicSuggestions() {
  const topicInput = document.getElementById("topic");
  if (!topicInput) {
    return;
  }

  document.querySelectorAll("[data-topic]").forEach((button) => {
    button.addEventListener("click", () => {
      topicInput.value = button.dataset.topic || "";
      topicInput.focus();
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
setupTopicSuggestions();
setupPasswordValidation();
