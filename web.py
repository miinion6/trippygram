import os
from aiohttp import web

# Get the bot's username from environment variables.
BOT_USERNAME = os.environ.get("BOT_USERNAME", "default_bot_username")

async def index(request):
    # Log the full URL, path, and query parameters for debugging.
    full_url = str(request.url)
    path = request.path
    query_params = dict(request.query)
    print("DEBUG: Full URL:", full_url)
    print("DEBUG: Path:", path)
    print("DEBUG: Query params:", query_params)
    
    # Look for the 'start' query parameter.
    start_param = request.query.get("start")
    
    if start_param:
        # Build the Telegram deep-link.
        deep_link = f"tg://resolve?domain={BOT_USERNAME}&start={start_param}"
        
        # Build an HTML page that attempts to redirect to Telegram and then close the window.
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
        # If no 'start' parameter is found, return the fallback along with debugging info.
        return web.Response(
            text=f"No 'start' parameter found.\nPath: {path}\nQuery: {query_params}",
            content_type="text/plain"
        )

# Register both the explicit root and a catch-all route.
app = web.Application()
app.router.add_get("/", index)
app.router.add_get("/{tail:.*}", index)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    web.run_app(app, host="0.0.0.0", port=port)
