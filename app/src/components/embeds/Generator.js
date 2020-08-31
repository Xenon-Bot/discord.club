import React, {useContext} from 'react';
import Card from "react-bootstrap/Card";
import Form from "react-bootstrap/Form";
import InputGroup from "react-bootstrap/InputGroup";
import Button from "react-bootstrap/Button";
import Col from "react-bootstrap/Col";
import Accordion from "react-bootstrap/Accordion";
import {FaPlus, FaTrash, FaAngleUp, FaAngleDown, FaMinusCircle} from 'react-icons/fa';
import {NotificationManager} from 'react-notifications';
import Preview from "./Preview";
import {AccordionContext, useAccordionToggle} from "react-bootstrap";


function tryInt(value) {
    let number = parseInt(value, 10);
    if (isNaN(number)) {
        return value;
    } else {
        return number;
    }
}


function EmbedToggle({children, eventKey, callback}) {
    const currentEventKey = useContext(AccordionContext);

    const decoratedOnClick = useAccordionToggle(
        eventKey,
        () => callback && callback(eventKey),
    );

    const isCurrentEventKey = currentEventKey === eventKey;

    return (
        <Button
            type="button" variant="outline-dark" size="md"
            onClick={decoratedOnClick}
            className="float-right"
        >
            {isCurrentEventKey ? <FaAngleUp/> : <FaAngleDown/>}
        </Button>
    );
}


