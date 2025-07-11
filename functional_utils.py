"""
函數式程式設計工具模組
提供函數組合、錯誤處理、高階函數等工具
"""

from functools import reduce, wraps
from typing import Callable, Any, Optional, Union, List, Dict, TypeVar, Generic
import logging

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# 型別變數定義
T = TypeVar("T")
U = TypeVar("U")
V = TypeVar("V")
E = TypeVar("E")


# 1. 函數組合工具
def compose(*functions: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """
    函數組合工具 - 從右到左組合函數
    compose(f, g, h)(x) = f(g(h(x)))
    """
    return reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)


def pipe(*functions: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """
    管道工具 - 從左到右組合函數
    pipe(f, g, h)(x) = h(g(f(x)))
    """
    return reduce(lambda f, g: lambda x: g(f(x)), functions, lambda x: x)


# 2. 函數式錯誤處理
class Result(Generic[T, E]):
    """函數式錯誤處理的 Result 類型"""

    def __init__(self, value: Optional[T] = None, error: Optional[E] = None) -> None:
        self._value: Optional[T] = value
        self._error: Optional[E] = error
        self._is_success: bool = error is None

    @classmethod
    def success(cls, value: T) -> "Result[T, E]":
        """創建成功結果"""
        return cls(value=value)

    @classmethod
    def failure(cls, error: E) -> "Result[T, E]":
        """創建失敗結果"""
        return cls(error=error)

    def is_success(self) -> bool:
        """檢查是否成功"""
        return self._is_success

    def is_failure(self) -> bool:
        """檢查是否失敗"""
        return not self._is_success

    def map(self, func: Callable[[T], U]) -> "Result[U, E]":
        """對成功值應用函數"""
        if self.is_success():
            try:
                return Result.success(func(self._value))  # type: ignore
            except Exception as e:
                return Result.failure(str(e))  # type: ignore
        return self  # type: ignore

    def flat_map(self, func: Callable[[T], "Result[U, E]"]) -> "Result[U, E]":
        """對成功值應用返回 Result 的函數"""
        if self.is_success():
            try:
                return func(self._value)  # type: ignore
            except Exception as e:
                return Result.failure(str(e))  # type: ignore
        return self  # type: ignore

    def get_or_else(self, default: T) -> T:
        """獲取值或返回默認值"""
        return self._value if self.is_success() else default  # type: ignore

    def get_error(self) -> Optional[E]:
        """獲取錯誤"""
        return self._error

    def map_err(self, func: Callable[[E], V]) -> "Result[T, V]":
        """對錯誤值應用函數"""
        if self.is_failure():
            try:
                return Result.failure(func(self._error))  # type: ignore
            except Exception as e:
                return Result.failure(str(e))  # type: ignore
        return self  # type: ignore

    def or_else(self, func: Callable[[E], "Result[T, E]"]) -> "Result[T, E]":
        """失敗時嘗試另一個操作"""
        if self.is_failure():
            try:
                return func(self._error)  # type: ignore
            except Exception as e:
                return Result.failure(str(e))  # type: ignore
        return self

    def and_then(self, func: Callable[[T], "Result[U, E]"]) -> "Result[U, E]":
        """flat_map 的別名，更符合其他語言習慣"""
        return self.flat_map(func)

    def unwrap_or(self, default: T) -> T:
        """get_or_else 的別名"""
        return self.get_or_else(default)

    def unwrap_or_else(self, func: Callable[[E], T]) -> T:
        """失敗時通過函數計算預設值"""
        if self.is_success():
            return self._value  # type: ignore
        return func(self._error)  # type: ignore

    def filter(
        self, predicate: Callable[[T], bool], error_msg: str = "Filter predicate failed"
    ) -> "Result[T, E]":
        """根據條件過濾結果"""
        if self.is_success():
            if predicate(self._value):  # type: ignore
                return self
            return Result.failure(error_msg)  # type: ignore
        return self

    def fold(self, on_failure: Callable[[E], U], on_success: Callable[[T], U]) -> U:
        """根據成功或失敗執行不同函數"""
        if self.is_success():
            return on_success(self._value)  # type: ignore
        return on_failure(self._error)  # type: ignore

    def bimap(
        self, error_func: Callable[[E], V], success_func: Callable[[T], U]
    ) -> "Result[U, V]":
        """同時映射成功和失敗的值"""
        if self.is_success():
            return self.map(success_func)  # type: ignore
        return self.map_err(error_func)  # type: ignore

    def tap(self, func: Callable[[T], None]) -> "Result[T, E]":
        """執行副作用但不改變結果"""
        if self.is_success():
            func(self._value)  # type: ignore
        return self

    def tap_err(self, func: Callable[[E], None]) -> "Result[T, E]":
        """對錯誤執行副作用"""
        if self.is_failure():
            func(self._error)  # type: ignore
        return self

    def to_optional(self) -> Optional[T]:
        """轉換為 Optional 類型"""
        return self._value if self.is_success() else None

    def match(self, patterns: Dict[str, Callable[[Any], U]]) -> U:
        """模式匹配風格的處理"""
        if self.is_success() and "Ok" in patterns:
            return patterns["Ok"](self._value)  # type: ignore
        elif self.is_failure() and "Err" in patterns:
            return patterns["Err"](self._error)  # type: ignore
        raise ValueError("Incomplete pattern match")

    @classmethod
    def collect(cls, results: List["Result[T, E]"]) -> "Result[List[T], E]":
        """將 Result 列表轉換為包含列表的 Result"""
        values: List[T] = []
        for result in results:
            if result.is_failure():
                return result  # type: ignore
            values.append(result._value)  # type: ignore
        return cls.success(values)

    @classmethod
    def traverse(
        cls, func: Callable[[T], "Result[U, E]"], items: List[T]
    ) -> "Result[List[U], E]":
        """對列表中每個元素應用函數並收集結果"""
        results: List[U] = []
        for item in items:
            result = func(item)
            if result.is_failure():
                return result  # type: ignore
            results.append(result._value)  # type: ignore
        return cls.success(results)

    @classmethod
    def try_catch(
        cls, func: Callable[..., T], *args: Any, **kwargs: Any
    ) -> "Result[T, str]":
        """將可能拋出異常的函數調用包裝為 Result"""
        try:
            return cls.success(func(*args, **kwargs))
        except Exception as e:
            return cls.failure(str(e))


def safe_execute(func: Callable[..., T]) -> Callable[..., Result[T, str]]:
    """
    安全執行裝飾器 - 將異常轉換為 Result
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Result[T, str]:
        try:
            result = func(*args, **kwargs)
            return Result.success(result)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            return Result.failure(str(e))

    return wrapper


# 3. 高階函數工具
def curry(func: Callable[..., T]) -> Callable[..., Union[T, Callable[..., T]]]:
    """
    柯里化裝飾器
    """

    @wraps(func)
    def curried(*args: Any, **kwargs: Any) -> Union[T, Callable[..., T]]:
        if len(args) + len(kwargs) >= func.__code__.co_argcount:
            return func(*args, **kwargs)
        return lambda *more_args, **more_kwargs: curried(
            *(args + more_args), **{**kwargs, **more_kwargs}
        )

    return curried


def partial_apply(
    func: Callable[..., T], *partial_args: Any, **partial_kwargs: Any
) -> Callable[..., T]:
    """
    部分應用函數
    """

    def wrapper(*args: Any, **kwargs: Any) -> T:
        return func(*(partial_args + args), **{**partial_kwargs, **kwargs})

    return wrapper


def memoize(func: Callable[..., T]) -> Callable[..., T]:
    """
    記憶化裝飾器
    """
    cache: Dict[str, T] = {}

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        key = str(args) + str(sorted(kwargs.items()))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]

    return wrapper


# 4. 函數式數據處理
def filter_map(
    predicate: Callable[[T], bool], mapper: Callable[[T], U], iterable: List[T]
) -> List[U]:
    """
    過濾並映射 - 函數式的 filter + map 組合
    """
    return [mapper(item) for item in iterable if predicate(item)]


def fold_left(func: Callable[[T, U], T], initial: T, iterable: List[U]) -> T:
    """
    左折疊 - reduce 的函數式版本
    """
    return reduce(func, iterable, initial)


def fold_right(func: Callable[[U, T], T], initial: T, iterable: List[U]) -> T:
    """
    右折疊
    """
    return reduce(lambda x, y: func(y, x), reversed(iterable), initial)


# 5. 函數式驗證
def validate_all(
    *validators: Callable[[T], Result[T, E]],
) -> Callable[[T], Result[T, List[E]]]:
    """
    組合多個驗證器
    """

    def validator(value: T) -> Result[T, List[E]]:
        errors: List[E] = []
        for validate_func in validators:
            result = validate_func(value)
            if result.is_failure():
                errors.append(result.get_error())  # type: ignore

        if errors:
            return Result.failure(errors)
        return Result.success(value)

    return validator


def validate_type(expected_type: type) -> Callable[[Any], Result[Any, str]]:
    """
    類型驗證器
    """

    def validator(value: Any) -> Result[Any, str]:
        if isinstance(value, expected_type):
            return Result.success(value)
        return Result.failure(
            f"Expected {expected_type.__name__}, got {type(value).__name__}"
        )

    return validator


def validate_not_empty() -> Callable[[T], Result[T, str]]:
    """
    非空驗證器
    """

    def validator(value: T) -> Result[T, str]:
        if value:
            return Result.success(value)
        return Result.failure("Value cannot be empty")

    return validator
