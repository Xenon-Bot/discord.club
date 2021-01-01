addEventListener('fetch', event => {
    event.respondWith(handleRequest(event.request))
})

/**
 * Proxy request
 * @param {Request} request
 */
async function handleRequest(request) {
    const referer = request.headers.get('referer')
    if (!referer || !new URL(referer).hostname.endsWith('discord.club')) {
        return new Response('Not allowed', {status: 403})
    }

    const {pathname} = new URL(request.url)
    const encodedUrl = pathname.replace('/', '')
    try {
        const url = atob(encodedUrl)
        const imgResponse = await fetch(url, {headers: request.headers})
        const contentType = imgResponse.headers.get('content-type')
        if (contentType && !contentType.match(/image/)) {
            return new Response(`Not an image: ${contentType}; ${await imgResponse.text()}`, {status: 400})
        }
        return imgResponse
    } catch (e) {
        return new Response(`Unable to fetch: ${e}`, {status: 400})
    }
}
