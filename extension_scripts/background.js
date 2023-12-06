const url = 'http://localhost:5000/process_pdf'; // Change to your backend URL

function summarizePdf(filePath) {
  console.log("In bg.js")
  fetch(url, {
    method: 'POST',
    body: JSON.stringify({ filePath }),
    headers: {
      'Content-Type': 'application/json'
    }
  })
  .then(response => response.json())
  .then(data => {
    // Handle success response (e.g., show download notification)
  })
  .catch(error => {
    // Handle error
  });
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === 'summarizePDF') {
    summarizePdf(message.filePath);
  }
});
