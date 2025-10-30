// Background script for managing connection state
let connectionStatus = false;

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "connection_status") {
    connectionStatus = message.connected;

    // Update badge to show connection status
    chrome.action.setBadgeText({
      text: connectionStatus ? "●" : "○",
    });

    chrome.action.setBadgeBackgroundColor({
      color: connectionStatus ? "#00FF00" : "#FF0000",
    });
  }

  if (message.type === "get_status") {
    sendResponse({ connected: connectionStatus });
  }
});

// Initialize badge
chrome.action.setBadgeText({ text: "○" });
chrome.action.setBadgeBackgroundColor({ color: "#FF0000" });
