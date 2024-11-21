chrome.action.onClicked.addListener(async (tab) => {
  if (
    !tab.url ||
    tab.url.startsWith("chrome://") ||
    tab.url.startsWith("chrome-extension://")
  ) {
    console.error("Cannot process this page.");
    return;
  }

  const apiUrl = "http://127.0.0.1:5000/process"; // Replace with your API URL

  try {
    // Make the API call with the current tab's URL
    const response = await fetch(apiUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ url: tab.url }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const responseData = await response.json();

    // Display a notification with the API response
    chrome.notifications.create({
      type: "basic",
      iconUrl: "icon.png", // Add an icon.png in your extension directory
      title: "API Response",
      message: responseData.response,
    });
  } catch (error) {
    console.error("Error during API call:", error);

    // Display an error notification
    chrome.notifications.create({
      type: "basic",
      iconUrl: "icon.png",
      title: "Error",
      message: error.message,
    });
  }
});
