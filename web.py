import os
from aiohttp import web

# Retrieve the bot's username from the environment.
# Ensure you set BOT_USERNAME (without the '@') in your Railway project settings.
BOT_USERNAME = os.environ.get("BOT_USERNAME", "default_bot_username")

async def index(request):
    # Debug logging: log the full URL, path, and query parameters.
    full_url = str(request.url)
    path = request.path
    query_params = dict(request.query)
    print("DEBUG: Full URL:", full_url)
    print("DEBUG: Path:", path)
    print("DEBUG: Query Params:", query_params)
    
    # Get the 'start' query parameter.
    start_param = request.query.get("start")
    if start_param:
        # Build the Telegram deep-link URL.
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
    <p>Redirecting to Telegram… If nothing happens, <a href="{deep_link}">click here</a>.</p>
    <p>If the window does not close automatically, please close it manually.</p>
  </body>
</html>"""
        return web.Response(text=html_content, content_type="text/html")
    else:
        # If no 'start' parameter is found, return a simple debug message.
        return web.Response(
            text=f"No 'start' parameter found.\nPath: {path}\nQuery: {query_params}",
            content_type="text/plain"
        )

# Create the aiohttp application and register routes.
app = web.Application()
# Register the root route explicitly.
app.router.add_get("/", index)
# Also register a catch-all route to handle any path (ensuring that missing trailing slashes aren’t an issue).
app.router.add_get("/{tail:.*}", index)

if __name__ == '__main__':
    # Railway will supply the PORT via an environment variable.
    port = int(os.environ.get("PORT", 8080))
    web.run_app(app, host="0.0.0.0", port=port)
