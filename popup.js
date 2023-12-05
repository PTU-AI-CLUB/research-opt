document.addEventListener("DOMContentLoaded", function() {
  const summarizeButton = document.getElementById("summarizeButton");
  console.log("In popup.js");

  // Check if the button exists before adding the event listener
  if (summarizeButton) {
    summarizeButton.addEventListener("click", () => {
      // Send a message to background.js on button click
      chrome.runtime.sendMessage({ action: "summarizePDF" }, (response) => {
        // Handle response from background.js if needed
      });
    });
  } else {
    console.error("summarizeButton not found!");
  }
});
