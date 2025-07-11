"""
函數式程式設計測試模組
測試所有函數式組件的正確性
"""

import unittest
from unittest.mock import Mock, patch
from functional_utils import (
    Result,
    compose,
    pipe,
    curry,
    safe_execute,
    filter_map,
    fold_left,
    validate_all,
    validate_type,
    validate_not_empty,
)
from crawlers import (
    fetch_page,
    parse_html,
    format_movie_list,
    format_news_list,
)
from message_handlers import (
    create_text_message,
    create_image_message,
    MessageProcessor,
    create_main_menu_template,
    get_cached_template,
)


class TestFunctionalUtils(unittest.TestCase):
    """測試函數式工具"""

    def test_result_success(self):
        """測試 Result 成功情況"""
        result = Result.success("test value")
        self.assertTrue(result.is_success())
        self.assertFalse(result.is_failure())
        self.assertEqual(result.get_or_else("default"), "test value")

    def test_result_failure(self):
        """測試 Result 失敗情況"""
        result = Result.failure("error message")
        self.assertFalse(result.is_success())
        self.assertTrue(result.is_failure())
        self.assertEqual(result.get_or_else("default"), "default")
        self.assertEqual(result.get_error(), "error message")

    def test_result_map(self):
        """測試 Result map 操作"""
        result = Result.success(5)
        mapped = result.map(lambda x: x * 2)
        self.assertTrue(mapped.is_success())
        self.assertEqual(mapped.get_or_else(0), 10)

        # 測試失敗情況的 map
        failed_result = Result.failure("error")
        mapped_failed = failed_result.map(lambda x: x * 2)
        self.assertTrue(mapped_failed.is_failure())

    def test_result_flat_map(self):
        """測試 Result flat_map 操作"""
        result = Result.success(5)
        flat_mapped = result.flat_map(lambda x: Result.success(x * 2))
        self.assertTrue(flat_mapped.is_success())
        self.assertEqual(flat_mapped.get_or_else(0), 10)

    def test_compose(self):
        """測試函數組合"""
        add_one = lambda x: x + 1
        multiply_two = lambda x: x * 2
        composed = compose(multiply_two, add_one)

        # compose(f, g)(x) = f(g(x))
        # multiply_two(add_one(5)) = multiply_two(6) = 12
        self.assertEqual(composed(5), 12)

    def test_pipe(self):
        """測試管道操作"""
        add_one = lambda x: x + 1
        multiply_two = lambda x: x * 2
        piped = pipe(add_one, multiply_two)

        # pipe(f, g)(x) = g(f(x))
        # multiply_two(add_one(5)) = multiply_two(6) = 12
        self.assertEqual(piped(5), 12)

    def test_curry(self):
        """測試柯里化"""

        @curry
        def add_three_numbers(a, b, c):
            return a + b + c

        # 部分應用
        add_5_and = add_three_numbers(2, 3)
        result = add_5_and(4)
        self.assertEqual(result, 9)

        # 完全應用
        result2 = add_three_numbers(1, 2, 3)
        self.assertEqual(result2, 6)

    def test_safe_execute(self):
        """測試安全執行裝飾器"""

        @safe_execute
        def divide(a, b):
            return a / b

        # 正常情況
        result = divide(10, 2)
        self.assertTrue(result.is_success())
        self.assertEqual(result.get_or_else(0), 5)

        # 異常情況
        result_error = divide(10, 0)
        self.assertTrue(result_error.is_failure())

    def test_filter_map(self):
        """測試 filter_map 函數"""
        numbers = [1, 2, 3, 4, 5, 6]
        result = filter_map(
            lambda x: x % 2 == 0,  # 過濾偶數
            lambda x: x * 2,  # 乘以 2
            numbers,
        )
        self.assertEqual(result, [4, 8, 12])  # [2*2, 4*2, 6*2]

    def test_fold_left(self):
        """測試左折疊"""
        numbers = [1, 2, 3, 4, 5]
        result = fold_left(lambda acc, x: acc + x, 0, numbers)
        self.assertEqual(result, 15)

    def test_validators(self):
        """測試驗證器"""
        # 類型驗證
        type_validator = validate_type(str)
        self.assertTrue(type_validator("hello").is_success())
        self.assertTrue(type_validator(123).is_failure())

        # 非空驗證
        not_empty_validator = validate_not_empty()
        self.assertTrue(not_empty_validator("hello").is_success())
        self.assertTrue(not_empty_validator("").is_failure())

        # 組合驗證
        combined_validator = validate_all(validate_type(str), validate_not_empty())
        self.assertTrue(combined_validator("hello").is_success())
        self.assertTrue(combined_validator("").is_failure())
        self.assertTrue(combined_validator(123).is_failure())


