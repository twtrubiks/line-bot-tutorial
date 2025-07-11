"""
爬蟲模組 - 使用函數式程式設計模式
所有爬蟲函數都是純函數，使用函數組合和錯誤處理
"""

import requests
import re
from bs4 import BeautifulSoup
from typing import List, Dict, Optional, Callable, Any
from functional_utils import (
    safe_execute,
    Result,
    pipe,
    curry,
    filter_map,
    memoize,
    validate_all,
    validate_type,
    validate_not_empty,
)
from constants import CrawlerConstants, PTTConstants, ErrorMessages


# 基礎工具函數
@safe_execute
def fetch_page(url: str, session: Optional[requests.Session] = None) -> str:
    """安全獲取網頁內容"""
    if session is None:
        session = requests.Session()

    response = session.get(url, verify=False)
    response.raise_for_status()
    
    # 修復編碼問題 - 對於特定網站使用 UTF-8 編碼
    if "atmovies.com.tw" in url or "gas.goodlife.tw" in url:
        response.encoding = 'utf-8'
    
    return response.text


@safe_execute
def parse_html(html_content: str) -> BeautifulSoup:
    """解析 HTML 內容"""
    return BeautifulSoup(html_content, "html.parser")


# 驗證器組合
validate_url: Callable[[str], Result[str, List[str]]] = validate_all(
    validate_type(str), validate_not_empty()
)

validate_text: Callable[[str], Result[str, List[str]]] = validate_all(
    validate_type(str), validate_not_empty()
)


# 高階函數 - 爬蟲模板
@curry
def create_crawler(
    url_generator: Callable[..., str],
    content_parser: Callable[[BeautifulSoup], Any],
    formatter: Callable[[Any], str],
) -> Callable[..., Result[str, str]]:
    """
    創建爬蟲的高階函數
    url_generator: 生成 URL 的函數
    content_parser: 解析內容的函數
    formatter: 格式化輸出的函數
    """

    def crawler(*args: Any, **kwargs: Any) -> Result[str, str]:
        url = url_generator(*args, **kwargs)
        return pipe(
            fetch_page,
            lambda result: result.flat_map(parse_html),
            lambda result: result.flat_map(content_parser),
            lambda result: result.map(formatter),
        )(url)

    return crawler


# 內容解析器
@safe_execute
def parse_apple_news_content(soup: BeautifulSoup) -> List[Dict[str, str]]:
    """解析蘋果新聞內容"""

    def extract_news_info(element: Any) -> Dict[str, str]:
        return {
            "title": element.text.strip(),
            "link": element["href"]
            if element["href"].startswith("http")
            else "https://tw.nextapple.com" + element["href"],
        }

    news_elements: List[Any] = soup.select(
        "#main-content > div.post-hot.stories-container > article > div > div:nth-child(1) > h3 > a"
    )[: CrawlerConstants.MAX_NEWS_COUNT]
    return [extract_news_info(elem) for elem in news_elements]


@safe_execute
def parse_tech_news_content(soup: BeautifulSoup) -> List[Dict[str, str]]:
    """解析科技新聞內容"""

    def extract_tech_news_info(element: Any) -> Dict[str, str]:
        link = element.get("href", "")
        if not link.startswith("http"):
            link = "https://technews.tw" + link
        return {"title": element.text.strip(), "link": link}

    def is_valid_article_link(href: str) -> bool:
        """判斷是否為有效的文章連結"""
        if not href:
            return False

        # 排除的連結類型
        exclude_patterns = [
            "javascript:",
            "mailto:",
            "#",
            "facebook.com",
            "twitter.com",
            "youtube.com",
            "/author/",
            "/category/",
            "/tag/",
            "/page/",
        ]

        # 必須是文章連結格式 (包含年份)
        article_pattern = r"/\d{4}/\d{2}/\d{2}/[^/]+/?$"

        return (
            not any(exclude in href for exclude in exclude_patterns)
            and re.search(article_pattern, href) is not None
        )

    # 嘗試多個可能的選擇器，找到文章連結
    selectors = [
        ".slides_a a",  # 主要輪播文章
        ".post-title a",  # 文章標題連結
        "h3 a",  # h3 標題連結
        "h2 a",  # h2 標題連結
        "article a",  # 文章內的連結
        ".entry-title a",  # 文章標題連結
    ]

    tech_news_elements = []
    for selector in selectors:
        elements = soup.select(selector)
        if elements:
            # 過濾出有效的文章連結
            valid_elements = [
                elem
                for elem in elements
                if is_valid_article_link(elem.get("href", ""))
                and elem.text.strip()
                and len(elem.text.strip()) > 10  # 標題長度至少10個字符
            ]
            tech_news_elements.extend(valid_elements)
            if len(tech_news_elements) >= CrawlerConstants.MAX_TECH_NEWS_COUNT:
                break

    # 去重並限制數量
    seen_links = set()
    unique_elements = []
    for elem in tech_news_elements:
        link = elem.get("href", "")
        if (
            link not in seen_links
            and len(unique_elements) < CrawlerConstants.MAX_TECH_NEWS_COUNT
        ):
            seen_links.add(link)
            unique_elements.append(elem)

    return [extract_tech_news_info(elem) for elem in unique_elements]


