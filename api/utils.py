from sanic import response


__all__ = (
    "requires_body",
)


def requires_body(*fields, **typed_fields):
    def predicate(handler):
        async def wrapper(request, *args, **kwargs):
            payload = {}
            data = request.json
            if data is None:
                return response.json({"error": "JSON body required"}, status=400)

            if len(fields) == 0 and len(typed_fields) == 0:
                return await handler(request, data, *args, **kwargs)

            for field in fields:
                value = data.get(field)
                if value is None:
                    return response.json({"error": f"Field '{field}' is required"}, status=400)

                payload[field] = value

            for field, type in typed_fields.items():
                value = data.get(field)
                if value is None:
                    return response.json({"error": f"Field '{field}' is required"}, status=400)

                try:
                    value = type(value)
                except:
                    return response.json({"error": f"Invalid value for field '{field}'"}, status=400)

                payload[field] = value

            return await handler(request, payload, *args, **kwargs)

        return wrapper

    return predicate
