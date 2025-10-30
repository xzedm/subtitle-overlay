// Popup script to show connection status
document.addEventListener("DOMContentLoaded", () => {
  const indicator = document.getElementById("indicator");
  const statusText = document.getElementById("statusText");
  const testBtn = document.getElementById("testBtn");
  const pageStatus = document.getElementById("pageStatus");
  const note = document.getElementById("note");

  // Check current tab URL
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    if (tabs[0]) {
      const url = tabs[0].url;
      const supportedSites = [
        "netflix.com",
        "youtube.com",
        "amazon.com",
        "disneyplus.com",
        "hulu.com",
        "hbomax.com",
        "rezka"
      ];
      
      const isSupported = supportedSites.some(site => url.includes(site));
      
      if (isSupported) {
        pageStatus.innerHTML = '<span style="color: green;">✓ Current page is supported</span>';
      } else {
        pageStatus.innerHTML = '<span style="color: orange;">⚠ Navigate to a streaming site</span>';
        note.style.display = "block";
      }
    }
  });

  // Test connection function
  function testConnection() {
    indicator.className = "indicator testing";
    statusText.textContent = "Testing...";
    testBtn.disabled = true;
    testBtn.textContent = "Testing...";

    let connectionSuccess = false;
    const ws = new WebSocket("ws://127.0.0.1:8765");
    
    const timeout = setTimeout(() => {
      if (!connectionSuccess) {
        ws.close();
        indicator.className = "indicator disconnected";
        statusText.textContent = "❌ Connection timeout";
        testBtn.disabled = false;
        testBtn.textContent = "Test Connection";
      }
    }, 3000);

    ws.onopen = () => {
      connectionSuccess = true;
      clearTimeout(timeout);
      indicator.className = "indicator connected";
      statusText.textContent = "✓ Connected to desktop app";
      
      // Send test message
      try {
        ws.send(JSON.stringify({
          type: "subtitle",
          text: "Extension test: Connection successful! 🎉",
          timestamp: Date.now()
        }));
      } catch (e) {
        console.log("Send failed:", e);
      }
      
      // Close after sending
      setTimeout(() => {
        ws.close(1000, "Test complete");
        testBtn.disabled = false;
        testBtn.textContent = "Test Connection";
      }, 500);
    };

    ws.onerror = (error) => {
      console.log("WebSocket error:", error);
      if (!connectionSuccess) {
        clearTimeout(timeout);
        indicator.className = "indicator disconnected";
        statusText.textContent = "❌ Desktop app not running";
        testBtn.disabled = false;
        testBtn.textContent = "Test Connection";
      }
    };

    ws.onclose = (event) => {
      console.log("WebSocket closed:", event.code, event.reason);
      // Only show error if connection was never successful
      if (!connectionSuccess) {
        clearTimeout(timeout);
        indicator.className = "indicator disconnected";
        statusText.textContent = "❌ Connection failed";
        testBtn.disabled = false;
        testBtn.textContent = "Test Connection";
      }
    };
  }

  // Initial status check
  chrome.runtime.sendMessage({ type: "get_status" }, (response) => {
    if (response && response.connected) {
      indicator.classList.add("connected");
      statusText.textContent = "✓ Connected to desktop app";
    } else {
      indicator.classList.add("disconnected");
      statusText.textContent = "Click 'Test Connection'";
    }
  });

  // Test button click handler
  testBtn.addEventListener("click", testConnection);
  
  // Auto-test on load
  setTimeout(testConnection, 500);
});