@safe_execute
def parse_ptt_beauty_content(
    soup: BeautifulSoup, push_rate: int = PTTConstants.DEFAULT_MIN_PUSH_RATE
) -> List[Dict[str, str]]:
    """解析 PTT 表特版內容"""

    def is_announcement(title: str) -> bool:
        """判斷文章是否為公告"""
        return any(keyword in title for keyword in PTTConstants.ANNOUNCEMENT_KEYWORDS)

    def extract_article_info(r_ent):
        try:
            link_elem = r_ent.find("a")
            if not link_elem or not link_elem.get("href"):
                return None

            title = r_ent.find(class_="title").text.strip()
            
            # 過濾公告文章
            if is_announcement(title):
                return None
                
            rate_elem = r_ent.find(class_="nrec")
            rate_text = rate_elem.text if rate_elem else ""

            # 處理推文數
            if rate_text.startswith(PTTConstants.EXPLOSION_PUSH_PREFIX):
                rate = PTTConstants.EXPLOSION_PUSH_RATE
            elif rate_text.startswith(PTTConstants.NEGATIVE_PUSH_PREFIX):
                rate = -1 * int(rate_text[1]) if len(rate_text) > 1 else 0
            elif rate_text.isdigit():
                rate = int(rate_text)
            else:
                rate = 0

            if rate >= push_rate:
                return {
                    "title": title,
                    "url": PTTConstants.BASE_URL + link_elem["href"],
                    "rate": rate,
                }
        except Exception:
            return None

    return filter_map(
        lambda x: x is not None,
        lambda x: x,
        [extract_article_info(elem) for elem in soup.find_all(class_="r-ent")],
    )


@safe_execute
def parse_movie_content(soup: BeautifulSoup) -> List[Dict[str, str]]:
    """解析電影資訊內容"""

    def extract_movie_info(element):
        title = element.text.replace("\t", "").replace("\r", "")
        link = "http://www.atmovies.com.tw" + element["href"]
        return {"title": title, "link": link}

    movie_elements = soup.select("ul.filmNextListAll a")[
        : CrawlerConstants.MAX_MOVIE_COUNT
    ]
    return [extract_movie_info(elem) for elem in movie_elements]


@safe_execute
def parse_new_movie_content(soup: BeautifulSoup) -> List[Dict[str, str]]:
    """解析近期上映電影資訊內容"""

    def extract_new_movie_info(element):
        title = element.text.strip()
        link = "https://www.atmovies.com.tw" + element["href"]
        return {"title": title, "link": link}

    # 選擇電影標題連結 - 基於網站結構分析
    movie_elements = soup.select("article div a")[
        : CrawlerConstants.MAX_NEW_MOVIE_COUNT
    ]
    return [extract_new_movie_info(elem) for elem in movie_elements]


@safe_execute
def parse_oil_price_content(soup: BeautifulSoup) -> Dict[str, str]:
    """解析油價資訊"""
    title = soup.select("#main")[0].text.replace("\n", "").split("(")[0]
    gas_price = soup.select("#gas-price")[0].text.replace("\n\n\n", "").replace(" ", "")
    cpc = soup.select("#cpc")[0].text.replace(" ", "")

    return {"title": title, "gas_price": gas_price, "cpc": cpc}


@safe_execute
def parse_ptt_hot_content(soup: BeautifulSoup) -> List[Dict[str, str]]:
    """解析熱門廢文內容"""
    
    def extract_hot_post_info(link_element) -> Dict[str, str]:
        """提取熱門文章資訊"""
        try:
            href = link_element.get("href", "")
            title = link_element.get_text(strip=True)
            
            # 過濾掉非文章連結
            if not href or "/b/PttHot/" not in href:
                return None
                
            # 過濾掉太短的標題
            if len(title) < 5:
                return None
                
            # 建構完整的 URL
            if href.startswith("/"):
                full_url = "https://disp.cc" + href
            else:
                full_url = href
            
            return {
                "title": title,
                "link": full_url,
                "push_count": "熱門"
            }
        except Exception:
            return None
    
    # 找到所有文章連結
    all_links = soup.find_all("a")
    
    # 提取文章資訊並過濾 None 值
    posts = []
    for link in all_links:
        post_info = extract_hot_post_info(link)
        if post_info and post_info["title"] and post_info["link"]:
            posts.append(post_info)
        
        # 限制數量
        if len(posts) >= CrawlerConstants.MAX_HOT_POSTS_COUNT:
            break
    
    return posts


