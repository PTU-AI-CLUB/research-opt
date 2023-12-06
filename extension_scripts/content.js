if (document.URL.endsWith('.pdf')) {
  const filePath = document.URL;
  console.log("in content.js");
  chrome.runtime.sendMessage({
    action: 'summarizePDF',
    filePath
  });
} else {
  // Handle non-PDF context
  console.log('This script only works for PDF files.');
}
