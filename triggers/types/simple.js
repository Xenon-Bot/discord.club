import BaseTrigger from './base'


export default class SimpleTrigger extends BaseTrigger {
    constructor(...props) {
        super(...props);
    }

    async execute() {
        return this.runScript(this.payload.script)
    }
}