# 格式化器
def format_movie_list(movies: List[Dict[str, str]]) -> str:
    """格式化電影列表"""
    formatted_movies = [f"{movie['title']}\n{movie['link']}" for movie in movies]
    return "\n".join(formatted_movies) + "\n"


def format_news_list(news: List[Dict[str, str]]) -> str:
    """格式化新聞列表"""
    if not news:
        return "抱歉，目前無法獲取新聞內容，請稍後再試。"
    formatted_news = [f"{item['title']}\n{item['link']}" for item in news]
    return "\n".join(formatted_news)


def format_ptt_articles(articles: List[Dict[str, str]]) -> str:
    """格式化 PTT 文章列表"""
    return "\n".join(
        f"[{article['rate']} push] {article['title']}\n{article['url']}\n"
        for article in articles
    )


def format_oil_price(oil_data: Dict[str, str]) -> str:
    """格式化油價資訊"""
    return f"{oil_data['title']}\n{oil_data['gas_price']}{oil_data['cpc']}"


def format_ptt_hot_posts(posts: List[Dict[str, str]]) -> str:
    """格式化熱門廢文列表"""
    if not posts:
        return "抱歉，目前無法獲取熱門廢文內容，請稍後再試。"
    
    formatted_posts = []
    for i, post in enumerate(posts, 1):
        push_info = f"[{post['push_count']} 推]" if post['push_count'] != "0" else ""
        formatted_posts.append(f"{i}. {push_info} {post['title']}\n{post['link']}")
    
    return "\n\n".join(formatted_posts)


# URL 生成器
def apple_news_url_generator() -> str:
    """蘋果新聞 URL 生成器"""
    return CrawlerConstants.APPLE_NEWS_URL


def tech_news_url_generator() -> str:
    """科技新聞 URL 生成器"""
    return CrawlerConstants.TECH_NEWS_URL


def movie_url_generator() -> str:
    """電影資訊 URL 生成器"""
    return CrawlerConstants.MOVIE_URL


def new_movie_url_generator() -> str:
    """近期上映電影 URL 生成器"""
    return CrawlerConstants.NEW_MOVIE_URL


def oil_price_url_generator() -> str:
    """油價查詢 URL 生成器"""
    return CrawlerConstants.OIL_PRICE_URL


def ptt_hot_url_generator() -> str:
    """熱門廢文 URL 生成器"""
    return CrawlerConstants.PTT_HOT_URL


# 使用高階函數創建具體的爬蟲
apple_news_crawler: Callable[..., Result[str, str]] = create_crawler(
    apple_news_url_generator, parse_apple_news_content, format_news_list
)

tech_news_crawler: Callable[..., Result[str, str]] = create_crawler(
    tech_news_url_generator, parse_tech_news_content, format_news_list
)

movie_crawler: Callable[..., Result[str, str]] = create_crawler(
    movie_url_generator, parse_movie_content, format_movie_list
)

new_movie_crawler: Callable[..., Result[str, str]] = create_crawler(
    new_movie_url_generator, parse_new_movie_content, format_movie_list
)

oil_price_crawler: Callable[..., Result[str, str]] = create_crawler(
    oil_price_url_generator, parse_oil_price_content, format_oil_price
)

ptt_hot_crawler: Callable[..., Result[str, str]] = create_crawler(
    ptt_hot_url_generator, parse_ptt_hot_content, format_ptt_hot_posts
)


# PTT 相關的複雜爬蟲
@safe_execute
def get_page_number(content: str) -> int:
    """從內容中提取頁面號碼"""
    start_index = content.find("index")
    end_index = content.find(".html")
    if start_index == -1 or end_index == -1:
        raise ValueError(ErrorMessages.PAGE_NUMBER_PARSE_ERROR)

    page_number = content[start_index + 5 : end_index]
    return int(page_number) + 1


@safe_execute
def create_ptt_session() -> requests.Session:
    """創建 PTT 會話"""
    session = requests.Session()
    session.post(
        PTTConstants.OVER_18_URL, verify=False, data=PTTConstants.OVER_18_FORM_DATA
    )
    return session


@safe_execute
def get_ptt_beauty_start_page(session: requests.Session) -> int:
    """獲取 PTT 表特版起始頁面編號"""
    index_url = f"{PTTConstants.BEAUTY_BOARD_URL}/index.html"
    page_result = fetch_page(index_url, session)

    if page_result.is_failure():
        raise Exception(page_result.get_error())

    soup_result = parse_html(page_result._value)
    if soup_result.is_failure():
        raise Exception(soup_result.get_error())

    soup = soup_result._value
    all_page_url = soup.select(".btn.wide")[1]["href"]
    page_number_result = get_page_number(all_page_url)

    if page_number_result.is_failure():
        raise Exception(page_number_result.get_error())

    return page_number_result._value


