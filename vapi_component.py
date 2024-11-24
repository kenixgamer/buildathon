import streamlit.components.v1 as components
import os

# Get the absolute path to your React component build
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Create the Vapi component
def vapi_widget():
    components.html(
        """
        <div id="vapi-container"></div>
        <script>
          var vapiInstance = null;
          const assistant = "669a5299-6ab1-4bde-a183-f3ca75b59875";
          const apiKey = "5680e105-a9ff-4ed2-a55e-31075962331d";
          const buttonConfig = {
            position: "bottom-left",
            offset: "40px",
            width: "50px",
            height: "50px",
            idle: {
              color: "rgb(93, 254, 202)",
              type: "pill",
              title: "Have a question?",
              subtitle: "Talk with our AI assistant",
              icon: "https://unpkg.com/lucide-static@0.321.0/icons/phone.svg"
            },
            loading: {
              color: "rgb(93, 124, 202)",
              type: "pill",
              title: "Connecting...",
              subtitle: "Please wait",
              icon: "https://unpkg.com/lucide-static@0.321.0/icons/loader-2.svg"
            },
            active: {
              color: "rgb(255, 0, 0)",
              type: "pill",
              title: "Call in progress...",
              subtitle: "End the call",
              icon: "https://unpkg.com/lucide-static@0.321.0/icons/phone-off.svg"
            }
          };

          (function(d, t) {
            var g = document.createElement(t),
              s = d.getElementsByTagName(t)[0];
            g.src = "https://cdn.jsdelivr.net/gh/VapiAI/html-script-tag@latest/dist/assets/index.js";
            g.defer = true;
            g.async = true;
            s.parentNode.insertBefore(g, s);
            g.onload = function() {
              vapiInstance = window.vapiSDK.run({
                apiKey: apiKey,
                assistant: assistant,
                config: buttonConfig
              });
            };
          })(document, "script");
        </script>
        """,
        height=0,
    )