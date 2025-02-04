import os
from aiohttp import web

# Retrieve the bot's username from environment variables.
# Ensure BOT_USERNAME is set in Railway’s environment (without the '@').
BOT_USERNAME = os.environ.get("BOT_USERNAME", "default_bot_username")
if BOT_USERNAME == "default_bot_username":
    print("WARNING: BOT_USERNAME is not set correctly!")

async def index(request):
    # For debugging, log the request details.
    full_url = str(request.url)
    path = request.path
    query_params = dict(request.query)
    print("DEBUG: Full URL:", full_url)
    print("DEBUG: Path:", path)
    print("DEBUG: Query Params:", query_params)
    
    # Look for the "start" query parameter.
    start_param = request.query.get("start")
    if start_param:
        # Build the Telegram deep-link URL.
        # For example: tg://resolve?domain=MyBot&start=<encoded_data>
        deep_link = f"tg://resolve?domain={BOT_USERNAME}&start={start_param}"
        print("DEBUG: Generated deep-link:", deep_link)
        
        # Build an HTML page that immediately attempts to redirect to Telegram.
        html_content = f"""<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Launching Telegram...</title>
    <!-- Use meta-refresh as a fallback -->
    <meta http-equiv="refresh" content="2; url={deep_link}">
    <script type="text/javascript">
      function redirectToTelegram() {{
          window.location.href = "{deep_link}";
          // For some browsers, location.replace may help.
          window.location.replace("{deep_link}");
      }}
      window.onload = function() {{
          setTimeout(redirectToTelegram, 500);
      }};
    </script>
    <style>
      body {{ font-family: sans-serif; text-align: center; padding: 2em; }}
    </style>
  </head>
  <body>
    <p>Attempting to open Telegram...</p>
    <p>If nothing happens, please <a href="{deep_link}">click here</a>.</p>
    <p>(If the browser does not automatically close this page, close it manually.)</p>
  </body>
</html>"""
        return web.Response(text=html_content, content_type="text/html")
    else:
        # If no "start" parameter is provided, simply return a default message.
        return web.Response(text="Codeflix FileStore", content_type="text/plain")

# Create the aiohttp application and register routes.
app = web.Application()
# Explicitly register the root route.
app.router.add_get("/", index)
# Also register a catch-all route (this ensures that if the URL is missing a trailing slash,
# the query string is still processed correctly).
app.router.add_get("/{tail:.*}", index)

if __name__ == '__main__':
    # Railway will provide the PORT environment variable.
    port = int(os.environ.get("PORT", 8080))
    web.run_app(app, host="0.0.0.0", port=port)
