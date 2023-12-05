chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "summarize_pdf") {
    const pdfUrl = message.pdfUrl;
    sendPDFUrlToBackend(pdfUrl)
      .then(() => {
        informUser("PDF Summarization in progress...");
      })
      .catch(error => console.error('Error sending PDF URL:', error));
  }
});

function sendPDFUrlToBackend(pdfUrl) {
  return fetch('http://localhost:5000/process_pdf', {
    method: 'POST',
    body: JSON.stringify({ pdfUrl }),
    headers: {
      'Content-Type': 'application/json'
    }
  })
  .catch(error => Promise.reject(error));
}

function informUser(message) {
  chrome.notifications.create({
    type: 'basic',
    iconUrl: 'hello_extensions.png', 
    title: 'PDF Processing',
    message: message
  });
}
