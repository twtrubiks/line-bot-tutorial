"""
消息處理模組 - 使用函數式程式設計模式
處理 Line Bot 的各種消息類型和回應
"""

import random
import requests
from typing import Dict, Callable, Optional, Any, Union, Tuple
from linebot.v3.messaging import (
    TextMessage,
    ImageMessage,
    TemplateMessage,
    ButtonsTemplate,
    CarouselTemplate,
    CarouselColumn,
    MessageAction,
    URIAction,
    StickerMessage,
)
from functional_utils import safe_execute, Result, pipe, curry, partial_apply, memoize
from constants import StickerConstants, TemplateConstants, ErrorMessages


# 消息類型定義
MessageType = Union[TextMessage, ImageMessage, TemplateMessage, StickerMessage]
MessageHandler = Callable[[str], Result[MessageType, str]]
TemplateBuilder = Callable[[], TemplateMessage]


# 基礎工具函數
@safe_execute
def create_text_message(content: str) -> TextMessage:
    """創建文本消息"""
    return TextMessage(text=content)


@safe_execute
def create_image_message(url: str) -> ImageMessage:
    """創建圖片消息"""
    return ImageMessage(original_content_url=url, preview_image_url=url)


@safe_execute
def create_sticker_message(package_id: str, sticker_id: str) -> StickerMessage:
    """創建貼圖消息"""
    return StickerMessage(package_id=package_id, sticker_id=sticker_id)


# 高階函數 - 消息處理器工廠
@curry
def create_message_handler(
    content_fetcher: Callable[[], str], message_creator: Callable[[str], MessageType]
) -> MessageHandler:
    """
    創建消息處理器的高階函數
    content_fetcher: 獲取內容的函數
    message_creator: 創建消息的函數
    """

    def handler(text: str) -> Result[MessageType, str]:
        return pipe(
            lambda _: content_fetcher(),
            lambda content: Result.success(content)
            if content
            else Result.failure("No content"),
            lambda result: result.flat_map(message_creator),
        )(text)

    return handler


# 模板建構器
def create_main_menu_template() -> TemplateMessage:
    """創建主選單模板"""
    buttons_template = ButtonsTemplate(
        title="選擇服務",
        text="請選擇",
        thumbnail_image_url=TemplateConstants.MAIN_MENU_IMAGE,
        actions=[
            MessageAction(label="新聞", text="新聞"),
            MessageAction(label="電影", text="電影"),
            MessageAction(label="看廢文", text="看廢文"),
            MessageAction(label="正妹", text="正妹"),
        ],
    )
    return TemplateMessage(
        alt_text=TemplateConstants.MAIN_MENU_ALT, template=buttons_template
    )


def create_news_menu_template() -> TemplateMessage:
    """創建新聞選單模板"""
    buttons_template = ButtonsTemplate(
        title="新聞類型",
        text="請選擇",
        thumbnail_image_url=TemplateConstants.NEWS_MENU_IMAGE,
        actions=[
            MessageAction(label="蘋果即時新聞", text="蘋果即時新聞"),
            MessageAction(label="科技新報", text="科技新報"),
        ],
    )
    return TemplateMessage(
        alt_text=TemplateConstants.NEWS_MENU_ALT, template=buttons_template
    )


def create_movie_menu_template() -> TemplateMessage:
    """創建電影選單模板"""
    buttons_template = ButtonsTemplate(
        title="服務類型",
        text="請選擇",
        thumbnail_image_url=TemplateConstants.MOVIE_MENU_IMAGE,
        actions=[
            MessageAction(label="近期上映電影", text="近期上映電影"),
        ],
    )
    return TemplateMessage(
        alt_text=TemplateConstants.MOVIE_MENU_ALT, template=buttons_template
    )


def create_gossip_menu_template() -> TemplateMessage:
    """創建廢文選單模板"""
    buttons_template = ButtonsTemplate(
        title="你媽知道你在看廢文嗎",
        text="請選擇",
        thumbnail_image_url=TemplateConstants.GOSSIP_MENU_IMAGE,
        actions=[
            MessageAction(label="近期熱門廢文", text="近期熱門廢文"),
        ],
    )
    return TemplateMessage(
        alt_text=TemplateConstants.GOSSIP_MENU_ALT, template=buttons_template
    )


def create_beauty_menu_template() -> TemplateMessage:
    """創建正妹選單模板"""
    buttons_template = ButtonsTemplate(
        title="選擇服務",
        text="請選擇",
        thumbnail_image_url=TemplateConstants.BEAUTY_MENU_IMAGE,
        actions=[
            MessageAction(
                label="PTT 表特版 近期大於 10 推的文章",
                text="PTT 表特版 近期大於 10 推的文章",
            ),
            MessageAction(label="隨便來張正妹圖片", text="隨便來張正妹圖片"),
        ],
    )
    return TemplateMessage(
        alt_text=TemplateConstants.BEAUTY_MENU_ALT, template=buttons_template
    )


