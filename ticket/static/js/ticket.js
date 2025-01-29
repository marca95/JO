document.addEventListener("DOMContentLoaded", function () {
  const sportLinks = document.querySelectorAll(".sport-link");
  const eventsContainer = document.getElementById("sport-details");

  const firstSportName = sportLinks[0].dataset.sportName;
  loadEvents(firstSportName);

  function loadEvents(sportName) {
    fetch(`${sportName}/`)
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

          let ticketOffre;
          if (event.stadium.available_space === 0) {
            ticketOffre = `<p class="fs-4 fw-bolder" style="color: red;">Plus de ticket disponible</p>`;
          } else if (
            event.stadium.available_space === undefined ||
            event.stadium.available_space === null
          ) {
            ticketOffre = `<p class="fs-4 fw-bolder" style="color: red;">Erreur lors du téléchargement.</p>`;
          } else if (event.tickets.length === 0) {
            ticketOffre = `<p class="fs-4 fw-bolder" style="color: red;">Ticket pas encore disponible</p>`;
          } else {
            const ticketDetails = event.tickets
              .map((ticket) => {
                const isAvailable =
                  ticket.nbr_place <= event.stadium.available_space;
                return `<div class="ticket-info row fw-bolder text-center">
                <p class="col-4 col-sm-2 mt-2">${ticket.nbr_place}</p>
                <p class="col-4 col-sm-2 text-capitalize mt-2">${
                  ticket.formula
                }</p>
                <p class="col-4 col-sm-2 mt-2">${ticket.price}</p>
                <button class="col-12 col-sm-6 add_cart ${
                  isAvailable ? "" : "btn-disabled"
                }" value="${ticket.id}" ${isAvailable ? "" : "disabled"}>${
                  isAvailable ? "Ajouter au panier" : "Plus de place suffisante"
                }
                </button>
              </div>`;
              })
              .join("");
            ticketOffre = `
              <p class="fs-5 fw-bolder text-center">Il reste ${event.stadium.available_space} places disponibles.</p>
              <h6 class="fs-4 text-decoration-underline mb-4">Offre :</h6>
              <p class="fs-5 fw-bolder text-center">Choisissez vos quantités dans votre panier personnel.</p>
              <div class="ticket-info row  fw-bolder text-center"><p class="col-4 col-sm-2">Place</p> <p class="col-4 col-sm-2 text-capitalize mb-5">Formule</p> <p class="col-4 col-sm-2">€</p> <p class="d-none d-sm-block col-6">Panier</p>

              ${ticketDetails} 
              <div class="centr_button"><a href="/panier/" class="button">Accéder au panier</a></div>
              </div>
            `;
          }
          eventElement.innerHTML = `
            <div class="d-flex flex-column align-items-center toto">
            <div class="opposition d-flex justify-content-between align-items-center w-100">
              ${nationsHtml}
            </div>
            <p class="fs-5 fst-italic fw-bolder">${event.date} à ${event.hour}</p>
            <p class="fs-5 fst-italic fw-bolder">${event.stadium.name} à ${event.stadium.address}</p>
            <div class="">${ticketOffre}</div>
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
      nationsHtml = `<span class="mx-auto fw-semibold fs-4 text-danger">Match encore désigné.</span>`;
    }

    return nationsHtml;
  }

  sportLinks.forEach((link) => {
    link.addEventListener("click", function (event) {
      event.preventDefault();
      const sportName = link.dataset.sportName;
      loadEvents(sportName);
    });
  });
});

document.addEventListener("click", (e) => {
  if (e.target.classList.contains("add_cart")) {
    e.preventDefault();

    let storedTickets = JSON.parse(localStorage.getItem("tickets")) || [];

    const ticketId = e.target.value;

    if (storedTickets.includes(ticketId)) {
      storedTickets = storedTickets.filter((id) => id !== ticketId);
      e.target.style.backgroundColor = "red";
      e.target.textContent = "Ticket retiré";
      setTimeout(() => {
        e.target.style.backgroundColor = "#0080ff";
        e.target.textContent = "Ajouter au panier";
      }, 1500);
    } else {
      storedTickets.push(ticketId);
      e.target.style.backgroundColor = "green";
      e.target.textContent = "Ticket ajouté!";
    }

    localStorage.setItem("tickets", JSON.stringify(storedTickets));
  }

  updateCart();
});
