import Sval from 'sval'
import {jsonResponse, fillMessageVars} from "../util";

export default class BaseTrigger {
    constructor(request) {
        this.request = request
        this.sval = new Sval()
        this.sval.import({jsonResponse, fillMessageVars, Response, fetch})
    }

    async initTrigger(triggerType, triggerSecret) {
        /* const resp = await fetch(`https://api.discord.club/triggers/${triggerSecret}`)
        if (!resp.ok) {
            return false
        }

        this.triggerData = await resp.json() */
        this.triggerData = {
            type: 'scheduled',
            message: {json: {content: 'yeet'}},
            webhook: {id: '', token: ''},
            script: 'trigger.executeWebhook().then(res => resolve(jsonResponse(res)))'
        }
        if (triggerType !== this.triggerData.type) {
            return false
        }

        this.payload = await this.request.json()
        return true
    }

    async runScript(code) {
        this.sval.run(`exports.result = new Promise(function(resolve) {${code}})`)
        return this.sval.exports.result
    }

    async executeWebhook() {
        return {webhook: 'cool'}
    }
}