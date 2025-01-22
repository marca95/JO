document.addEventListener("DOMContentLoaded", function () {
  let tickets = JSON.parse(localStorage.getItem("tickets")) || [];

  if (tickets.length > 0 && !window.location.search.includes("ticket_id")) {
    const url = `/panier/?ticket_id=${tickets.join("&ticket_id=")}`;
    window.location.href = url;
  }

  totalprice();

  const deleteButtons = document.querySelectorAll(".delete-ticket-btn");
  deleteButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const ticketId = this.parentElement.getAttribute("data-ticket-id");

      tickets = tickets.filter((id) => id !== ticketId);
      localStorage.setItem("tickets", JSON.stringify(tickets));

      this.parentElement.remove();

      // if (tickets.length === 0) {
      //   document.querySelector(".show_ticket").innerHTML =
      //     "<p>Aucun ticket dans votre panier.</p>";
      // }

      updateURL(tickets);
      updateCart();
      totalprice();
    });
  });
});

function updateURL(tickets) {
  let url = "/panier/";
  if (tickets.length > 0) {
    url = `/panier/?ticket_id=${tickets.join("&ticket_id=")}`;
  }
  window.history.replaceState({}, document.title, url);
}

// Calcul prix dynamique
function totalprice() {
  let price = document.querySelectorAll(".price");
  let totalPrice = 0;
  let sumPrice = document.querySelector(".total_price");

  price.forEach((element) => {
    let fetchPrice = element.innerHTML;
    totalPrice += parseFloat(fetchPrice.substr(23, 5));
  });

  if (totalPrice > 0) {
    sumPrice.textContent = `Prix total : ${totalPrice}€`;
  }
}
