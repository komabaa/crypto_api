from aiohttp import web

@web.middleware
async def handle_error(request, handler):
    try:
        response = await handler(request)
        return response
    except Exception as e:
        return web.json_response({'error': str(e)}, status=500) 