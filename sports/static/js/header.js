// For burger menu
document.addEventListener("DOMContentLoaded", () => {
  const responsiveMenu = document.querySelector(".burger");
  const navLinks = document.querySelector(".nav-links");
  const navBar = document.querySelector(".navbar");

  responsiveMenu.addEventListener("click", () => {
    navLinks.classList.toggle("menu-responsive");
    navBar.classList.toggle("menu-show");
  });
});
