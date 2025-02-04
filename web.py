import os
from aiohttp import web

# Retrieve your bot's username from environment variables.
# Make sure you set BOT_USERNAME in your Heroku config (without the @).
BOT_USERNAME = os.environ.get("BOT_USERNAME", "default_bot_username")

async def index(request):
    # Check if the 'start' query parameter is provided.
    start_param = request.rel_url.query.get("start")
    if start_param:
        # Build the Telegram deep link. For example:
        # tg://resolve?domain=MyBot&start=<start_param>
        deep_link = f"tg://resolve?domain={BOT_USERNAME}&start={start_param}"
        
        # Return an HTML page that automatically redirects to Telegram.
        html_content = f"""<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <meta http-equiv="refresh" content="0; url={deep_link}">
    <script type="text/javascript">
      window.location.href = "{deep_link}";
    </script>
    <title>Launching Telegram</title>
  </head>
  <body>
    <p>If you are not redirected automatically, <a href="{deep_link}">click here</a> to open Telegram.</p>
  </body>
</html>"""
        return web.Response(text=html_content, content_type='text/html')
    else:
        # No start parameter provided – show a simple message.
        return web.Response(text="Welcome to Codeflix FileStore")

# Set up the aiohttp application and add the route.
app = web.Application()
app.router.add_get("/", index)

if __name__ == '__main__':
    # Heroku provides the PORT via an environment variable.
    port = int(os.environ.get("PORT", 8080))
    web.run_app(app, host="0.0.0.0", port=port)
