const summarizeButton = document.getElementById("summarize-button");

summarizeButton.addEventListener("click", async () => {
  console.log("in popup.js");
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    chrome.tabs.sendMessage(tabs[0].id, "summarize");
  });
});
