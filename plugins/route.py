import os
from aiohttp import web

# Use your existing configuration variable for the bot's username.
# (Make sure BOT_USERNAME is set in your Railway environment.)
BOT_USERNAME = os.environ.get("BOT_USERNAME", "default_bot_username")
if BOT_USERNAME == "default_bot_username":
    print("WARNING: BOT_USERNAME is not set correctly!")

async def redirect_handler(request):
    # Log details for debugging (you can remove or comment out these prints later)
    full_url = str(request.url)
    path = request.path
    query_params = dict(request.query)
    print("DEBUG: Full URL:", full_url)
    print("DEBUG: Path:", path)
    print("DEBUG: Query Params:", query_params)
    
    # Check for the "start" parameter
    start_param = request.query.get("start")
    if start_param:
        # Build the Telegram deep-link using your existing BOT_USERNAME variable.
        deep_link = f"tg://resolve?domain={BOT_USERNAME}&start={start_param}"
        print("DEBUG: Generated deep-link:", deep_link)
        
        # Build the HTML content that will redirect to Telegram.
        html_content = f"""<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Launching Telegram...</title>
    <!-- Meta-refresh as a fallback (2-second delay) -->
    <meta http-equiv="refresh" content="2; url={deep_link}">
    <script type="text/javascript">
      function redirectToTelegram() {{
          window.location.href = "{deep_link}";
          window.location.replace("{deep_link}");
      }}
      // Wait 500ms, then try to redirect
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
        # When no start parameter is provided, return a default message.
        return web.Response(
            text="No 'start' parameter provided. This page is for Telegram deep-link redirection.",
            content_type="text/plain"
        )

# Create the application and register the routes.
app = web.Application()
# Register the root URL explicitly.
app.router.add_get("/", redirect_handler)
# Also register a catch-all so that if the URL is missing a trailing slash the query is still processed.
app.router.add_get("/{tail:.*}", redirect_handler)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    web.run_app(app, host="0.0.0.0", port=port)
