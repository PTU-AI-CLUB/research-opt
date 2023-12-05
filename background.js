chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "summarize_pdf") {
      const pdfData = message.pdfData;
  
      // Use fetch or other means to send the PDF data to your Python script
      // Example:
      fetch('http://localhost:5000/summarize', {
        method: 'POST',
        body: JSON.stringify({ pdfData }),
        headers: {
          'Content-Type': 'application/json'
        }
      })
      .then(response => response.json())
      .then(data => {
        // Handle the summarized data here, e.g., download it
      })
      .catch(error => console.error('Error:', error));
    }
  });
  