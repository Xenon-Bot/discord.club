from sanic import response
import hashlib


__all__ = (
    "requires_body",
    "upload_file",
    "single_value_form"
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


async def upload_file(bucket, file_name, blob: bytes, content_type="application/octet-stream"):
    """
    Uploads a file to the GridFS bucket
    Respecting the md5 hash to avoid duplicates
    """
    md5 = hashlib.md5(blob).hexdigest()
    existing = await bucket.collection.files.find_one({"md5": md5})
    if existing is not None:
        return existing["_id"]

    file_id = await bucket.upload_from_stream(
        file_name,
        blob,
        metadata={"content_type": content_type}
    )
    return file_id


def single_value_form(form_data):
    return {
        k: v[0]
        for k, v in form_data.items()
    }
