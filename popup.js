document.getElementById("summarizeButton").addEventListener("click", () => {
    // Get active tab
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      const activeTab = tabs[0];
      
      // Execute content script
      chrome.scripting.executeScript({
        target: { tabId: activeTab.id },
        files: ['content.js']
      });
    });
  });
  