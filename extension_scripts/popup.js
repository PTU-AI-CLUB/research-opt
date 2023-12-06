document.addEventListener("DOMContentLoaded", function() {
  const summarizeButton = document.getElementById('summarize-button');

  if (summarizeButton) {
      summarizeButton.addEventListener('click', () => {
        console.log("In popup.js");
        chrome.runtime.sendMessage({
          action: 'summarizePDF'
        });
      });
  } else {
    console.error("summarizeButton not found!");
  }
});