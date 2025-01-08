document.addEventListener("DOMContentLoaded", function () {
  const sportLinks = document.querySelectorAll(".sport-link");

  sportLinks.forEach((link) => {
    link.addEventListener("click", function (event) {
      event.preventDefault(); // Empêche le comportement par défaut du lien

      const sportId = this.dataset.sportId;

      fetch(`/sport/${sportId}/events/`)
        .then((response) => response.json())
        .then((data) => {
          const sportDetailsDiv = document.getElementById("sport-details");
          sportDetailsDiv.innerHTML = ""; // Réinitialiser le contenu existant

          if (data.events.length > 0) {
            data.events.forEach((event) => {
              const eventElement = document.createElement("div");
              eventElement.classList.add("event");

              let nationsHtml = "";
              event.nations.forEach((nation) => {
                nationsHtml += `
                  <div class="nation">
                    <h4>${nation.name} (${nation.nickname})</h4>
                    <img src="${nation.image_url}" alt="${nation.name}" width="100">
                  </div>
                `;
              });

              eventElement.innerHTML = `
              <h3>${event.date} - ${event.hour}</h3>
              <p><strong>${event.stadium.name} à ${
                event.stadium.address
              }.</strong></p>
              <p>Opposants : ${nationsHtml}</p>
              <p>
                Il reste ${event.stadium.available_space} places disponibles.
                ${
                  event.stadium.available_space > 0
                    ? `<a href="ticket.html?event_id=${event.id}" class="btn btn-primary">Réserver maintenant</a>`
                    : `<span>Plus de places disponibles</span>`
                }
              </p>
            `;

              sportDetailsDiv.appendChild(eventElement);
            });
          } else {
            sportDetailsDiv.innerHTML = "<p>Aucun événement trouvé.</p>";
          }
        })
        .catch((error) => {
          console.error("Erreur lors du chargement des événements:", error);
        });
    });
  });
});
