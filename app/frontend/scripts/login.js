document.addEventListener("DOMContentLoaded", () => {
  const toggleButtons = document.querySelectorAll(".toggle-form");
  const formContent = document.querySelector(".form-content");
  const loginForm = document.querySelector(".login-form");
  const signupForm = document.querySelector(".signup-form");
  const loginSubmit = document.getElementById("login-submit");
  const signupSubmit = document.getElementById("signup-submit");

  toggleButtons.forEach(button => {
    button.addEventListener("click", () => {
      loginForm.classList.toggle("active");
      signupForm.classList.toggle("active");

      if (signupForm.classList.contains("active")) {
        formContent.style.transform = "translateX(-50%)";
      } else {
        formContent.style.transform = "translateX(0%)";
      }
    });
  });

  if (loginSubmit) {
    loginSubmit.addEventListener("click", async () => {
      const username = document.getElementById("login-username").value.trim();
      const password = document.getElementById("login-password").value;

      if (!username || !password) {
        alert("Please fill in all fields");
        return;
      }

      try {
        const response = await fetch("/api/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ username, password })
        });

        const data = await response.json();

        if (response.ok) {
          localStorage.setItem("token", data.token);
          localStorage.setItem("username", username);
          window.location.href = "dashboard.html";
        } else {
          alert(data.message || "Login failed");
        }
      } catch (error) {
        console.error(error);
        alert("Error connecting to server");
      }
    });
  }

  if (signupSubmit) {
    signupSubmit.addEventListener("click", async () => {
      const username = document.getElementById("signup-username").value.trim();
      const email = document.getElementById("signup-email").value.trim();
      const password = document.getElementById("signup-password").value;
      const confirmPassword = document.getElementById("signup-confirm-password").value;

      if (!username || !email || !password || !confirmPassword) {
        alert("Please fill in all fields");
        return;
      }

      if (password !== confirmPassword) {
        alert("Passwords do not match");
        return;
      }

      try {
        const response = await fetch("/api/register", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ username, email, password })
        });

        const data = await response.json();

        if (response.ok) {
          alert("Registration successful! Please login.");
          toggleButtons[0]?.click();
        } else {
          alert(data.message || "Registration failed");
        }
      } catch (error) {
        console.error(error);
        alert("Error connecting to server");
      }
    });
  }
});