def create_default_carousel_template() -> TemplateMessage:
    """創建默認輪播模板"""
    carousel_template = CarouselTemplate(
        columns=[
            CarouselColumn(
                thumbnail_image_url=TemplateConstants.CAROUSEL_IMAGES[0],
                title="選擇服務",
                text="請選擇",
                actions=[
                    MessageAction(label="開始玩", text="開始玩"),
                    URIAction(
                        label="影片介紹 阿肥bot",
                        uri=TemplateConstants.YOUTUBE_INTRO_LINK,
                    ),
                    URIAction(
                        label="如何建立自己的 Line Bot",
                        uri=TemplateConstants.GITHUB_TUTORIAL_LINK,
                    ),
                ],
            ),
            CarouselColumn(
                thumbnail_image_url=TemplateConstants.CAROUSEL_IMAGES[1],
                title="選擇服務",
                text="請選擇",
                actions=[
                    MessageAction(label="other bot", text="imgur bot"),
                    MessageAction(label="油價查詢", text="油價查詢"),
                    URIAction(
                        label="聯絡作者", uri=TemplateConstants.FACEBOOK_CONTACT_LINK
                    ),
                ],
            ),
            CarouselColumn(
                thumbnail_image_url=TemplateConstants.CAROUSEL_IMAGES[2],
                title="選擇服務",
                text="請選擇",
                actions=[
                    URIAction(
                        label="分享 bot", uri=TemplateConstants.LINE_BOT_SHARE_LINK
                    ),
                    URIAction(
                        label="PTT正妹網", uri=TemplateConstants.PTT_BEAUTY_WEB_LINK
                    ),
                    URIAction(
                        label="youtube 程式教學分享頻道",
                        uri=TemplateConstants.YOUTUBE_CHANNEL_LINK,
                    ),
                ],
            ),
        ]
    )
    return TemplateMessage(
        alt_text=TemplateConstants.CAROUSEL_ALT, template=carousel_template
    )


# 特殊處理函數
@safe_execute
def get_random_beauty_image(api_url: str) -> str:
    """獲取隨機正妹圖片"""
    response = requests.get(api_url)
    response.raise_for_status()
    return response.json().get("Url", "")


@safe_execute
def get_random_sticker() -> Tuple[str, str]:
    """獲取隨機貼圖"""
    sticker_id: str = str(random.choice(StickerConstants.AVAILABLE_STICKER_IDS))
    return (StickerConstants.DEFAULT_PACKAGE_ID, sticker_id)


# 消息處理器映射
class MessageProcessor:
    """消息處理器類 - 使用函數式設計"""

    def __init__(self, crawlers_module: Any, api_get_image: str) -> None:
        self.crawlers = crawlers_module
        self.api_get_image: str = api_get_image

        # 使用部分應用創建專用處理器
        self.text_handler = partial_apply(
            create_message_handler, message_creator=create_text_message
        )
        self.template_handler: Callable[[TemplateBuilder], MessageHandler] = (
            lambda template_func: lambda _: Result.success(template_func())
        )

        # 建立消息處理映射
        self.handlers: Dict[str, MessageHandler] = self._build_handlers()

    def _build_handlers(self) -> Dict[str, MessageHandler]:
        """建立消息處理器映射"""
        return {
            # 爬蟲相關
            "蘋果即時新聞": self.text_handler(self.crawlers.apple_news),
            "科技新報": self.text_handler(self.crawlers.tech_news),
            "PTT 表特版 近期大於 10 推的文章": self.text_handler(
                self.crawlers.ptt_beauty
            ),
            "近期上映電影": self.text_handler(self.crawlers.new_movie),
            "油價查詢": self.text_handler(self.crawlers.oil_price),
            "近期熱門廢文": self.text_handler(self.crawlers.ptt_hot),
            # 模板相關
            "開始玩": self.template_handler(create_main_menu_template),
            "新聞": self.template_handler(create_news_menu_template),
            "電影": self.template_handler(create_movie_menu_template),
            "看廢文": self.template_handler(create_gossip_menu_template),
            "正妹": self.template_handler(create_beauty_menu_template),
            # 特殊處理
            "隨便來張正妹圖片": self._handle_random_image,
        }

    def _handle_random_image(self, text: str) -> Result[MessageType, str]:
        """處理隨機圖片請求"""
        url_result: Result[str, str] = get_random_beauty_image(self.api_get_image)
        if url_result.is_success():
            return create_image_message(url_result._value)  # type: ignore
        return Result.failure(ErrorMessages.IMAGE_FETCH_ERROR)

    def process_text_message(self, text: str) -> Result[MessageType, str]:
        """處理文本消息"""
        # 標準化輸入
        normalized_text: str = text.strip()

        # 檢查是否有對應的處理器
        if normalized_text in self.handlers:
            return self.handlers[normalized_text](normalized_text)
        else:
            # 默認回應
            return Result.success(create_default_carousel_template())

    def process_sticker_message(self) -> Result[MessageType, str]:
        """處理貼圖消息"""
        sticker_result: Result[Tuple[str, str], str] = get_random_sticker()
        if sticker_result.is_success():
            package_id, sticker_id = sticker_result._value  # type: ignore
            return create_sticker_message(package_id, sticker_id)  # type: ignore
        return Result.failure(ErrorMessages.STICKER_CREATE_ERROR)


# 函數式的消息處理管道
def create_message_pipeline(
    processor: MessageProcessor,
) -> Callable[[str], Result[MessageType, str]]:
    """創建消息處理管道"""

    def pipeline(message_text: str) -> Result[MessageType, str]:
        return pipe(
            lambda text: text.strip(), lambda text: processor.process_text_message(text)
        )(message_text)

    return pipeline


# 記憶化的處理器（用於緩存模板）
@memoize
def get_cached_template(template_name: str) -> TemplateMessage:
    """獲取緩存的模板"""
    template_builders: Dict[str, TemplateBuilder] = {
        "main_menu": create_main_menu_template,
        "news_menu": create_news_menu_template,
        "movie_menu": create_movie_menu_template,
        "gossip_menu": create_gossip_menu_template,
        "beauty_menu": create_beauty_menu_template,
        "default_carousel": create_default_carousel_template,
    }

    builder: Optional[TemplateBuilder] = template_builders.get(template_name)
    if builder:
        return builder()
    return create_default_carousel_template()


# 導出的工廠函數
def create_message_processor(
    crawlers_module: Any, api_get_image: str
) -> MessageProcessor:
    """創建消息處理器實例"""
    return MessageProcessor(crawlers_module, api_get_image)
