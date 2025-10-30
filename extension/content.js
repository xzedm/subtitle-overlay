// Subtitle detection for various streaming platforms
class SubtitleDetector {
  constructor() {
    this.lastSubtitle = "";
    this.websocket = null;
    this.connectToServer();
    this.startDetection();
  }

  connectToServer() {
    try {
      this.websocket = new WebSocket("ws://127.0.0.1:8765");

      this.websocket.onopen = () => {
        console.log("Connected to subtitle overlay app");
        this.sendConnectionStatus(true);
      };

      this.websocket.onclose = () => {
        console.log("Disconnected from subtitle overlay app");
        this.sendConnectionStatus(false);
        // Attempt to reconnect after 5 seconds
        setTimeout(() => this.connectToServer(), 5000);
      };

      this.websocket.onerror = (error) => {
        console.error("WebSocket error:", error);
      };
    } catch (error) {
      console.error("Failed to connect:", error);
      setTimeout(() => this.connectToServer(), 5000);
    }
  }

  sendSubtitle(text) {
    if (this.websocket && this.websocket.readyState === WebSocket.OPEN) {
      // Only send if subtitle has changed
      if (text !== this.lastSubtitle) {
        this.lastSubtitle = text;
        this.websocket.send(
          JSON.stringify({
            type: "subtitle",
            text: text,
            timestamp: Date.now(),
            url: window.location.href,
          })
        );
      }
    }
  }

  sendConnectionStatus(connected) {
    chrome.runtime.sendMessage({
      type: "connection_status",
      connected: connected,
    });
  }

  startDetection() {
    const hostname = window.location.hostname;

    if (hostname.includes("netflix.com")) {
      this.detectNetflix();
    } else if (hostname.includes("youtube.com")) {
      this.detectYouTube();
    } else if (hostname.includes("amazon.com")) {
      this.detectAmazon();
    } else if (hostname.includes("disneyplus.com")) {
      this.detectDisneyPlus();
    } else if (hostname.includes("hulu.com")) {
      this.detectHulu();
    } else if (hostname.includes("hbomax.com")) {
      this.detectHBOMax();
    } else if (hostname.includes("rezka")) {
      this.detectRezka();
    } else {
      this.detectGeneric();
    }
  }

  detectNetflix() {
    setInterval(() => {
      // Netflix subtitle container
      const subtitleContainer = document.querySelector(
        ".player-timedtext-text-container"
      );
      if (subtitleContainer) {
        const text = subtitleContainer.innerText.trim();
        if (text) {
          this.sendSubtitle(text);
        }
      }
    }, 200);
  }

  detectYouTube() {
    setInterval(() => {
      // YouTube subtitle container
      const subtitleContainer = document.querySelector(".ytp-caption-segment");
      if (subtitleContainer) {
        const text = subtitleContainer.innerText.trim();
        if (text) {
          this.sendSubtitle(text);
        }
      }
    }, 200);
  }

  detectAmazon() {
    setInterval(() => {
      // Amazon Prime subtitle container
      const subtitleContainer = document.querySelector(
        ".atvwebplayersdk-captions-text"
      );
      if (subtitleContainer) {
        const text = subtitleContainer.innerText.trim();
        if (text) {
          this.sendSubtitle(text);
        }
      }
    }, 200);
  }

  detectDisneyPlus() {
    setInterval(() => {
      // Disney+ subtitle container
      const subtitleContainer = document.querySelector(
        ".dss-subtitle-renderer-cue"
      );
      if (subtitleContainer) {
        const text = subtitleContainer.innerText.trim();
        if (text) {
          this.sendSubtitle(text);
        }
      }
    }, 200);
  }

  detectHulu() {
    setInterval(() => {
      // Hulu subtitle container
      const subtitleContainer = document.querySelector(".caption-text-box");
      if (subtitleContainer) {
        const text = subtitleContainer.innerText.trim();
        if (text) {
          this.sendSubtitle(text);
        }
      }
    }, 200);
  }

  detectHBOMax() {
    setInterval(() => {
      // HBO Max subtitle container
      const subtitleContainer = document.querySelector(
        ".class-for-hbo-subtitles"
      ); // Update this
      if (subtitleContainer) {
        const text = subtitleContainer.innerText.trim();
        if (text) {
          this.sendSubtitle(text);
        }
      }
    }, 200);
  }

  detectRezka() {
    console.log("Rezka subtitle detector activated");
    
    setInterval(() => {
      // Try multiple selectors for Rezka subtitles
      const selectors = [
        "#oframecdnplayer span",  // Rezka CDN player subtitles
        "pjsdiv span",             // Rezka player div subtitles
        ".b-player__subtitle",
        ".pgs-subtitle",
        ".subtitle-text",
        ".vjs-text-track-display",
        "#subtitle-display",
        ".player-subs",
        ".rezka-subtitle"
      ];

      for (const selector of selectors) {
        const subtitleContainer = document.querySelector(selector);
        if (subtitleContainer) {
          const text = subtitleContainer.innerText.trim();
          if (text) {
            console.log(`Rezka subtitle detected (${selector}): ${text}`);
            this.sendSubtitle(text);
            return;
          }
        }
      }

      // Also try HTML5 video text tracks as fallback
      const video = document.querySelector("video");
      if (video && video.textTracks && video.textTracks.length > 0) {
        for (let i = 0; i < video.textTracks.length; i++) {
          const track = video.textTracks[i];
          if (track.mode === "showing" && track.activeCues && track.activeCues.length > 0) {
            const cue = track.activeCues[0];
            const text = cue.text;
            if (text) {
              console.log(`Rezka subtitle from text track: ${text}`);
              this.sendSubtitle(text);
              return;
            }
          }
        }
      }
    }, 200);
  }

  detectGeneric() {
    // Generic detection for HTML5 video text tracks
    setInterval(() => {
      const video = document.querySelector("video");
      if (video && video.textTracks && video.textTracks.length > 0) {
        const track = video.textTracks[0];
        if (track.activeCues && track.activeCues.length > 0) {
          const cue = track.activeCues[0];
          const text = cue.text;
          if (text) {
            this.sendSubtitle(text);
          }
        }
      }
    }, 200);
  }
}

// Initialize detector
const detector = new SubtitleDetector();
