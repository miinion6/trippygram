import os
from aiohttp import web

# Retrieve your bot's username using your existing configuration variable name.
BOT_USERNAME = os.environ.get("BOT_USERNAME", "default_bot_username")
if BOT_USERNAME == "default_bot_username":
    print("WARNING: BOT_USERNAME is not set correctly in your environment!")

async def index(request):
    # Debug: Log the full URL, path, and query parameters
    full_url = str(request.url)
    path = request.path
    query_params = dict(request.query)
    print("DEBUG: Full URL:", full_url)
    print("DEBUG: Path:", path)
    print("DEBUG: Query Params:", query_params)
    
    # Check if the "start" query parameter is present.
    start_param = request.query.get("start")
    if start_param:
        # Build the Telegram deep‑link using your BOT_USERNAME.
        deep_link = f"tg://resolve?domain={BOT_USERNAME}&start={start_param}"
        print("DEBUG: Generated deep-link:", deep_link)
        
        # Build an HTML page that attempts to redirect to Telegram.
        html_content = f"""<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Launching Telegram...</title>
    <!-- Meta-refresh (2-second delay as fallback) -->
    <meta http-equiv="refresh" content="2; url={deep_link}">
    <script type="text/javascript">
      function redirectToTelegram() {{
          window.location.href = "{deep_link}";
          window.location.replace("{deep_link}");
      }}
      window.onload = function() {{
          setTimeout(redirectToTelegram, 500);
      }};
    </script>
    <style>
      body {{
        font-family: Arial, sans-serif;
        text-align: center;
        padding-top: 50px;
      }}
    </style>
  </head>
  <body>
    <p>Attempting to open Telegram...</p>
    <p>If nothing happens, please <a href="{deep_link}">click here</a>.</p>
    <p>(If the page does not close automatically, please close it manually.)</p>
  </body>
</html>"""
        return web.Response(text=html_content, content_type="text/html")
    else:
        # If no "start" parameter is provided, return a default message.
        return web.Response(
            text="No 'start' parameter provided. This page is for Telegram deep-link redirection.",
            content_type="text/plain"
        )

# Create the aiohttp application and register the routes.
app = web.Application()
# Explicitly register the root route.
app.router.add_get("/", index)
# Also register a catch-all route (handles cases where the trailing slash might be omitted).
app.router.add_get("/{tail:.*}", index)

if __name__ == "__main__":
    # Railway provides the PORT environment variable.
    port = int(os.environ.get("PORT", 8080))
    web.run_app(app, host="0.0.0.0", port=port)
