"""
驗證工具模組 (Validation Utilities)

此模組包含所有資料驗證函數，用於 Pydantic schemas 的欄位驗證。

使用方式:
    from .validators import validate_phone_number, validate_url

    class MySchema(BaseModel):
        @field_validator('phone')
        @classmethod
        def validate_phone_format(cls, v):
            return validate_phone_number(v)
"""

import re
from typing import Optional


def validate_phone_number(phone: Optional[str]) -> Optional[str]:
    """
    驗證電話號碼格式（寬鬆驗證，適合災害救援情境）

    支援格式（接受有無"-"分隔符號）：
    - 手機: 09XX-XXXXXX, 09XXXXXXXX, 9XXXXXXXX (容許缺少前導0)
    - 市話(含區碼): 0X-XXXXXXX, 0X-XXXXXXXX (如: 03-8701129, 038701129)
    - 市話(僅本地號碼): 7-8碼本地號碼，不含區碼 (如: 8701129, 870-1129)
      註：允許僅輸入本地號碼，因災區民眾可能省略區碼
    - 免付費: 0800-XXX-XXX, 0800XXXXXX
    - 國際: +886-X-XXX-XXX, +886XXXXXXXXX (台灣國際碼)

    註：驗證前會自動移除空白、"-"、"()"等分隔符號

    Args:
        phone: 電話號碼字串

    Returns:
        原始電話號碼（若有效）或 None

    Raises:
        ValueError: 當電話號碼格式不正確時

    Examples:
        >>> validate_phone_number("03-8701129")
        "03-8701129"
        >>> validate_phone_number("0937175360")
        "0937175360"
        >>> validate_phone_number("8701129")  # 僅本地號碼
        "8701129"
    """
    if not phone:
        return phone

    # 移除空白和常見分隔符號，保留+號(國際碼)
    clean_phone = re.sub(r'[\s\-()]', '', phone)

    # 支援的電話格式（按優先順序檢查）：
    patterns = [
        r'^09\d{8}$',           # 手機: 09XXXXXXXX (10位)
        r'^9\d{8}$',            # 手機(缺0): 9XXXXXXXX (9位，向後兼容CSV資料)
        r'^0[2-8]\d{7,8}$',     # 市話含區碼: 02-08開頭 (9-10位)
        r'^\d{7,8}$',           # 僅本地號碼: 7-8位數字 (允許省略區碼)
        r'^0800\d{6}$',         # 免付費: 0800XXXXXX (10位)
        r'^\+886[2-9]\d{7,8}$', # 國際格式: +886XXXXXXXXX
    ]

    for pattern in patterns:
        if re.match(pattern, clean_phone):
            return phone

    raise ValueError(f'電話號碼格式不正確: {phone}')


def validate_url(url: Optional[str]) -> Optional[str]:
    """
    驗證URL格式（寬鬆驗證）

    支援格式：
    - https://example.com
    - http://example.com
    - www.example.com (允許省略 http(s)://)

    Args:
        url: URL字串

    Returns:
        原始URL（若有效）或 None

    Raises:
        ValueError: 當URL格式不正確時

    Examples:
        >>> validate_url("https://maps.google.com")
        "https://maps.google.com"
        >>> validate_url("www.example.com")
        "www.example.com"
    """
    if not url:
        return url

    # URL格式驗證：允許 http(s):// 開頭或 www. 開頭
    url_patterns = [
        r'^https?://[^\s]+$',  # http:// 或 https:// 開頭
        r'^www\.[^\s]+$',      # www. 開頭（允許省略協定）
    ]

    for pattern in url_patterns:
        if re.match(pattern, url):
            return url

    raise ValueError(f'URL格式不正確: {url}')
