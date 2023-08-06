import datetime
import logging
import sqlite3

import pandas as pd

from .repository_path import RepositoryPath

logger = logging.getLogger(__name__)

TABLE_STATEMENTS = "statements"
DATA_TYPE_TEXT = "TEXT"
DATA_TYPE_REAL = "REAL"
DATA_DIFINITION = [
    ("DisclosedDate", DATA_TYPE_TEXT),
    ("DisclosedTime", DATA_TYPE_TEXT),
    ("LocalCode", DATA_TYPE_TEXT),
    ("DisclosureNumber", DATA_TYPE_TEXT),
    ("TypeOfDocument", DATA_TYPE_TEXT),
    ("TypeOfCurrentPeriod", DATA_TYPE_TEXT),
    ("CurrentPeriodStartDate", DATA_TYPE_TEXT),
    ("CurrentPeriodEndDate", DATA_TYPE_TEXT),
    ("CurrentFiscalYearEndDate", DATA_TYPE_TEXT),
    ("CurrentFiscalYearStartDate", DATA_TYPE_TEXT),
    ("NextFiscalYearStartDate", DATA_TYPE_TEXT),
    ("NextFiscalYearEndDate", DATA_TYPE_TEXT),
    ("NetSales", DATA_TYPE_REAL),
    ("OperatingProfit", DATA_TYPE_REAL),
    ("OrdinaryProfit", DATA_TYPE_REAL),
    ("Profit", DATA_TYPE_REAL),
    ("EarningsPerShare", DATA_TYPE_REAL),
    ("DilutedEarningsPerShare", DATA_TYPE_REAL),
    ("TotalAssets", DATA_TYPE_REAL),
    ("Equity", DATA_TYPE_REAL),
    ("EquityToAssetRatio", DATA_TYPE_REAL),
    ("BookValuePerShare", DATA_TYPE_REAL),
    ("CashFlowsFromOperatingActivities", DATA_TYPE_REAL),
    ("CashFlowsFromInvestingActivities", DATA_TYPE_REAL),
    ("CashFlowsFromFinancingActivities", DATA_TYPE_REAL),
    ("CashAndEquivalents", DATA_TYPE_REAL),
    ("ResultDividendPerShare1stQuarter", DATA_TYPE_REAL),
    ("ResultDividendPerShare2ndQuarter", DATA_TYPE_REAL),
    ("ResultDividendPerShare3rdQuarter", DATA_TYPE_REAL),
    ("ResultDividendPerShareFiscalYearEnd", DATA_TYPE_REAL),
    ("ResultDividendPerShareAnnual", DATA_TYPE_REAL),
    ("DistributionsPerUnit(REIT)", DATA_TYPE_REAL),
    ("ResultTotalDividendPaidAnnual", DATA_TYPE_REAL),
    ("ResultPayoutRatioAnnual", DATA_TYPE_REAL),
    ("ForecastDividendPerShare1stQuarter", DATA_TYPE_REAL),
    ("ForecastDividendPerShare2ndQuarter", DATA_TYPE_REAL),
    ("ForecastDividendPerShare3rdQuarter", DATA_TYPE_REAL),
    ("ForecastDividendPerShareFiscalYearEnd", DATA_TYPE_REAL),
    ("ForecastDividendPerShareAnnual", DATA_TYPE_REAL),
    ("ForecastDistributionsPerUnit(REIT)", DATA_TYPE_REAL),
    ("ForecastTotalDividendPaidAnnual", DATA_TYPE_REAL),
    ("ForecastPayoutRatioAnnual", DATA_TYPE_REAL),
    ("NextYearForecastDividendPerShare1stQuarter", DATA_TYPE_REAL),
    ("NextYearForecastDividendPerShare2ndQuarter", DATA_TYPE_REAL),
    ("NextYearForecastDividendPerShare3rdQuarter", DATA_TYPE_REAL),
    ("NextYearForecastDividendPerShareFiscalYearEnd", DATA_TYPE_REAL),
    ("NextYearForecastDividendPerShareAnnual", DATA_TYPE_REAL),
    ("NextYearForecastDistributionsPerUnit(REIT)", DATA_TYPE_REAL),
    ("NextYearForecastPayoutRatioAnnual", DATA_TYPE_REAL),
    ("ForecastNetSales2ndQuarter", DATA_TYPE_REAL),
    ("ForecastOperatingProfit2ndQuarter", DATA_TYPE_REAL),
    ("ForecastOrdinaryProfit2ndQuarter", DATA_TYPE_REAL),
    ("ForecastProfit2ndQuarter", DATA_TYPE_REAL),
    ("ForecastEarningsPerShare2ndQuarter", DATA_TYPE_REAL),
    ("NextYearForecastNetSales2ndQuarter", DATA_TYPE_REAL),
    ("NextYearForecastOperatingProfit2ndQuarter", DATA_TYPE_REAL),
    ("NextYearForecastOrdinaryProfit2ndQuarter", DATA_TYPE_REAL),
    ("NextYearForecastProfit2ndQuarter", DATA_TYPE_REAL),
    ("NextYearForecastEarningsPerShare2ndQuarter", DATA_TYPE_REAL),
    ("ForecastNetSales", DATA_TYPE_REAL),
    ("ForecastOperatingProfit", DATA_TYPE_REAL),
    ("ForecastOrdinaryProfit", DATA_TYPE_REAL),
    ("ForecastProfit", DATA_TYPE_REAL),
    ("ForecastEarningsPerShare", DATA_TYPE_REAL),
    ("NextYearForecastNetSales", DATA_TYPE_REAL),
    ("NextYearForecastOperatingProfit", DATA_TYPE_REAL),
    ("NextYearForecastOrdinaryProfit", DATA_TYPE_REAL),
    ("NextYearForecastProfit", DATA_TYPE_REAL),
    ("NextYearForecastEarningsPerShare", DATA_TYPE_REAL),
    ("MaterialChangesInSubsidiaries", DATA_TYPE_REAL),
    ("ChangesBasedOnRevisionsOfAccountingStandard", DATA_TYPE_REAL),
    ("ChangesOtherThanOnesBasedOnRevisionsOfAccountingStandard", DATA_TYPE_REAL),
    ("ChangesInAccountingEstimates", DATA_TYPE_REAL),
    ("RetrospectiveRestatement", DATA_TYPE_REAL),
    ("NumberOfIssuedAndOutstandingSharesAtTheEndOfFiscalYearIncludingTreasuryStock", DATA_TYPE_REAL),
    ("NumberOfTreasuryStockAtTheEndOfFiscalYear", DATA_TYPE_REAL),
    ("AverageNumberOfShares", DATA_TYPE_REAL),
    ("NonConsolidatedNetSales", DATA_TYPE_REAL),
    ("NonConsolidatedOperatingProfit", DATA_TYPE_REAL),
    ("NonConsolidatedOrdinaryProfit", DATA_TYPE_REAL),
    ("NonConsolidatedProfit", DATA_TYPE_REAL),
    ("NonConsolidatedEarningsPerShare", DATA_TYPE_REAL),
    ("NonConsolidatedTotalAssets", DATA_TYPE_REAL),
    ("NonConsolidatedEquity", DATA_TYPE_REAL),
    ("NonConsolidatedEquityToAssetRatio", DATA_TYPE_REAL),
    ("NonConsolidatedBookValuePerShare", DATA_TYPE_REAL),
    ("ForecastNonConsolidatedNetSales2ndQuarter", DATA_TYPE_REAL),
    ("ForecastNonConsolidatedOperatingProfit2ndQuarter", DATA_TYPE_REAL),
    ("ForecastNonConsolidatedOrdinaryProfit2ndQuarter", DATA_TYPE_REAL),
    ("ForecastNonConsolidatedProfit2ndQuarter", DATA_TYPE_REAL),
    ("ForecastNonConsolidatedEarningsPerShare2ndQuarter", DATA_TYPE_REAL),
    ("NextYearForecastNonConsolidatedNetSales2ndQuarter", DATA_TYPE_REAL),
    ("NextYearForecastNonConsolidatedOperatingProfit2ndQuarter", DATA_TYPE_REAL),
    ("NextYearForecastNonConsolidatedOrdinaryProfit2ndQuarter", DATA_TYPE_REAL),
    ("NextYearForecastNonConsolidatedProfit2ndQuarter", DATA_TYPE_REAL),
    ("NextYearForecastNonConsolidatedEarningsPerShare2ndQuarter", DATA_TYPE_REAL),
    ("ForecastNonConsolidatedNetSales", DATA_TYPE_REAL),
    ("ForecastNonConsolidatedOperatingProfit", DATA_TYPE_REAL),
    ("ForecastNonConsolidatedOrdinaryProfit", DATA_TYPE_REAL),
    ("ForecastNonConsolidatedProfit", DATA_TYPE_REAL),
    ("ForecastNonConsolidatedEarningsPerShare", DATA_TYPE_REAL),
    ("NextYearForecastNonConsolidatedNetSales", DATA_TYPE_REAL),
    ("NextYearForecastNonConsolidatedOperatingProfit", DATA_TYPE_REAL),
    ("NextYearForecastNonConsolidatedOrdinaryProfit", DATA_TYPE_REAL),
    ("NextYearForecastNonConsolidatedProfit", DATA_TYPE_REAL),
    ("NextYearForecastNonConsolidatedEarningsPerShare", DATA_TYPE_REAL),
]


