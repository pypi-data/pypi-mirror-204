""" Kameleoon data module"""
import random
import warnings
from enum import Enum, IntEnum
from typing import Optional, Literal, List, Tuple
from urllib.parse import quote

from kameleoon.exceptions import KameleoonException

ALPHA_NUMERIC_CHARS = "abcdef0123456789"
NONCE_LENGTH = 16


class DataType(Enum):
    """Data types"""

    CUSTOM: str = "CUSTOM"
    BROWSER: str = "BROWSER"
    CONVERSION: str = "CONVERSION"
    DEVICE: str = "DEVICE"
    PAGE_VIEW: str = "PAGE_VIEW"


class BrowserType(IntEnum):
    """Browser types"""

    CHROME: int = 0
    INTERNET_EXPLORER: int = 1
    FIREFOX: int = 2
    SAFARI: int = 3
    OPERA: int = 4
    OTHER: int = 5


class DeviceType(Enum):
    """Device types"""

    PHONE: str = "PHONE"
    TABLET: str = "TABLET"
    DESKTOP: str = "DESKTOP"


def get_nonce() -> str:
    """Generates alphanumeric characters"""
    return "".join(random.choice(ALPHA_NUMERIC_CHARS) for _ in range(NONCE_LENGTH))


class Data:
    """Base data class"""

    def __init__(self) -> None:
        self.nonce: str = get_nonce()
        self.sent: bool = False

    def to_dict(self):
        """Convert class instance to dict"""
        return self.__dict__

    def obtain_full_post_text_line(self) -> str:
        """
        obtain full post text line
        :return:
        """
        raise NotImplementedError

    @classmethod
    def encode(cls, to_encode: str) -> str:
        """
        Encode string to send into URL
        :param to_encode: string which need to encoded
        :type to_encode: str
        :return:
        """
        return quote(to_encode, safe="~()*!.'")


class CustomData(Data):
    """Custom data."""

    @property
    def values(self) -> Tuple[str, ...]:
        """Stored values."""
        return self.__values

    def __init__(self, id: int, *args: str, value: Optional[str] = None):
        """
        :param id: Index / ID of the custom data to be stored. This field is mandatory.
        :type id: int
        :param `*args`: Values of the custom data to be stored. This field is optional.
        :type `*args`: Tuple[str, ...]
        :param value: Single value of the custom data to be stored. This field is optional.
        :type value: Optional[str]

        Example:

        .. code-block:: python3

                kameleoon_client.add_data(visitor_code, CustomData(123, "some-value"))
        """
        # pylint: disable=invalid-name,redefined-builtin
        self.id = str(id)
        if value is None:
            self.__values = args
        else:
            self.__values = (*args, value)
            warnings.warn(
                "Passing deprecated parameter `value`. Please pass variadic parameter list instead.",
                category=DeprecationWarning,
            )
        self.instance = DataType.CUSTOM.value
        super().__init__()

    def obtain_full_post_text_line(self) -> str:
        if len(self.__values) == 0:
            return ""
        str_values = ",".join((f'["{v}",1]' for v in self.__values))
        encoded_value = self.encode(f"[{str_values}]")
        return f"eventType=customData&index={self.id}&valueToCount={encoded_value}&overwrite=true&nonce={self.nonce}"


class Browser(Data):
    """Browser data."""

    def __init__(
        self,
        browser_type: Literal[
            BrowserType.CHROME,
            BrowserType.INTERNET_EXPLORER,
            BrowserType.FIREFOX,
            BrowserType.SAFARI,
            BrowserType.OPERA,
            BrowserType.OTHER,
        ],
    ):
        """
        :param browser_type: Browser type, can be: CHROME, INTERNET_EXPLORER, FIREFOX, SAFARI, OPERA, OTHER

        Example:

        .. code-block:: python3

                kameleoon_client.add_data(visitor_code, Browser(BrowserType.CHROME))
        """
        self.browser = browser_type
        self.instance = DataType.BROWSER.value
        super().__init__()

    def obtain_full_post_text_line(self) -> str:
        if self.browser < 0:
            raise KameleoonException("Browser not recognized")
        return f"eventType=staticData&browser={self.browser}&nonce={self.nonce}"


class PageView(Data):
    """Page view"""

    def __init__(self, url: str, title: str, referrers: Optional[List[int]] = None):
        """
        :param url: Url of the page
        :type url: str
        :param title: Title of the page
        :type title: str
        :param referrers: Optional field - Referrer ids
        :type referrers: Optional[List[int]]

        Example:

        .. code-block:: python3

                kameleoon_client.add_data(visitor_code, PageView("www.test.com", "test-title"))
        """
        self.url = url
        self.title = title
        self.referrers = referrers
        self.instance = DataType.PAGE_VIEW.value
        super().__init__()

    def obtain_full_post_text_line(self) -> str:
        referrer_string = (
            f"&referrersIndices=[{map(str, self.referrers)}]" if self.referrers else ""
        )
        return f"eventType=page&href={self.encode(self.url)}&title={self.title}{referrer_string}&nonce={self.nonce}"  # noqa: E501


class Conversion(Data):
    """Conversion"""

    def __init__(self, goal_id: int, revenue: float = 0.0, negative: bool = False):
        """
        :param goal_id: Id of the goal associated to the conversion
        :type goal_id: int
        :param revenue: Optional field - Revenue associated to the conversion, defaults to 0.0
        :type revenue: float
        :param negative: Optional field - If the revenue is negative. By default it's positive, defaults to False
        :type negative: bool

        Example:

        .. code-block:: python3

                kameleoon_client.add_data(visitor_code, Conversion(1, 100.0))

        """
        self.goal_id = goal_id
        self.revenue = revenue
        self.negative = negative
        self.instance = DataType.CONVERSION.value
        super().__init__()

    def obtain_full_post_text_line(self) -> str:
        return f"eventType=conversion&goalId={self.goal_id}&revenue={self.revenue}&negative={self.negative}&nonce={self.nonce}"  # noqa: E501


class Device(Data):
    """Device data."""

    def __init__(
        self,
        device_type: Literal[DeviceType.PHONE, DeviceType.TABLET, DeviceType.DESKTOP],
    ):
        """
        :param device_type: Device type, can be: PHONE, TABLET, DESKTOP

        Example:
        .. code-block:: python3
                kameleoon_client.add_data(visitor_code, Device(DeviceType.PHONE))
        """
        self.device = device_type.value
        self.instance = DataType.DEVICE.value
        super().__init__()

    def obtain_full_post_text_line(self) -> str:
        if self.device is None:
            raise KameleoonException("Device not recognized")
        return f"eventType=staticData&deviceType={self.device}&nonce={self.nonce}"


class UserAgent:
    """User Agent data"""

    def __init__(self, value: str):
        """
        :param value: User Agent header value which would be used for tracking requests

        Example:
        .. code-block:: python3
                kameleoon_client.add_data(visitor_code, UserAgent('TestUserAgent'))
        """
        self.value = value

    def get_value(self) -> str:
        """
        return user agent value
        :return:
        """
        return self.value
