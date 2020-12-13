<template>
    <div>
        <a href="/discord" class="btn btn-outline-secondary float-right" target="_blank">Support Discord</a>
        <!--<h3 class="mb-3">Quick Start</h3>
        <h4>Sending a message</h4>
        <h4>Creating a trigger</h4>-->
        <h3 class="mb-3 -mt-5">FAQ</h3>
        <div id="faq-accordion" class="mb-3">
            <div v-for="(question, i) in faq.questions" :key="`question${i}`" class="card bg-darker mb-2">
                <div class="card-header c-pointer" id="headingOne" data-toggle="collapse" :data-target="`#question${i}`"
                     aria-expanded="true" :aria-controls="`question${i}`">
                    <h5 class="mb-0">{{question.title}}</h5>
                </div>
                <div :id="`question${i}`" class="collapse" aria-labelledby="headingOne" data-parent="#faq-accordion">
                    <div class="card-body" v-html="question.text"></div>
                </div>
            </div>
        </div>
        <span class="float-right">
            <img src="@/assets/locales/en.svg" alt="English" class="locale" @click="setLocale('en')">
            <img src="@/assets/locales/de.svg" alt="German" class="locale" @click="setLocale('de')">
            <img src="@/assets/locales/ru.svg" alt="Russian" class="locale" @click="setLocale('ru')">
            <img src="@/assets/locales/es.svg" alt="Spanish" class="locale" @click="setLocale('es')">
            <img src="@/assets/locales/fr.svg" alt="French" class="locale" @click="setLocale('fr')">
            <img src="@/assets/locales/ar.svg" alt="Arabic" class="locale" @click="setLocale('ar')">
            <h5 class="text-right mt-2">Translated by {{faq.author}}</h5>
        </span>
    </div>