class Generator extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            webhookUrl: null,
            files: [],
            data: {}
        };
    }

    setKey(key, value, bubbleDown = false) {
        const path = key.split(".");
        const data = this.state.data;
        let level = data;

        if (value === "" || value === null || value === undefined) {
            if (bubbleDown) {
                for (let i = path.length - 1; i >= 0; i--) {
                    level = data;
                    let cancel = false;
                    for (let x = 0; x < i; x++) {
                        let key = tryInt(path[x]);

                        if (level.hasOwnProperty(key)) {
                            level = level[key];
                        } else {
                            cancel = true;
                            break;
                        }
                    }

                    if (cancel) {
                        continue;
                    }

                    let key = tryInt(path[i]);

                    if (!level[key]) {
                        return;
                    } else if (Array.isArray(level[key])) {
                        if (level[key].length === 0) {
                            if (Array.isArray(level)) {
                                level.splice(key, 1);
                            } else {
                                delete level[key];
                            }
                        }
                    } else if (Object.keys(level[key]).length === 0 || i === (path.length - 1)) {
                        if (Array.isArray(level)) {
                            level.splice(key, 1);
                        } else {
                            delete level[key];
                        }
                    }
                }
            } else {
                for (let i = 0; i < path.length; i++) {
                    const part = path[i];
                    let key = tryInt(part);

                    if (level.hasOwnProperty(key)) {
                        if (i === (path.length - 1)) {
                            if (Array.isArray(level)) {
                                level.splice(key, 1);
                            } else {
                                delete level[key];
                            }
                        } else {
                            level = level[key];
                        }
                    } else {
                        return;
                    }
                }
            }
        } else {
            for (let i = 0; i < path.length; i++) {
                const part = path[i];

                let key = tryInt(part);

                if (i === (path.length - 1)) {
                    level[key] = value;
                } else if (!level.hasOwnProperty(key)) {
                    const nextIndex = parseInt(path[i + 1], 10);
                    if (isNaN(nextIndex)) {
                        level[key] = {}
                    } else {
                        level[key] = []
                    }
                }

                level = level[key];
            }
        }
    }

    getKey(key, def) {
        const path = key.split(".");
        let level = this.state.data;
        for (let part of path) {
            if (!level.hasOwnProperty(part)) {
                return def ? def : "";
            }

            level = level[part];
        }

        return level;
    }

    handleFormChange(event) {
        const target = event.target;
        const value = target.type === 'checkbox' ? target.checked : target.value;

        this.setKey(target.name, value);
        this.setState({data: this.state.data});
    }

    handleJSONChange(event) {
        const target = event.target;
        try {
            this.setState({data: JSON.parse(target.value)});
        } catch (e) {
            NotificationManager.error("The JSON code isn't valid")
        }
    }

    addFile() {
        const files = this.state.files;
        if (files.length < 10) {
            files.push({});
            this.setState({files: files})
        } else {
            NotificationManager.error("You can't add more than 10 files")
        }
    }

    deleteFile(i) {
        const files = this.state.files;
        files.splice(i, 1);
        this.setState({files: files});
    }

    deleteFiles() {
        this.setState({files: []});
    }

    addEmbed() {
        const data = this.state.data;
        if (!data.hasOwnProperty("embeds")) {
            data.embeds = [];
        }

        if (data.embeds.length < 10) {
            data.embeds.push({});
            this.setState({data: data});
        } else {
            NotificationManager.error("You can't add more than 10 embeds")
        }
    }

    deleteEmbed(i) {
        const data = this.state.data;
        if (data.hasOwnProperty("embeds")) {
            data.embeds.splice(i, 1);
            this.setState({data: data});
        }
    }

    deleteEmbeds() {
        const data = this.state.data;
        if (data.hasOwnProperty("embeds")) {
            delete data["embeds"];
            this.setState({data: data});
        }
    }

    addField(e) {
        const data = this.state.data;
        const embed = data.embeds[e];
        if (!embed.hasOwnProperty("fields")) {
            embed.fields = [];
        }

        if (embed.fields.length < 10) {
            embed.fields.push({});
            this.setState({data: data});
        } else {
            NotificationManager.error("You can't add more than 10 fields per embed")
        }
    }

    deleteField(e, i) {
        const data = this.state.data;
        const embed = data.embeds[e];
        if (embed.hasOwnProperty("fields")) {
            embed.fields.splice(i, 1);
            this.setState({data: data});
        }
    }

    deleteFields(e) {
        const data = this.state.data;
        const embed = data.embeds[e];
        if (embed.hasOwnProperty("fields")) {
            delete embed["fields"];
            this.setState({data: data});
        }
    }

    render() {
        const embeds = [];
        if (this.state.data.hasOwnProperty("embeds")) {
            for (let i = 0; i < this.state.data.embeds.length; i++) {
                const embed = this.state.data.embeds[i];
                const fields = [];
                if (embed.hasOwnProperty("fields")) {
                    for (let x = 0; x < embed.fields.length; x++) {
                        fields.push(
                            <Form.Row key={x}>
                                <Form.Group as={Col}>
                                    <Form.Control type="text" placeholder="Name" maxLength="256"
                                                  value={this.getKey(`embeds.${i}.fields.${x}.name`)}
                                                  name={`embeds.${i}.fields.${x}.name`}
                                                  onChange={e => this.handleFormChange(e)}/>
                                </Form.Group>
                                <Form.Group as={Col}>
                                    <Form.Control type="text" placeholder="Value" maxLength="1024"
                                                  value={this.getKey(`embeds.${i}.fields.${x}.value`)}
                                                  name={`embeds.${i}.fields.${x}.value`}
                                                  onChange={e => this.handleFormChange(e)}/>
                                </Form.Group>
                                <Form.Group as={Col} xs="auto">
                                    <Form.Check type="checkbox" label="inline"/>
                                </Form.Group>
                                <Form.Group as={Col} xs="auto">
                                    <Button
                                        type="button" variant="outline-danger" size="sm"
                                        onClick={() => this.deleteField(i, x)}
                                    >
                                        <FaMinusCircle/>
                                    </Button>
                                </Form.Group>
                            </Form.Row>
                        )
                    }
                }

                embeds.push(
                    <Card className="mb-4" key={i}>
                        <Card.Body>
                            <Form.Row>
                                <Form.Group as={Col} xs={10}>
                                    <Form.Control type="text" placeholder="Title" maxLength="256"
                                                  value={this.getKey(`embeds.${i}.title`)}
                                                  name={`embeds.${i}.title`} onChange={e => this.handleFormChange(e)}/>
                                </Form.Group>
                                <Form.Group as={Col} xs={2}>
                                    <Form.Control type="color" maxLength="256"
                                                  value={this.getKey(`embeds.${i}.color`, "#1f2225")}
                                                  name={`embeds.${i}.color`} onChange={e => this.handleFormChange(e)}/>
                                </Form.Group>
                            </Form.Row>
                            <Accordion.Collapse eventKey={i.toString()}>
                                <div>
                                    <Form.Group>
                                        <Form.Control as="textarea" placeholder="Content" rows="5"
                                                      onChange={e => this.handleFormChange(e)}
                                                      name={`embeds.${i}.description`}
                                                      value={this.getKey(`embeds.${i}.description`)}/>
                                    </Form.Group>
                                    <Form.Group className="pb-3">
                                        <Form.Control type="url" placeholder="Url"
                                                      name={`embeds.${i}.url`}
                                                      onChange={e => this.handleFormChange(e)}
                                                      value={this.getKey(`embeds.${i}.url`)}/>
                                    </Form.Group>

                                    <Form.Label>Author</Form.Label>
                                    <Form.Row>
                                        <Form.Group as={Col}>
                                            <Form.Control type="text" placeholder="Name" maxLength="256"
                                                          name={`embeds.${i}.author.name`}
                                                          onChange={e => this.handleFormChange(e)}
                                                          value={this.getKey(`embeds.${i}.author.name`)}/>
                                        </Form.Group>
                                        <Form.Group as={Col}>
                                            <Form.Control type="url" placeholder="Url"
                                                          name={`embeds.${i}.author.url`}
                                                          onChange={e => this.handleFormChange(e)}
                                                          value={this.getKey(`embeds.${i}.author.url`)}/>
                                        </Form.Group>
                                    </Form.Row>
                                    <Form.Group className="pb-3">
                                        <Form.Control type="url" placeholder="Icon Url"
                                                      name={`embeds.${i}.author.icon_url`}
                                                      onChange={e => this.handleFormChange(e)}
                                                      value={this.getKey(`embeds.${i}.author.icon_url`)}/>
                                    </Form.Group>

                                    <Form.Label>Images</Form.Label>
                                    <Form.Group>
                                        <Form.Control type="url" placeholder="Thumbnail Url"
                                                      name={`embeds.${i}.thumbnail.url`}
                                                      onChange={e => this.handleFormChange(e)}
                                                      value={this.getKey(`embeds.${i}.thumbnail.url`)}/>
                                    </Form.Group>
                                    <Form.Group className="pb-3">
                                        <Form.Control type="url" placeholder="Image Url"
                                                      name={`embeds.${i}.image.url`}
                                                      onChange={e => this.handleFormChange(e)}
                                                      value={this.getKey(`embeds.${i}.image.url`)}/>
                                    </Form.Group>

                                    <Form.Label>Footer</Form.Label>
                                    <Form.Row>
                                        <Form.Group as={Col}>
                                            <Form.Control type="text" placeholder="Text" maxLength="256"
                                                          name={`embeds.${i}.footer.text`}
                                                          onChange={e => this.handleFormChange(e)}
                                                          value={this.getKey(`embeds.${i}.footer.text`)}/>
                                        </Form.Group>
                                        <Form.Group as={Col}>
                                            <Form.Control type="datetime-local" placeholder="Url"
                                                          name={`embeds.${i}.timestamp`} step="0.001"
                                                          onChange={e => this.handleFormChange(e)}
                                                          value={this.getKey(`embeds.${i}.timestamp`)}/>
                                        </Form.Group>
                                    </Form.Row>
                                    <Form.Group className="pb-3">
                                        <Form.Control type="url" placeholder="Icon Url"
                                                      name={`embeds.${i}.footer.icon_url`}
                                                      onChange={e => this.handleFormChange(e)}
                                                      value={this.getKey(`embeds.${i}.footer.icon_url`)}/>
                                    </Form.Group>

                                    <Form.Label>Fields</Form.Label>
                                    <div>
                                        {fields}
                                    </div>
                                    <Button
                                        type="button" variant="outline-success" size="sm"
                                        onClick={() => this.addField(i)}
                                        className="mr-1"
                                    >
                                        <FaPlus/>
                                    </Button>
                                    <Button
                                        type="button" variant="outline-danger" size="sm"
                                        onClick={() => this.deleteFields(i)}
                                    >
                                        <FaTrash/>
                                    </Button>
                                </div>
                            </Accordion.Collapse>
                            <EmbedToggle eventKey={i.toString()} as={Button}/>
                            <Button
                                type="button" variant="outline-danger" size="md"
                                onClick={() => this.deleteEmbed(i)}
                                className="float-right mr-1"
                            >
                                <FaMinusCircle/>
                            </Button>
                        </Card.Body>
                    </Card>
                )
            }
        }

        const files = [];
        for (let i = 0; i < this.state.files.length; i++) {
            files.push(<h5 key={i}>File {i + 1}</h5>)
        }

        return (
            <div>
                <Form>
                    <h4>Message</h4>
                    <Card className="mt-3 mb-5">
                        <Card.Body>
                            <Form.Label>Webhook Settings</Form.Label>
                            <Form.Group>
                                <InputGroup>
                                    <Form.Control type="url"
                                                  defaultValue={this.state.webhookUrl}
                                                  onChange={e => this.setState({webhookUrl: e.target.value})}
                                                  placeholder="https://discordapp.com/api/webhooks/423157583646294017/nsFEJfuNKVBRcKcgj0JX3TygdvhX-ItEJhrWVWadw7shUXXuIRwsJHUS_XbDDSA_ILKN"
                                                  required/>
                                    <InputGroup.Append>
                                        <Button type="button">Create One</Button>
                                    </InputGroup.Append>
                                </InputGroup>
                            </Form.Group>
                            <Form.Row className="pb-3">
                                <Form.Group as={Col}>
                                    <Form.Control type="text" placeholder="Name" name="username"
                                                  onChange={e => this.handleFormChange(e)}
                                                  value={this.getKey("username")}/>
                                </Form.Group>
                                <Form.Group as={Col}>
                                    <Form.Control type="url" placeholder="Avatar-Url" name="avatar_url"
                                                  onChange={e => this.handleFormChange(e)}
                                                  value={this.getKey("avatar_url")}/>
                                </Form.Group>
                            </Form.Row>

                            <Form.Label>Message Content</Form.Label>
                            <Form.Group className="pb-3">
                                <Form.Control as="textarea" placeholder="Content" rows="5" maxLength="2000"
                                              name="content" onChange={e => this.handleFormChange(e)}
                                              value={this.getKey("content")}/>
                            </Form.Group>

                            <Form.Label>Files</Form.Label>
                            <div>
                                {files}
                            </div>
                            <Button className="mr-1" type="button" variant="outline-success" size="sm"
                                    onClick={() => this.addFile()}><FaPlus/></Button>
                            <Button type="button" variant="outline-danger" size="sm"
                                    onClick={() => this.deleteFiles()}><FaTrash/></Button>
                        </Card.Body>
                    </Card>

                    <h4>Embeds</h4>
                    <Accordion>
                        {embeds}
                    </Accordion>
                    <Button className="mr-1" type="button" variant="outline-success" size="md"
                            onClick={() => this.addEmbed()}><FaPlus/></Button>
                    <Button type="button" variant="outline-danger" size="md"
                            onClick={() => this.deleteEmbeds()}><FaTrash/></Button>
                </Form>
                <h4 className="mt-5">JSON Code</h4>
                <Card className="mb-5">
                    <Card.Body>
                        <Form.Control as="textarea" placeholder="Content" rows="10"
                                      onChange={e => this.handleJSONChange(e)}
                                      value={JSON.stringify(this.state.data, null, 2)}/>
                    </Card.Body>
                </Card>

                <Card>
                    <Card.Body>
                        <Preview/>
                    </Card.Body>
                </Card>
            </div>
        );
    }
}

export default Generator;
