document.addEventListener("DOMContentLoaded", () => {
  const responsiveMenu = document.querySelector(".burger");
  const navLinks = document.querySelector(".nav-links");
  const burgerIcon = document.querySelector(".burger-icon");
  const closeIcon = document.querySelector(".close-icon");

  //Gère l'update de mon panier
  updateCart();

  responsiveMenu.addEventListener("click", () => {
    navLinks.classList.toggle("menu-responsive");

    const isMenuOpen = navLinks.classList.contains("menu-responsive");
    burgerIcon.style.display = isMenuOpen ? "none" : "inline";
    closeIcon.style.display = isMenuOpen ? "inline" : "none";
  });
});

// Gère la déconnection à retravailler
const logout = document.querySelector(".logout");

if (logout !== null) {
  logout.addEventListener("click", (e) => {
    e.preventDefault();

    const userConfirm = confirm("Etes-vous sur de vouloir vous déconnecter?");

    if (userConfirm) {
      window.location.href = logout.href;
    }
  });
}

// Gère la quantité du panier
function updateCart() {
  let storedTickets = JSON.parse(localStorage.getItem("tickets")) || [];
  let products = storedTickets.length;

  let cartCount = document.querySelector(".cart-count");
  if (products === 0) {
    cartCount.textContent = "";
  } else if (products > 0 || products < 10) {
    cartCount.textContent = products;
  } else {
    cartCount.textContent = "+9";
  }
}
