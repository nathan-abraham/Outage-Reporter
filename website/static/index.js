// Get form objects
const reportForm = document.getElementById("reportForm");
const findForm = document.getElementById("findForm");

if (reportForm != null) {
  // Check if the form entries are valid and cancel the request if not
  reportForm.addEventListener("submit", (event) => {
    if (!reportForm.checkValidity()) {
      event.preventDefault();
      event.stopPropagation();
      reportForm.classList.add("was-validated");
    }
  });
}

// Check if the form entries are valid and cancel the request if not
findForm.addEventListener("submit", (event) => {
  if (!findForm.checkValidity()) {
    event.preventDefault();
    event.stopPropagation();
    findForm.classList.add("was-validated");
  }
});

function findReport(zipCode, city) {
  // Send POST request to URL endpoint
  fetch("/find-submit", {
    method: "POST",
    body: JSON.stringify({zipCode: zipCode, city: city}),
  }).then((_res) => {
    // Reload window on resolution
    window.location.href = "/find"
  })
}
