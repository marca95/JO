document.addEventListener("DOMContentLoaded", function () {
  const sportLinks = document.querySelectorAll(".sport-link");
  const eventsContainer = document.getElementById("sport-details");

  function loadEvents(sportId) {
    fetch(`/ticket/${sportId}/events/`)
      .then((response) => response.json())
      .then((data) => {
        const backgroundBlur =
          eventsContainer.querySelector(".background-blur");
        const contentContainer = eventsContainer.querySelector(".content");

        contentContainer.innerHTML = "";

        if (data.sport_image_url) {
          backgroundBlur.style.backgroundImage = `url(${data.sport_image_url})`;
        }

        data.events.forEach((event) => {
          const eventElement = document.createElement("div");
          eventElement.className = "event-card";
          eventElement.innerHTML = `
                      <h3>${event.date} - ${event.hour}</h3>
                      <p>${event.stadium.name}, ${event.stadium.address}</p>
                      <button data-sport-id="${sportId}" data-event-id="${event.id}" class="view-event">Voir l'événement</button>
                  `;
          contentContainer.appendChild(eventElement);
        });

        document.querySelectorAll(".view-event").forEach((button) => {
          button.addEventListener("click", function () {
            const sportId = this.dataset.sportId;
            const eventId = this.dataset.eventId;
            loadEventDetails(sportId, eventId);
          });
        });
      });
  }

  function loadEventDetails(sportId, eventId) {
    fetch(`/ticket/${sportId}/events/${eventId}/`)
      .then((response) => response.json())
      .then((data) => {
        const event = data.event;
        const contentContainer = eventsContainer.querySelector(".content");
        contentContainer.innerHTML = `
                  <h2>${event.date} - ${event.hour}</h2>
                  <p>Stadium: ${event.stadium.name}, ${
          event.stadium.address
        }</p>
                  <p>Available Seats: ${event.stadium.available_space}</p>
                  ${event.tickets
                    .map(
                      (ticket) => `
                      <p>${ticket.formula}: ${ticket.price}€</p>
                  `
                    )
                    .join("")}
              `;
      });
  }

  sportLinks.forEach((link) => {
    link.addEventListener("click", function (e) {
      e.preventDefault();
      const sportId = this.dataset.sportId;
      loadEvents(sportId);
    });
  });
});
