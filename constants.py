"""
常數定義模組
集中管理專案中的魔術數字和字串
"""

from typing import List


# PTT 相關常數
class PTTConstants:
    """PTT 相關常數"""

    BASE_URL = "https://www.ptt.cc"
    BEAUTY_BOARD_URL = f"{BASE_URL}/bbs/Beauty"
    GOSSIP_BOARD_URL = f"{BASE_URL}/bbs/Gossiping"

    # 推文數相關
    DEFAULT_MIN_PUSH_RATE = 10
    EXPLOSION_PUSH_RATE = 100
    NEGATIVE_PUSH_PREFIX = "X"
    EXPLOSION_PUSH_PREFIX = "爆"
    
    # 多頁瀏覽設定
    DEFAULT_PAGES_TO_CRAWL = 3
    
    # 過濾文章標題
    ANNOUNCEMENT_KEYWORDS = ["公告", "[公告]", "公告：", "置底", "[置底]"]

    # 會話相關
    OVER_18_URL = f"{BASE_URL}/ask/over18"
    OVER_18_FORM_DATA = {"from": "/bbs/Gossiping/index.html", "yes": "yes"}


# 爬蟲相關常數
class CrawlerConstants:
    """爬蟲相關常數"""

    APPLE_NEWS_URL = "https://tw.nextapple.com/"
    TECH_NEWS_URL = "https://technews.tw/"
    MOVIE_URL = "http://www.atmovies.com.tw/movie/next/0/"
    NEW_MOVIE_URL = "https://www.atmovies.com.tw/movie/new/"
    OIL_PRICE_URL = "https://gas.goodlife.tw/"
    PTT_HOT_URL = "https://disp.cc/b/PttHot"

    # 電影資訊限制
    MAX_MOVIE_COUNT = 20
    MAX_NEW_MOVIE_COUNT = 5

    # 蘋果新聞限制
    MAX_NEWS_COUNT = 5

    # 科技新聞限制
    MAX_TECH_NEWS_COUNT = 3
    
    # 熱門廢文限制
    MAX_HOT_POSTS_COUNT = 5


# 貼圖相關常數
class StickerConstants:
    """貼圖相關常數"""

    DEFAULT_PACKAGE_ID = "1"
    AVAILABLE_STICKER_IDS: List[int] = [
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        15,
        16,
        17,
        21,
        100,
        101,
        102,
        103,
        104,
        105,
        106,
        107,
        108,
        109,
        110,
        111,
        112,
        113,
        114,
        115,
        116,
        117,
        118,
        119,
        120,
        121,
        122,
        123,
        124,
        125,
        126,
        127,
        128,
        129,
        130,
        131,
        132,
        133,
        134,
        135,
        136,
        137,
        138,
        139,
        401,
        402,
    ]


# 錯誤訊息常數
class ErrorMessages:
    """錯誤訊息常數"""

    # 網路相關錯誤
    NETWORK_ERROR = "網路連線錯誤，請稍後再試"
    REQUEST_TIMEOUT = "請求逾時，請稍後再試"
    INVALID_URL = "無效的網址格式"

    # 爬蟲相關錯誤
    APPLE_NEWS_FETCH_ERROR = "無法獲取蘋果新聞，可能是網站暫時無法存取"
    TECH_NEWS_FETCH_ERROR = "無法獲取科技新聞，可能是網站暫時無法存取"
    PTT_BEAUTY_FETCH_ERROR = "無法獲取 PTT 表特版資訊，可能是網站暫時無法存取"
    MOVIE_FETCH_ERROR = "無法獲取電影資訊，可能是網站暫時無法存取"
    NEW_MOVIE_FETCH_ERROR = "無法獲取近期上映電影資訊，可能是網站暫時無法存取"
    OIL_PRICE_FETCH_ERROR = "無法獲取油價資訊，可能是網站暫時無法存取"
    PTT_HOT_FETCH_ERROR = "無法獲取熱門廢文資訊，可能是網站暫時無法存取"

    # 解析相關錯誤
    HTML_PARSE_ERROR = "網頁內容解析失敗"
    JSON_PARSE_ERROR = "JSON 資料解析失敗"
    PAGE_NUMBER_PARSE_ERROR = "無法解析頁面編號"

    # 驗證相關錯誤
    EMPTY_CONTENT_ERROR = "內容不能為空"
    INVALID_TYPE_ERROR = "資料類型不正確"
    VALIDATION_FAILED = "資料驗證失敗"

    # 圖片相關錯誤
    IMAGE_FETCH_ERROR = "無法獲取圖片，請稍後再試"
    IMAGE_URL_INVALID = "圖片網址無效"

    # 貼圖相關錯誤
    STICKER_CREATE_ERROR = "無法創建貼圖回應"

    # 通用錯誤
    UNKNOWN_ERROR = "發生未知錯誤"
    SERVICE_UNAVAILABLE = "服務暫時無法使用"
    RATE_LIMIT_EXCEEDED = "請求過於頻繁，請稍後再試"


# 模板相關常數
class TemplateConstants:
    """模板相關常數"""

    # 圖片 URL
    MAIN_MENU_IMAGE = "https://i.imgur.com/xQF5dZT.jpg"
    NEWS_MENU_IMAGE = "https://i.imgur.com/vkqbLnz.png"
    MOVIE_MENU_IMAGE = "https://i.imgur.com/sbOTJt4.png"
    GOSSIP_MENU_IMAGE = "https://i.imgur.com/ocmxAdS.jpg"
    BEAUTY_MENU_IMAGE = "https://i.imgur.com/qKkE2bj.jpg"

    CAROUSEL_IMAGES = [
        "https://i.imgur.com/kzi5kKy.jpg",
        "https://i.imgur.com/DrsmtKS.jpg",
        "https://i.imgur.com/h4UzRit.jpg",
    ]

    # 連結
    YOUTUBE_INTRO_LINK = "https://youtu.be/1IxtWgWxtlE"
    GITHUB_TUTORIAL_LINK = "https://github.com/twtrubiks/line-bot-tutorial"
    FACEBOOK_CONTACT_LINK = "https://www.facebook.com/TWTRubiks?ref=bookmarks"
    PTT_BEAUTY_WEB_LINK = "https://ptt-beauty-infinite-scroll.herokuapp.com/"
    YOUTUBE_CHANNEL_LINK = "https://www.youtube.com/channel/UCPhn2rCqhu0HdktsFjixahA"
    LINE_BOT_SHARE_LINK = "https://line.me/R/nv/recommendOA/@vbi2716y"

    # Alt Text
    MAIN_MENU_ALT = "開始玩 template"
    NEWS_MENU_ALT = "新聞 template"
    MOVIE_MENU_ALT = "電影 template"
    GOSSIP_MENU_ALT = "看廢文 template"
    BEAUTY_MENU_ALT = "正妹 template"
    CAROUSEL_ALT = "目錄 template"


# 日誌相關常數
class LogConstants:
    """日誌相關常數"""

    DEFAULT_LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
