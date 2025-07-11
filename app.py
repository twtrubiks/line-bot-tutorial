"""
Line Bot 主應用程式 - 函數式程式設計版本
使用函數組合、錯誤處理、高階函數等函數式設計模式
"""

import configparser
from typing import Callable
from flask import Flask, request, abort
from linebot.v3 import WebhookHandler
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent, StickerMessageContent

# 導入函數式模組
from functional_utils import safe_execute, Result
from message_handlers import (
    create_message_processor,
    create_message_pipeline,
    MessageProcessor,
    MessageType,
)
import crawlers

# 應用程式初始化
app = Flask(__name__)


# 配置載入
@safe_execute
def load_config() -> configparser.ConfigParser:
    """安全載入配置文件"""
    config: configparser.ConfigParser = configparser.ConfigParser()
    config.read("config.ini")
    return config


# 初始化配置
config_result: Result[configparser.ConfigParser, str] = load_config()
if config_result.is_failure():
    raise RuntimeError(f"Failed to load config: {config_result.get_error()}")

config: configparser.ConfigParser = config_result._value  # type: ignore

# Line Bot 配置
configuration: Configuration = Configuration(
    access_token=config["line_bot"]["Channel_Access_Token"]
)
handler: WebhookHandler = WebhookHandler(config["line_bot"]["Channel_Secret"])
API_Get_Image: str = config["other_api"]["API_Get_Image"]

# 創建消息處理器
message_processor: MessageProcessor = create_message_processor(crawlers, API_Get_Image)
message_pipeline: Callable[[str], Result[MessageType, str]] = create_message_pipeline(
    message_processor
)


# 函數式的回調處理
@safe_execute
def process_webhook(signature: str, body: str) -> str:
    """處理 webhook 請求"""
    handler.handle(body, signature)
    return "OK"


@app.route("/callback", methods=["POST"])
def callback() -> str:
    """Webhook 回調端點"""
    signature: str = request.headers.get("X-Line-Signature", "")
    body: str = request.get_data(as_text=True)

    app.logger.info(f"Request body: {body}")

    result: Result[str, str] = process_webhook(signature, body)

    if result.is_failure():
        app.logger.error(f"Webhook processing failed: {result.get_error()}")
        if "Invalid signature" in str(result.get_error()):
            abort(400)
        abort(500)

    return result.get_or_else("OK")


# 函數式的消息回應處理
@safe_execute
def send_reply_message(
    line_bot_api: MessagingApi, reply_token: str, message: MessageType
) -> str:
    """發送回覆消息"""
    line_bot_api.reply_message(
        ReplyMessageRequest(reply_token=reply_token, messages=[message])
    )
    return "Message sent successfully"


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event: MessageEvent) -> None:
    """函數式的文本消息處理器"""
    with ApiClient(configuration) as api_client:
        line_bot_api: MessagingApi = MessagingApi(api_client)

        app.logger.info(f"Received message: {event.message.text}")

        # 使用函數式管道處理消息
        message_result: Result[MessageType, str] = message_pipeline(event.message.text)

        if message_result.is_success():
            message: MessageType = message_result._value  # type: ignore
            reply_result: Result[str, str] = send_reply_message(
                line_bot_api, event.reply_token, message
            )

            if reply_result.is_failure():
                app.logger.error(f"Failed to send reply: {reply_result.get_error()}")
        else:
            app.logger.error(f"Failed to process message: {message_result.get_error()}")
            # 發送錯誤回應
            error_message: Result[MessageType, str] = (
                message_processor.process_text_message("開始玩")
            )
            if error_message.is_success():
                send_reply_message(
                    line_bot_api, event.reply_token, error_message._value
                )  # type: ignore


@handler.add(MessageEvent, message=StickerMessageContent)
def handle_sticker_message(event: MessageEvent) -> None:
    """函數式的貼圖消息處理器"""
    with ApiClient(configuration) as api_client:
        line_bot_api: MessagingApi = MessagingApi(api_client)

        app.logger.info(
            f"Received sticker - package_id: {event.message.package_id}, sticker_id: {event.message.sticker_id}"
        )

        # 使用函數式方法處理貼圖回應
        sticker_result: Result[MessageType, str] = (
            message_processor.process_sticker_message()
        )

        if sticker_result.is_success():
            sticker_message: MessageType = sticker_result._value  # type: ignore
            reply_result: Result[str, str] = send_reply_message(
                line_bot_api, event.reply_token, sticker_message
            )

            if reply_result.is_failure():
                app.logger.error(
                    f"Failed to send sticker reply: {reply_result.get_error()}"
                )
        else:
            app.logger.error(f"Failed to process sticker: {sticker_result.get_error()}")


if __name__ == "__main__":
    app.logger.info("Starting Line Bot with Functional Programming architecture")
    app.run(debug=True)
