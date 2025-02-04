from aiohttp import web
import base64
import os  # For getting the PORT environment variable

routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    # Check for the "start" query parameter
    start_param = request.rel_url.query.get("start")
    
    if start_param:
        try:
            # Decode the base64 string (if it was encoded)
            decoded_data = base64.urlsafe_b64decode(start_param).decode("utf-8")
        except Exception:
            return web.json_response({"error": "Invalid start parameter"}, status=400)
        
        # Process the decoded data as needed
        return web.json_response({"message": f"Processing request: {decoded_data}"})
    
    # Fallback response when no start parameter is provided
    return web.json_response("Codeflix FileStore")

# Create the aiohttp application and add routes
app = web.Application()
app.add_routes(routes)

if __name__ == "__main__":
    # Use the PORT environment variable or default to 8080
    web.run_app(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
