import os
from aiohttp import web

# Retrieve your bot's username from environment variables.
BOT_USERNAME = os.environ.get("BOT_USERNAME", "default_bot_username")

async def index(request):
    # Check for the 'start' query parameter
    start_param = request.rel_url.query.get("start")
    if start_param:
        # Build the Telegram deep link, e.g., tg://resolve?domain=MyBot&start=...
        deep_link = f"tg://resolve?domain={BOT_USERNAME}&start={start_param}"
        
        # Create an HTML page that redirects to Telegram and then attempts to close the window.
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
        # Fallback response if no start parameter is provided
        return web.Response(text="Codeflix FileStore", content_type="text/plain")

# Use a catch-all route so that any GET request (with or without a trailing slash) is handled.
app = web.Application()
app.router.add_get("/{tail:.*}", index)

if __name__ == '__main__':
    # Railway (like Heroku) sets the PORT via an environment variable.
    port = int(os.environ.get("PORT", 8080))
    web.run_app(app, host="0.0.0.0", port=port)
