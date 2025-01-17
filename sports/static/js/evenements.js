document.addEventListener("DOMContentLoaded", function () {
  const sportLinks = document.querySelectorAll(".sport-link");
  const eventsContainer = document.getElementById("sport-details");

  const firstSportId = sportLinks[0].dataset.sportName;
  loadEvents(firstSportId);

  function loadEvents(sport_name) {
    fetch(`/${sport_name}/events/`)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Erreur réseau lors de la récupération des données.");
        }
        return response.json();
      })
      .then((data) => {
        const backgroundBlur =
          eventsContainer.querySelector(".background-blur");
        const contentContainer = eventsContainer.querySelector(".content");

        contentContainer.innerHTML = "";

        const sportImageUrl = data.sport_image_url;
        if (sportImageUrl) {
          backgroundBlur.style.backgroundImage = `url(${sportImageUrl})`;
          backgroundBlur.style.backgroundSize = "cover";
          backgroundBlur.style.backgroundPosition = "center";
        } else {
          backgroundBlur.style.backgroundImage = "none";
        }

        data.events.forEach((event, index) => {
          const eventElement = document.createElement("div");
          eventElement.classList.add(
            "col-12",
            "col-xl-6",
            "layout_card",
            "mb-4"
          );

          const nationsHtml = generateNationsHtml(event);
          eventElement.innerHTML = `
    <div class="d-flex flex-column align-items-center toto">
        <div class="opposition d-flex justify-content-between align-items-center w-100">
            ${nationsHtml}
        </div>
        <p class="fs-5 fst-italic fw-bolder">${event.date} à ${event.hour}</p>
        <p class="fs-5 fst-italic fw-bolder">${event.stadium.name} à ${
            event.stadium.address
          }</p>
          <p class="fs-5 fst-italic fw-bolder">
        ${
          event.stadium.available_space === 0
            ? `<p class="fs-4 fw-bolder" style="color: red;">Plus de ticket disponible</p>`
            : `Il reste ${event.stadium.available_space} places disponibles. 
                <p class="centr_button"><a href="/ticket/${sport_name}/events/${event.id}" class="button">Réserver maintenant</a></p>`
        }</p>
    </div>
`;

          contentContainer.appendChild(eventElement);

          if (
            index === data.events.length - 1 &&
            data.events.length % 2 !== 0
          ) {
            eventElement.classList.add("mx-auto");
          }
        });
      })
      .catch((error) =>
        console.error("Erreur lors du chargement des événements:", error)
      );
  }

  function generateNationsHtml(event) {
    let nationsHtml = "";

    if (event.nations && event.nations.length > 0) {
      nationsHtml = event.nations
        .map((nation) => {
          return `<div class="d-flex flex-column align-items-center text-center">
              <img src="${nation.image_url}" alt="${nation.name}" class="flag-img" style="max-height: 100px; max-width: 160px">
              <span class="fs-5 fw-bolder mt-2">${nation.name}</span>
            </div>`;
        })
        .join(" / ");
    } else if (event.players && event.players.length > 0) {
      if (event.players.length > 4) {
        nationsHtml = `<span>${event.players.length} sportifs participants</span>`;
      } else {
        nationsHtml = event.players
          .map((player) => {
            return `<div class="d-flex flex-column align-items-center text-center">
                <img src="${player.image_url}" alt="${player.first_name} ${player.last_name}" class="player-img" style="max-height: 100px;">
                <span class="fs-5 fw-bolder mt-2">${player.first_name} ${player.last_name}</span>
              </div>`;
          })
          .join(" / ");
      }
    } else {
      nationsHtml = `<span>Pas encore désigné.</span>`;
    }

    return nationsHtml;
  }

  sportLinks.forEach((link) => {
    link.addEventListener("click", function (event) {
      event.preventDefault();
      const sportName = this.dataset.sportName;
      loadEvents(sportName);
    });
  });
});
