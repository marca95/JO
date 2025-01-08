document.addEventListener("DOMContentLoaded", function () {
  const sportLinks = document.querySelectorAll(".sport-link");

  sportLinks.forEach((link) => {
    link.addEventListener("click", function (event) {
      event.preventDefault();

      const sportId = this.dataset.sportId;

      fetch(`/sport/${sportId}/events/`)
        .then((response) => response.json())
        .then((data) => {
          const eventsContainer = document.getElementById("sport-details");
          eventsContainer.innerHTML = "";

          data.events.forEach((event) => {
            const eventElement = document.createElement("div");

            const eventDate = event.date;
            const eventHour = event.hour;

            let nationsHtml = "";
            if (event.nations && event.nations.length > 0) {
              event.nations.forEach((nation) => {
                nationsHtml += `<span>${nation.name} (${nation.nickname})</span>`;
                if (nation.image_url) {
                  nationsHtml += `<img src="${nation.image_url}" alt="${nation.name}" width="50">`;
                }
              });
            } else if (event.players && event.players.length > 0) {
              event.players.forEach((player) => {
                nationsHtml += `<span>${player.first_name} ${player.last_name}</span>`;
                if (player.image_url) {
                  nationsHtml += `<img src="${player.image_url}" alt="${player.first_name} ${player.last_name}" title="${player.first_name} ${player.last_name}" width="50">`;
                }
              });
            } else {
              nationsHtml = `<span>Pas encore désigné.</span>`;
            }

            eventElement.innerHTML = `
              <h3>${eventDate} à ${eventHour}</h3>
              <p><strong>${event.stadium.name} à ${
              event.stadium.address
            }</strong></p>
              <p>Opposants : ${nationsHtml}</p>
              <p>
              ${
                event.stadium.available_space === 0
                  ? "Plus de tickets disponibles"
                  : `Il reste ${event.stadium.available_space} places disponibles. 
                <a href="/ticket/${event.id}" class="btn btn-primary">Réserver maintenant</a>`
              }
            </p>
            `; // ATTENTION, IL FAUDRA ENCORE PERSONNALISER LES TICKETS AVEC LA PAGE TICKET

            eventsContainer.appendChild(eventElement);
          });
        })
        .catch((error) => console.error("Error fetching event data:", error));
    });
  });
});
