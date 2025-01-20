document.addEventListener("DOMContentLoaded", function () {
  let tickets = JSON.parse(localStorage.getItem("tickets"));

  const show_ticket = document.querySelector(".show_ticket");

  if (tickets.length === 0) {
    show_ticket.innerHTML = `<p>Vous n'avez pas selectionné de ticket</p>`;
  } else {
    tickets.forEach((ticket) => {
      const ticketElement = document.createElement("p");
      ticketElement.innerHTML = `<p>Ticket id numéro ${ticket}</p>`;

      show_ticket.appendChild(ticketElement);
    });
  }
});
