if event.message.text == "要嗎?":
        buttons_template = TemplateSendMessage(
            alt_text='要嗎? template',
            template=ConfirmTemplate(
                title='請決定要或不要',
                text='yes/no',
                thumbnail_image_url='https://i.imgur.com/3fdSP2p.png',
                actions=[
                    MessageTemplateAction(
                        label='要',
                        text='要'
                    ),
                    MessageTemplateAction(
                        label='不要',
                        text='不要'
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
        return 0
