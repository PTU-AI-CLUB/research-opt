const pdfElement = document.querySelector('embed[type="application/pdf"]');
if (pdfElement) {
  const pdfUrl = pdfElement.getAttribute('src');
  
  chrome.runtime.sendMessage({ action: "summarize_pdf", pdfUrl });
} else {
  console.error('No PDF found on the page.');
}
