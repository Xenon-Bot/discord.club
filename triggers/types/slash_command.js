import BaseTrigger from './base'
import {jsonResponse} from "../util";


export default class SlashCommandTrigger extends BaseTrigger {
    constructor(...props) {
        super(...props);
    }

    async execute() {
        return jsonResponse({})
    }
}