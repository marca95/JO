document.addEventListener("DOMContentLoaded", () => {
  const responsiveMenu = document.querySelector(".burger");
  const navLinks = document.querySelector(".nav-links");
  const burgerIcon = document.querySelector(".burger-icon");
  const closeIcon = document.querySelector(".close-icon");

  responsiveMenu.addEventListener("click", () => {
    navLinks.classList.toggle("menu-responsive");

    const isMenuOpen = navLinks.classList.contains("menu-responsive");
    burgerIcon.style.display = isMenuOpen ? "none" : "inline";
    closeIcon.style.display = isMenuOpen ? "inline" : "none";
  });
});
