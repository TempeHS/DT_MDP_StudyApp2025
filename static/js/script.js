import "https://cdn.jsdelivr.net/npm/@popperjs/core@2.10.2/dist/umd/popper.min.js";
import "https://stackpath.bootstrapcdn.com/bootstrap/5.1.3/js/bootstrap.min.js";

document.addEventListener("DOMContentLoaded", function () {
  const sidebar = document.querySelector(".sidebar");
  const content = document.querySelector(".custom-content");

  function handleResize() {
    if (window.innerWidth <= 480) {
      sidebar.classList.add("collapsed");
      content.style.marginLeft = "50px";
    } else if (window.innerWidth <= 768) {
      sidebar.classList.remove("collapsed");
      content.style.marginLeft = "100px";
    } else {
      sidebar.classList.remove("collapsed");
      content.style.marginLeft = "250px";
    }
  }

  window.addEventListener("resize", handleResize);
  handleResize(); // Call once to set the initial state

  // Check if Bootstrap is loaded
  if (typeof bootstrap !== "undefined") {
    console.log("Bootstrap is loaded");
  } else {
    console.error("Bootstrap is not loaded");
  }

  var dropdownElementList = [].slice.call(
    document.querySelectorAll(".dropdown-toggle")
  );
  var dropdownList = dropdownElementList.map(function (dropdownToggleEl) {
    return new bootstrap.Dropdown(dropdownToggleEl);
  });

  var organisationToolsLink = document.getElementById("organisationToolsLink");
  organisationToolsLink.addEventListener("click", function (event) {
    event.preventDefault();
    var modal = new bootstrap.Modal(document.getElementById("exampleModal"));
    modal.show();
  });

  document
    .getElementById("studyToolsButton")
    .addEventListener("click", function () {
      window.location.href = "/study-tools";
    });

  document.getElementById("blogsButton").addEventListener("click", function () {
    window.location.href = "/blogs";
  });
});
