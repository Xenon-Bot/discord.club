import SlashCommandTrigger from "./types/slash_command";
import {jsonResponse} from "./util";
import SimpleTrigger from "./types/simple";

async function handleRequest(request) {
    const {pathname} = new URL(request.url)
    const pathParts = pathname
        .replace(/(^\/)|(\/$)/, '')
        .split('/')
    if (pathParts.length < 2) {
        return jsonResponse({error: 'Missing required path parameters'}, 400)
    }

    const triggerType = pathParts[0]
    const triggerSecret = pathParts[1]

    let executor
    switch (triggerType) {
        case 'interaction':
            executor = new SlashCommandTrigger(request)
            break
        case 'scheduled':
            executor = new SimpleTrigger(request)
            break
        default:
            return jsonResponse({error: 'Unknown trigger type'}, 400)
    }

    if (!await executor.initTrigger(triggerType, triggerSecret)) {
        return jsonResponse({error: 'Invalid trigger secret'}, 400)
    }
    try {
        return await executor.execute()
    } catch (e) {
        return jsonResponse({error: `Internal Server Error: ${e}`}, 500)
    }
}

addEventListener('fetch', event => {
    event.respondWith(handleRequest(event.request))
})
