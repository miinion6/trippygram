from aiohttp import web
import base64

routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    return web.json_response("Codeflix FileStore")

@routes.get("/", allow_head=True)
async def handle_start(request):
    """Handles requests with the ?start= parameter."""
    start_param = request.rel_url.query.get("start")

    if start_param:
        try:
            # Decode the base64 string (if necessary)
            decoded_data = base64.urlsafe_b64decode(start_param).decode("utf-8")
        except Exception:
            return web.json_response({"error": "Invalid start parameter"}, status=400)

        # Now, process the decoded data (e.g., fetch file info, generate a download link, etc.)
        return web.json_response({"message": f"Processing request: {decoded_data}"})

    return web.json_response({"error": "Missing 'start' parameter"}, status=400)

# Create the aiohttp application and add routes
app = web.Application()
app.add_routes(routes)

# Run the web app on Heroku
if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
