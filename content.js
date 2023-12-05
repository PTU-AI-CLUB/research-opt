const pdfElement = document.querySelector('embed[type="application/pdf"]');
if (pdfElement) {
  const pdfUrl = pdfElement.getAttribute('src');
  console.log("In content.js");
  chrome.runtime.sendMessage({ action: "summarizePDF", pdfUrl });
} else {
  console.error('No PDF found on the page.');
}
