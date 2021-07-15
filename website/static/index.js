// Get form objects
const reportForm = document.getElementById("reportForm");
const findForm = document.getElementById("findForm");

const detailsTextArea = document.getElementById("detailsTextArea")

// Change textarea height based on screen size
if (detailsTextArea != null) {
  if ($(window).height() < 576)
    detailsTextArea.rows = 3;
}


if (reportForm != null) {
  // Check if the form entries are valid and cancel the request if not
  reportForm.addEventListener("submit", (event) => {
    if (!reportForm.checkValidity()) {
      event.preventDefault();
      event.stopPropagation();
      reportForm.classList.add("was-validated");
    }
  });

  // Space out columns
  const formColumns = document.querySelectorAll("[data-column]");
  formColumns.forEach((column) => {
    column.classList.add("form-group");
  });
}

// Check if the form entries are valid and cancel the request if not
if (findForm != null) {
  findForm.addEventListener("submit", (event) => {
    if (!findForm.checkValidity()) {
      event.preventDefault();
      event.stopPropagation();
      findForm.classList.add("was-validated");
    }
  });
}

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
