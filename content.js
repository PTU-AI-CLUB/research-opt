const pdfData = /* Logic to get PDF data */

chrome.runtime.sendMessage({ action: "summarize_pdf", pdfData });