class TestCrawlers(unittest.TestCase):
    """測試爬蟲模組"""

    @patch("crawlers.requests.Session")
    def test_fetch_page_success(self, mock_session_class):
        """測試成功獲取頁面"""
        mock_session = Mock()
        mock_response = Mock()
        mock_response.text = "<html>test</html>"
        mock_response.raise_for_status.return_value = None
        mock_session.get.return_value = mock_response
        mock_session_class.return_value = mock_session

        result = fetch_page("http://example.com")
        self.assertTrue(result.is_success())
        self.assertEqual(result.get_or_else(""), "<html>test</html>")

    @patch("crawlers.requests.Session")
    def test_fetch_page_failure(self, mock_session_class):
        """測試獲取頁面失敗"""
        mock_session = Mock()
        mock_session.get.side_effect = Exception("Network error")
        mock_session_class.return_value = mock_session

        result = fetch_page("http://example.com")
        self.assertTrue(result.is_failure())

    def test_parse_html_success(self):
        """測試 HTML 解析成功"""
        html_content = "<html><body><h1>Test</h1></body></html>"
        result = parse_html(html_content)
        self.assertTrue(result.is_success())

        soup = result.get_or_else(None)
        self.assertIsNotNone(soup)
        self.assertEqual(soup.find("h1").text, "Test")

    def test_format_movie_list(self):
        """測試電影列表格式化"""
        movies = [
            {"title": "Movie 1", "link": "http://example.com/1"},
            {"title": "Movie 2", "link": "http://example.com/2"},
        ]
        result = format_movie_list(movies)
        expected = "Movie 1\nhttp://example.com/1\nMovie 2\nhttp://example.com/2\n"
        self.assertEqual(result, expected)

    def test_format_news_list(self):
        """測試新聞列表格式化"""
        news = [
            {"title": "News 1", "link": "http://news1.com"},
            {"title": "News 2", "link": "http://news2.com"},
        ]
        result = format_news_list(news)
        expected = "News 1\nhttp://news1.com\nNews 2\nhttp://news2.com"
        self.assertEqual(result, expected)

        # 測試空列表情況
        empty_result = format_news_list([])
        self.assertEqual(empty_result, "抱歉，目前無法獲取新聞內容，請稍後再試。")


class TestMessageHandlers(unittest.TestCase):
    """測試消息處理模組"""

    def test_create_text_message(self):
        """測試創建文本消息"""
        result = create_text_message("Hello World")
        self.assertTrue(result.is_success())

        message = result.get_or_else(None)
        self.assertIsNotNone(message)
        self.assertEqual(message.text, "Hello World")

    def test_create_image_message(self):
        """測試創建圖片消息"""
        url = "http://example.com/image.jpg"
        result = create_image_message(url)
        self.assertTrue(result.is_success())

        message = result.get_or_else(None)
        self.assertIsNotNone(message)
        self.assertEqual(message.original_content_url, url)
        self.assertEqual(message.preview_image_url, url)

    def test_create_main_menu_template(self):
        """測試創建主選單模板"""
        template = create_main_menu_template()
        self.assertIsNotNone(template)
        self.assertEqual(template.alt_text, "開始玩 template")

    def test_get_cached_template(self):
        """測試獲取緩存模板"""
        template1 = get_cached_template("main_menu")
        template2 = get_cached_template("main_menu")

        # 由於記憶化，應該返回相同的實例
        self.assertIsNotNone(template1)
        self.assertIsNotNone(template2)

    def test_message_processor_initialization(self):
        """測試消息處理器初始化"""
        mock_crawlers = Mock()
        mock_crawlers.apple_news = Mock(return_value="news content")

        processor = MessageProcessor(mock_crawlers, "http://api.example.com")
        self.assertIsNotNone(processor)
        self.assertIn("開始玩", processor.handlers)

    @patch("message_handlers.get_random_beauty_image")
    def test_message_processor_text_handling(self, mock_get_image):
        """測試消息處理器文本處理"""
        mock_crawlers = Mock()
        mock_crawlers.apple_news = Mock(return_value="news content")

        processor = MessageProcessor(mock_crawlers, "http://api.example.com")

        # 測試開始玩命令
        result = processor.process_text_message("開始玩")
        self.assertTrue(result.is_success())

        # 測試未知命令（應該返回默認輪播）
        result = processor.process_text_message("unknown command")
        self.assertTrue(result.is_success())


class TestIntegration(unittest.TestCase):
    """整合測試"""

    def test_functional_pipeline(self):
        """測試函數式管道整合"""
        # 測試簡單的數據處理管道
        data = [1, 2, 3, 4, 5]

        pipeline = pipe(
            lambda nums: filter(lambda x: x % 2 == 0, nums),  # 過濾偶數
            lambda nums: map(lambda x: x * 2, nums),  # 乘以 2
            list,  # 轉換為列表
        )

        result = pipeline(data)
        self.assertEqual(result, [4, 8])  # [2*2, 4*2]

    def test_error_handling_pipeline(self):
        """測試錯誤處理管道"""

        @safe_execute
        def divide_by_two(x):
            if x == 0:
                raise ValueError("Cannot process zero")
            return x / 2

        @safe_execute
        def multiply_by_three(x):
            return x * 3

        # 成功情況
        result = Result.success(10).flat_map(divide_by_two).flat_map(multiply_by_three)
        self.assertTrue(result.is_success())
        self.assertEqual(result.get_or_else(0), 15)  # (10/2)*3 = 15

        # 失敗情況
        result = Result.success(0).flat_map(divide_by_two).flat_map(multiply_by_three)
        self.assertTrue(result.is_failure())

    def test_curry_with_validation(self):
        """測試柯里化與驗證的結合"""

        @curry
        def validated_add(validator, a, b):
            val_result = validator(a)
            if val_result.is_failure():
                return val_result
            return Result.success(a + b)

        positive_validator = (
            lambda x: Result.success(x) if x > 0 else Result.failure("Must be positive")
        )

        add_positive = validated_add(positive_validator)

        # 成功情況
        result = add_positive(5, 3)
        self.assertTrue(result.is_success())
        self.assertEqual(result.get_or_else(0), 8)

        # 失敗情況
        result = add_positive(-1, 3)
        self.assertTrue(result.is_failure())


if __name__ == "__main__":
    # 運行所有測試
    unittest.main(verbosity=2)
