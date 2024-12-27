// For burger menu
document.addEventListener("DOMContentLoaded", () => {
  const responsiveMenu = document.querySelector(".burger");
  const navLinks = document.querySelector(".nav-links");

  responsiveMenu.addEventListener("click", () => {
    navLinks.classList.toggle("menu-responsive");
  });
});
