chrome.action.onClicked.addListener(async (tab) => {
  if(tab.url.endsWith(".pdf"))
  {
    fetch('http://localhost:5000/process_pdf',{
      method: 'POST',
      body : JSON.stringify({'filePath' : tab.url}),
      mode : 'cors',
      headers : {
        'Content-type' : 'application/json'
      }
    })
    .then(r => r.json())
    .then(r => {
      console.log(r.message);
    }).catch((error) => {
      console.error('Error:', error);
    });
    }
  }
);

chrome.webRequest.onBeforeSendHeaders.addListener(
  (details) => {
    if (details.url.startsWith("http://localhost:5000/process_pdf")) {
      details.requestHeaders.push({
        name: "Access-Control-Allow-Origin",
        value: "*"
      });
      details.requestHeaders.push({
        name: "Access-Control-Allow-Methods",
        value: "GET, POST, PUT, DELETE, OPTIONS"
      });
    }
    return {requestHeaders: details.requestHeaders};
  },
  {urls: ["<all_urls>"]},
  ["blocking"]
);