</template>
<script>
    const faq = {
        en: {
            author: 'Merlin',
            questions: [
                {
                    title: 'How to create a webhook?',
                    text: `You need a webhook URL to send a message. If you are using the desktop or web version of
                                discord you can just go to the channel settings and create a webhook there.
                                <img src="/img/faq/create_webhook_desktop.png" alt="Create a webhook desktop" class="faq-image">
                                If you are using the mobile app, you can
                                <a href="/invite" target="_blank">invite the bot</a> and use the <code>&gt;webhook</code>
                                command to get a valid webhook url for your channel.
                                <img src="/img/faq/create_webhook_mobile.png" alt="Create a webhook mobile" class="faq-image">`
                },
                {
                    title: 'How to edit an existing message?',
                    text: `Editing an existing message requires the message URL / ID and the webhook URL that was
                                used to create the message. If the message was not sent by a webhook or the correct
                                webhook got deleted there is no way to edit the message. <br/>
                                You can obtain the webhook URL in the channel settings and the message URL by
                                right-clicking the message (opening the context menu) and clicking
                                <code>Copy Message Link</code>.
                                <img src="/img/faq/get_message_url.png" alt="Get message URL" class="faq-image">
                                You can also <a href="/invite" target="_blank">invite the bot</a> and use the
                                <code>&gt;edit &lt;message-url-or-id&gt;</code> command to quickly obtain a share-link
                                with the webhook and message URL pre-filled.
                                <img src="/img/faq/edit_message_cmd.png" alt="Edit message cmd" class="faq-image">`
                },
                {
                    title: 'How do I mention a user, channel or role?',
                    text: `To mention a user, channel or role you need to use the
                                <a href="https://discord.com/developers/docs/reference#message-formatting">API format</a>.
                                Click <a href="https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID">here</a>
                                to see how to obtain an entity ID. <br>
                                You can also <a href="/invite" target="_blank">invite the bot</a> and use the
                                <code>&gt;format &lt;text&gt;</code> command to get the API format for a given text.
                                <img src="/img/faq/api_format_cmd.png" alt="API format cmd" class="faq-image">`
                },
                {
                    title: 'How do I use a custom emoji?',
                    text: `To use a custom emoji you need to use the
                                <a href="https://discord.com/developers/docs/reference#message-formatting">API format</a>.
                                You can obtain the correct format by putting a backslash (<code>\\</code>) in front of
                                the emoji inside discord. <br>
                                You can also <a href="/invite" target="_blank">invite the bot</a> and use the
                                <code>&gt;format &lt;text&gt;</code> command to get the API format for a given text.
                                <img src="/img/faq/api_format_cmd.png" alt="API format cmd" class="faq-image">
                                Keep in mind that the <code>@everyone</code> role needs to have the "Use External Emojis"
                                permission if you want to use an emoji from a different server in a webhook message.`
                },
                {
                    title: 'Are there other ways to format my message?',
                    text: `Discord supports a limited subset of markdown in embeds and webhook messages.
                                Markdown is only supported in the message content, embed descriptions and embed field values.
                                <div class="faq-table mt-3 rounded">
                                <table class="table table-dark">
                                    <thead>
                                        <tr>
                                            <th></th>
                                            <th>Format</th>
                                            <th>Result</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <td>Bold</td>
                                        <td><code>**text**</code></td>
                                        <td><b>text</b></td>
                                    </tbody>
                                    <tbody>
                                        <td>Italic</td>
                                        <td><code>*text*</code></td>
                                        <td><i>text</i></td>
                                    </tbody>
                                    <tbody>
                                        <td>Underline</td>
                                        <td><code>__text__</code></td>
                                        <td><u>text</u></td>
                                    </tbody>
                                    <tbody>
                                        <td>Strikethrough</td>
                                        <td><code>~~text~~</code></td>
                                        <td><strike>text</strike></td>
                                    </tbody>
                                    <tbody>
                                        <td>Hyperlink</td>
                                        <td><code>[Xenon Bot](https://xenon.bot)</code></td>
                                        <td><a href="https://xenon.bot" target="_blank">Xenon Bot</a></td>
                                    </tbody>
                                    <tbody>
                                        <td>Avoid Embed</td>
                                        <td><code>&lt;https://xenon.bot&gt;</code></td>
                                        <td>The link will not be embedded by discord</td>
                                    </tbody>
                                </table>
                                </div>
                                You can also combine multiple styles: <code>**__text__**</code> will result in <b><u>text</u></b>.`
                },
                {
                    title: 'How do I save a message?',
                    text: `You need to login with discord to be able to save messages on the server. <br>
                                In the "Quick Message" section click on "Save Message" below the JSON-Code and click on
                                the discord icon if you aren't already logged in. <br>
                                After you logged in you can click "Save Message" again, give the message a name and
                                click "Save". You will be redirected to the edit page of the newly saved message.
                                <img src="/img/faq/save_message.png" alt="Save message" class="faq-image">`
                },
                {
                    title: 'How do I edit and use a saved message?',
                    text: `You can find your saved messages by clicking on "Messages" in the menu on the left side.
                                Select the message you want to edit or use and click on "View". Your saved message should
                                appear and you can edit it. You can save the edited message by clicking on "Save Message".
                                <img src="/img/faq/edit_saved.png" alt="Edit saved message" class="faq-image"/>`
                }
            ]
        },
        de: {
            author: 'Merlin',
            questions: [
                {
                    title: 'Wie erstelle ich einen Webhook?',
                    text: `Du benötigst einen Webhook um eine Nachricht zu senden. Wenn du die Dasktop-App von discord bentuzt,
                                kannst du einen Webhook in den Kanaleinstellungen erstellen.
                                <img src="/img/faq/create_webhook_desktop.png" alt="Create a webhook desktop" class="faq-image">
                                Wenn du die Mobile-App benutzt, kannst du den
                                <a href="/invite" target="_blank">bot einladen</a> und den <code>&gt;webhook</code>
                                Befehl benutzen um eine Webhook-Url für den Kanal zu bekommen.
                                <img src="/img/faq/create_webhook_mobile.png" alt="Create a webhook mobile" class="faq-image">`
                },
                {
                    title: 'Wie editiere ich eine existierende Nachricht?',
                    text: `Um eine existierende Nachricht zu editieren, benötigst du die Nachrichten-URL und die
                                Webhook-URL die verwendet wurde, um die Nachricht zu erstellen. Wenn die Nachricht nicht
                                von einem Webhook gesendet, oder der Webhook gelöscht wurde gibt es keine Möglichkeit
                                die Nachricht zu editieren. <br/>
                                Die Webhook-URL kannst du in den Kanaleinstellungen finden. Um die Nachrichten-URL
                                abzurufen, musst due nach dem Rechtsklick auf eine Nachricht auf
                                 <code>Nachrichtenlink kopieren</code> klicken.
                                <img src="/img/faq/get_message_url.png" alt="Get message URL" class="faq-image">
                                Du kannst auch <a href="/invite" target="_blank">den bot einladen</a> und den
                                <code>&gt;edit &lt;message-url-or-id&gt;</code> Befehl benutzen um schnell
                                einen Share-Link mit der Webhook-URL und Message-URL zu bekommen.
                                <img src="/img/faq/edit_message_cmd.png" alt="Edit message cmd" class="faq-image">`
                },
            ]
        },
        ru: {
            author: 'JustPh03n1x',
            questions: [
                {
                    title: 'Как создать вебхук?',
                    text: `Для отправки вебхука вам нужен URL-адрес. Если вы используете программу или веб-версиб Дискорда, 
                           вы можете просто зайти в настройки канала и создать там вебхук.
                                <img src="/img/faq/create_webhook_desktop.png" alt="Create a webhook desktop" class="faq-image">
                                Если вы используете мобильное приложение, вы можете
                                <a href="/invite" target="_blank">пригласить бота</a> и использовать <code>&gt;webhook</code>
                                чтобы получить действительный URL-адрес вебхука для вашего канала.
                                <img src="/img/faq/create_webhook_mobile.png" alt="Create a webhook mobile" class="faq-image">`
                },
                {
                    title: 'Как отредактировать существующее сообщение?',
                    text: `Для редактирования существующего сообщения требуется URL/ID сообщения и URL-адрес вебхука, который был
                                использован для создания сообщения. Если сообщение не было отправлено с помощью вебхука или он
                                был удален, сообщение невозможно отредактировать. <br/>
                                Вы можете получить URL-адрес вебхука в настройках канала или URL-адрес сообщения,
                                щелкнув сообщение правой кнопкой мыши (открыв контекстное меню) и нажав
                                <code>Copy Message Link</code>.
                                <img src="/img/faq/get_message_url.png" alt="Get message URL" class="faq-image">
                                Вы также можете <a href="/invite" target="_blank">пригласить бота</a> и использовать
                                <code>&gt;edit &lt;message-url-or-id&gt;</code> чтобы быстро получить ссылку для совместного доступа
                                с предварительно заполненным вебхуком и URL-адресом сообщения.
                                <img src="/img/faq/edit_message_cmd.png" alt="Edit message cmd" class="faq-image">`
                },
                {
                    title: 'Как мне упомянуть пользователя, канал или роль?',
                    text: `Чтобы упомянуть пользователя, канал или роль, вам необходимо использовать
                                <a href="https://discord.com/developers/docs/reference#message-formatting">API format</a>.
                                Нажмите <a href="https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID">здесь</a>
                                чтобы узнать, как получить ID. <br>
                                Вы также можете <a href="/invite" target="_blank">пригласить бота</a> и использовать
                                <code>&gt;format &lt;text&gt;</code> чтобы получить формат API для заданного текста.
                                <img src="/img/faq/api_format_cmd.png" alt="API format cmd" class="faq-image">`
                },
                {
                    title: 'Как использовать собственный смайлик?',
                    text: `Чтобы использовать собственный смайлик, вам нужно использовать
                                <a href="https://discord.com/developers/docs/reference#message-formatting">API format</a>.
                                Вы можете получить правильный формат, поставив обратную косую черту (<code>\\</code>) перед
                                смайликом в дискорде. <br>
                                Вы также можете <a href="/invite" target="_blank">пригласить бота</a> и использовать
                                <code>&gt;format &lt;text&gt;</code> чтобы получить формат API для данного текста.
                                <img src="/img/faq/api_format_cmd.png" alt="API format cmd" class="faq-image">
                                Имейте в виду, что роль <code>@everyone</code> должна иметь параметр "Использовать внешние эмодзи".
                                разрешение, если вы хотите использовать эмодзи с другого сервера в сообщении вебхука.`
                },
                {
                    title: 'Есть ли другие способы отформатировать мое сообщение?',
                    text: `Discord поддерживает ограниченный во встраиваемых сообщениях и сообщениях вебхука.
                                 Markdown поддерживается только в содержимом сообщения, описаниях вставок и значениях полей вставок.
                                <div class="faq-table mt-3 rounded">
                                <table class="table table-dark">
                                    <thead>
                                        <tr>
                                            <th></th>
                                            <th>Формат</th>
                                            <th>Результат</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <td>Bold</td>
                                        <td><code>**текст**</code></td>
                                        <td><b>текст</b></td>
                                    </tbody>
                                    <tbody>
                                        <td>Italic</td>
                                        <td><code>*текст*</code></td>
                                        <td><i>текст</i></td>
                                    </tbody>
                                    <tbody>
                                        <td>Underline</td>
                                        <td><code>__текст__</code></td>
                                        <td><u>текст</u></td>
                                    </tbody>
                                    <tbody>
                                        <td>Strikethrough</td>
                                        <td><code>~~текст~~</code></td>
                                        <td><strike>текст</strike></td>
                                    </tbody>
                                    <tbody>
                                        <td>Hyperlink</td>
                                        <td><code>[Xenon Bot](https://xenon.bot)</code></td>
                                        <td><a href="https://xenon.bot" target="_blank">Xenon Bot</a></td>
                                    </tbody>
                                    <tbody>
                                        <td>Avoid Embed</td>
                                        <td><code>&lt;https://xenon.bot&gt;</code></td>
                                        <td>Ссылка не будет встроена в Discord</td>
                                    </tbody>
                                </table>
                                </div>
                                Вы также можете комбинировать несколько стилей: <code>**__текст__**</code> приведет к <b><u>текст</u></b>.`
                },
                {
                    title: 'Как сохранить сообщение?',
                    text: `Вам необходимо войти в систему с помощью Discord, чтобы иметь возможность сохранять сообщения на сервере. <br>
                                В разделе "Quick Message" нажмите "Save Message" под JSON-кодом и нажмите
                                значок Discord, если вы еще не вошли в систему. <br>
                                После входа в систему вы можете снова нажать "Save Message", дать сообщению имя и
                                нажмите "Save". Вы будете перенаправлены на страницу редактирования только что сохраненного сообщения.
                                <img src="/img/faq/save_message.png" alt="Save message" class="faq-image">`
                },
                {
                    title: 'Как редактировать и использовать сохраненное сообщение?',
                    text: `Вы можете найти свои сохраненные сообщения, щелкнув "Messages" в меню слева.
                                Выберите сообщение, которое вы хотите отредактировать или использовать, и нажмите "View". Ваше сохраненное сообщение должно
                                появляются, и вы можете редактировать его. Вы можете сохранить отредактированное сообщение, нажав "Save Message".
                                <img src="/img/faq/edit_saved.png" alt="Edit saved message" class="faq-image"/>`
                }
            ]
        },
        ar: {
            author: '',
            questions: []
        },
        es: {
            author: '',
            questions: []
        },
        fr: {
            author: '',
            questions: []
        }
    }

    export default {
        name: 'Help',
        data() {
            return {
                locale: localStorage.getItem('locale') ?? 'en'
            }
        },
        computed: {
            faq() {
                return faq[this.locale]
            }
        },
        methods: {
            setLocale(newLocale) {
                localStorage.setItem('locale', newLocale)
                this.locale = newLocale
            }
        }
    }
</script>
<style lang="scss">
    .faq-image {
        display: block;
        margin: 15px 0;
        max-width: 500px;
        width: 100%;
        border-radius: 5px;
    }

    .faq-table {
        width: 100%;
        overflow-x: auto;
    }

    strike {
        text-decoration: line-through;
    }

    .locale {
        height: 3em;
        margin-left: 1em;
        cursor: pointer;
    }
</style>
