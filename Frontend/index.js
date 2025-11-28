const div = document.querySelector("div");

const API_URL = "http://localhost:8001"

function FetchAPI() {
  fetch(API_URL)
    .then(response => response.text())
    .then(data => div.textContent = data)
    .catch(error => div.textContent = console.log(error))
}
