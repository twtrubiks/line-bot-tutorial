
 if event.message.text == "雷弟安安" or event.message.text == "功能表" or event.message.text == "啟動功能表":
        buttons_template = TemplateSendMessage(
            alt_text='功能表 template',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        title='看正妹就像喝水一樣',
                        text='每天都要來一點',
                        thumbnail_image_url='https://i.imgur.com/DDI9m3i.png',
                        actions=[
                            MessageTemplateAction(
                                label='隨便來一張正妹',
                                text='抽卡'
                            ),
                            MessageTemplateAction(
                                label='表特版熱門連結',
                                text='PTT 表特版'
                            )
                        ]
                    ),
                    # http://imgur.com/JVXiiin
                    CarouselColumn(
                        title='肥宅不出門',
                        text='能知天下事',
                        # 子堯照片
                        thumbnail_image_url='https://i.imgur.com/3fdSP2p.png',
                        actions=[
                            MessageTemplateAction(
                            label='youtube熱門',
                            text='yt'
                        ),
                            MessageTemplateAction(
                                label='近期熱門廢文',
                                text='熱門廢文'
                            )
                        ]
                    ),
                    CarouselColumn(
                        title='低卡低卡',
                        text='低卡真的低能嗎?',
                        # Dcard logo 我的imgur 連結
                        thumbnail_image_url='https://i.imgur.com/JVXiiin.png',
                        actions=[
                            MessageTemplateAction(
                            label='kkbox日榜',
                            text='kkbox日榜'
                        ),
                            MessageTemplateAction(
                                label='熱門低卡',
                                text='熱門低卡'
                        )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
        return 0
