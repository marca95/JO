function safe(idForInput) {
  let password1 = document.getElementById(idForInput);
  let safetyPolicy = document.querySelectorAll(".safety_policy");

  password1.addEventListener("input", () => {
    data = password1.value;

    if (data.length >= 8) {
      safetyPolicy[0].style.color = "green";
    } else {
      safetyPolicy[0].style.color = "red";
    }

    let number = /\d/.test(data);
    if (number) {
      safetyPolicy[1].style.color = "green";
    } else {
      safetyPolicy[1].style.color = "red";
    }

    let upperCase = /[A-Z]/.test(data);
    if (upperCase) {
      safetyPolicy[2].style.color = "green";
    } else {
      safetyPolicy[2].style.color = "red";
    }

    let specialChar = /[?!,@.]/.test(data);
    if (specialChar) {
      safetyPolicy[3].style.color = "green";
    } else {
      safetyPolicy[3].style.color = "red";
    }
  });
}
