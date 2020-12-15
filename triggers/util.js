function jsonResponse(obj, status = 200) {
    return new Response(JSON.stringify(obj), {
        status: status,
        headers: {'Content-Type': 'application/json'}
    })
}

function fillMessageVars(json, vars) {

}

export {
    jsonResponse,
    fillMessageVars
}