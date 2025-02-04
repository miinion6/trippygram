import os
from aiohttp import web

# Get the bot's username from the environment.
BOT_USERNAME = os.environ.get("BOT_USERNAME", "default_bot_username")

async def index(request):
    # Log the incoming URL for debugging.
    print("Incoming request:", request.rel_url)
    # Try to retrieve the 'start' query parameter.
    start_param = request.rel_url.query.get("start")
    
    if start_param:
        # Build the Telegram deep-link.
        deep_link = f"tg://resolve?domain={BOT_USERNAME}&start={start_param}"
        
        # Build an HTML page that attempts to redirect to Telegram and auto-close.
        html_content = f"""<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Launching Telegram...</title>
    <meta http-equiv="refresh" content="2; url={deep_link}">
    <script type="text/javascript">
      function redirectAndClose() {{
          window.location.href = "{deep_link}";
          setTimeout(function() {{
              window.open('', '_self', '');
              window.close();
          }}, 1500);
      }}
      window.onload = redirectAndClose;
    </script>
  </head>
  <body>
    <p>Redirecting to Telegram… If nothing happens, <a href="{deep_link}">click here</a> to open Telegram.</p>
    <p>If the window does not close automatically, please close it manually.</p>
  </body>
</html>"""
        return web.Response(text=html_content, content_type="text/html")
    else:
        # Fallback response when no 'start' parameter is found.
        return web.Response(text="Codeflix FileStore", content_type="text/plain")

# Create the application and register routes:
app = web.Application()
# Explicitly register the root route.
app.router.add_get("/", index)
# Also register a catch-all route to handle requests that might not include the trailing slash.
app.router.add_get("/{tail:.*}", index)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    web.run_app(app, host="0.0.0.0", port=port)
