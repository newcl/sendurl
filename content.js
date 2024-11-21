console.log("Content script loaded.");

chrome.runtime.onMessage.addListener((message) => {
  console.log("Message received in content.js:", message);

  if (message.type === "showToast") {
    // Create toast container if it doesn't exist
    let container = document.getElementById("toast-container");
    if (!container) {
      container = document.createElement("div");
      container.id = "toast-container";
      document.body.appendChild(container);
      console.log("#toast-container added to DOM.");
    }

    // Create toast message
    const toast = document.createElement("div");
    toast.className = "toast";
    toast.textContent = message.message;

    // Append toast to container
    container.appendChild(toast);
    console.log("Toast added to DOM:", toast);

    // Remove toast after 3 seconds
    setTimeout(() => {
      toast.remove();
    }, 3000);
  }
});
