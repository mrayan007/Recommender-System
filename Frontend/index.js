const div = document.querySelector("div");
const text = document.querySelector("textarea");
const popup = document.getElementById("popup");
const popuptext = document.querySelector("#popup span");

const API_URL = "http://localhost:8000";

function FetchAPI() {
  fetch(API_URL)
    .then(response => response.json())
    .then(data => div.textContent = data)
    .catch(error => console.log(error));
}

function Submit() {
  const response = text.value === "" ? "Please insert a student profile" : text.value;

  popuptext.textContent = response;
  popup.classList.toggle("scale-0");
}