@safe_execute
def fetch_ptt_beauty_articles(
    session: requests.Session, start_page: int, pages_to_crawl: int = PTTConstants.DEFAULT_PAGES_TO_CRAWL
) -> List[Dict[str, str]]:
    """獲取 PTT 表特版多頁文章列表"""
    all_articles = []
    
    for page_offset in range(pages_to_crawl):
        current_page_num = start_page - page_offset
        current_page_url = f"{PTTConstants.BEAUTY_BOARD_URL}/index{current_page_num}.html"
        
        current_page_result = fetch_page(current_page_url, session)
        if current_page_result.is_failure():
            # 如果單頁失敗，繼續下一頁
            continue

        current_soup_result = parse_html(current_page_result._value)
        if current_soup_result.is_failure():
            continue

        articles_result = parse_ptt_beauty_content(current_soup_result._value)
        if articles_result.is_failure():
            continue

        all_articles.extend(articles_result._value)
    
    # 按推文數排序，推文數高的在前面
    all_articles.sort(key=lambda x: x["rate"], reverse=True)
    
    return all_articles


def ptt_beauty_crawler() -> Result[str, str]:
    """PTT 表特版爬蟲 - 使用函數組合改善可讀性"""

    def crawl_beauty() -> str:
        # 建立 PTT 會話
        session_result = create_ptt_session()
        if session_result.is_failure():
            raise Exception(session_result.get_error())

        session = session_result._value

        # 獲取起始頁面編號
        start_page_result = get_ptt_beauty_start_page(session)
        if start_page_result.is_failure():
            raise Exception(start_page_result.get_error())

        start_page = start_page_result._value

        # 獲取文章列表
        articles_result = fetch_ptt_beauty_articles(session, start_page)
        if articles_result.is_failure():
            raise Exception(articles_result.get_error())

        articles = articles_result._value
        return format_ptt_articles(articles)

    return safe_execute(crawl_beauty)()


# 記憶化的爬蟲函數（用於緩存結果）
@memoize
def cached_apple_news() -> Result[str, str]:
    """緩存的蘋果新聞爬蟲"""
    return apple_news_crawler()


@memoize
def cached_tech_news() -> Result[str, str]:
    """緩存的科技新聞爬蟲"""
    return tech_news_crawler()


@memoize
def cached_movie_info() -> Result[str, str]:
    """緩存的電影資訊爬蟲"""
    return movie_crawler()


@memoize
def cached_new_movie_info() -> Result[str, str]:
    """緩存的近期上映電影資訊爬蟲"""
    return new_movie_crawler()


@memoize
def cached_oil_price() -> Result[str, str]:
    """緩存的油價查詢爬蟲"""
    return oil_price_crawler()


@memoize
def cached_ptt_hot() -> Result[str, str]:
    """緩存的熱門廢文爬蟲"""
    return ptt_hot_crawler()


# 導出的主要函數
def apple_news() -> str:
    """蘋果新聞爬蟲主函數"""
    result: Result[str, str] = cached_apple_news()
    return result.get_or_else(ErrorMessages.APPLE_NEWS_FETCH_ERROR)


def tech_news() -> str:
    """科技新聞爬蟲主函數"""
    result: Result[str, str] = cached_tech_news()
    return result.get_or_else(ErrorMessages.TECH_NEWS_FETCH_ERROR)


def movie() -> str:
    """電影資訊爬蟲主函數"""
    result: Result[str, str] = cached_movie_info()
    return result.get_or_else(ErrorMessages.MOVIE_FETCH_ERROR)


def new_movie() -> str:
    """近期上映電影爬蟲主函數"""
    result: Result[str, str] = cached_new_movie_info()
    return result.get_or_else(ErrorMessages.NEW_MOVIE_FETCH_ERROR)


def oil_price() -> str:
    """油價查詢爬蟲主函數"""
    result: Result[str, str] = cached_oil_price()
    return result.get_or_else(ErrorMessages.OIL_PRICE_FETCH_ERROR)


def ptt_beauty() -> str:
    """PTT 表特版爬蟲主函數"""
    result: Result[str, str] = ptt_beauty_crawler()
    return result.get_or_else(ErrorMessages.PTT_BEAUTY_FETCH_ERROR)


def ptt_hot() -> str:
    """熱門廢文爬蟲主函數"""
    result: Result[str, str] = cached_ptt_hot()
    return result.get_or_else(ErrorMessages.PTT_HOT_FETCH_ERROR)