class RawStatementsRepository:

    """ダウンロードした生の決算情報をデータベースに挿入するためのレポジトリ"""

    def __init__(self, repository_path: RepositoryPath) -> None:
        self.repository_path = repository_path

    def insert_statements_df(self, df: pd.DataFrame) -> None:
        """データベースに対象日のレコードを挿入する"""

        # 入力のチェック
        if len(df) == 0:
            raise ValueError("DataFrame is empty.")

        if len(df["DisclosedDate"].unique()) != 1:
            raise ValueError("DataFrame contains two or more different disclosed date.")

        keys = [key for key, _ in DATA_DIFINITION]
        if len(df.columns) != len(keys):
            logger.warning("Fields size is different frop expectd size. Check JQuants sepcification updated.")

        # 既にレコードが存在していたら一度削除する
        conn = self.__get_connection()
        date = df["DisclosedDate"][0]
        if self.has_records(date):
            date_str = date.strftime("%Y-%m-%d")
            conn.execute(f"DELETE FROM stock WHERE DisclosedDateDate='{date_str}'")

        # 挿入処理
        df = preprocess_before_insert(df)
        df.to_sql(TABLE_STATEMENTS, conn, if_exists="append", index=False)
        conn.close()

    def drop_index(self) -> None:
        """Indexを落とす"""
        conn = self.__get_connection()
        cur = conn.cursor()
        cur.execute("DROP INDEX IF EXISTS statements_index;")
        conn.commit()
        conn.close()

    def set_index(self) -> None:
        """CodeにIndexを貼る"""
        conn = self.__get_connection()
        cur = conn.cursor()
        cur.execute("CREATE INDEX IF NOT EXISTS statements_index ON statements (LocalCode);")
        conn.commit()
        conn.close()

    def create_table(self) -> None:
        """新しくstockテーブルを生成する"""
        conn = self.__get_connection()
        cur = conn.cursor()

        fields_str = ",".join([f"`{k}` {v}" for k, v in DATA_DIFINITION])
        query = f"""
            CREATE TABLE statements(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            {fields_str}
        );"""
        print(query)
        cur.execute(query)

        conn.commit()
        conn.close()

    def table_exists(self) -> bool:
        """priceテーブルが存在するか判定する"""
        conn = self.__get_connection()
        cur = conn.cursor()
        res = cur.execute("SELECT COUNT(*) FROM sqlite_master WHERE TYPE='table' AND name='statements';")
        size = res.fetchone()
        is_exist: bool = size[0] > 0
        conn.commit()
        conn.close()
        return is_exist

    def has_records(self, date: datetime.date) -> bool:
        """対象日のデータが存在するか確認する"""
        if not isinstance(date, datetime.date):
            raise TypeError("date must be 'datetiem.date'")
        date_str = date.strftime("%Y-%m-%d")
        conn = self.__get_connection()
        res = conn.execute(f"SELECT COUNT(*) FROM statements WHERE DisclosedDate='{date_str}';")
        size = res.fetchone()
        is_exist: bool = size[0] > 0
        conn.close()
        return is_exist

    def records_size(self) -> int:
        """データ総数を取得"""
        conn = self.__get_connection()
        cur = conn.cursor()
        res = cur.execute("SELECT COUNT(*) FROM statements;")
        size: int = res.fetchone()[0]
        conn.commit()
        conn.close()
        return size

    def __get_connection(self) -> sqlite3.Connection:
        db_path = self.repository_path.sqlite_path
        conn = sqlite3.connect(db_path)
        return conn


def preprocess_before_insert(df: pd.DataFrame) -> pd.DataFrame:
    """Unicode型をSqliteが扱えないので予め処理する"""
    df = df.replace("－", None)
    df["DisclosedDate"] = df["DisclosedDate"].dt.strftime("%Y-%m-%d")
    return df
