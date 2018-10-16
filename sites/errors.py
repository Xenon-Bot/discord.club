from aiohttp import web
import aiohttp_jinja2


@web.middleware
async def error_middleware(request, handler):
    try:
        response = await handler(request)
        if response.status < 400:
            return response

        status = response.status
        message = response.message
    except web.HTTPException as ex:
        status = ex.status
        if status < 400:
            raise

        message = ex.reason

    return aiohttp_jinja2.render_template(template_name="/error.html", context={"message": message, "status": status}, status=status, request=request)


async def setup(app):
    app.middlewares.append(error_middleware)