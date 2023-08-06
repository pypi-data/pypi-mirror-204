from typing import Any


class Brand:

    """銘柄情報を扱うクラス"""

    def __init__(
        self, code: str, company_name: str, sector17: str, sector33: str, scale_category: str, market_code: str
    ) -> None:
        self.code = code
        self.company_name = company_name
        self.sector17 = sector17
        self.sector33 = sector33
        self.scale_category = scale_category
        self.market_code = market_code

    def __repr__(self) -> str:
        return self.company_name

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Brand):
            raise TypeError("other must be Brand object.")
        return other.code == self.code
