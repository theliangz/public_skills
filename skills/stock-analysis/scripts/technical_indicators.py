"""
股票技术指标计算工具
计算常用的技术分析指标，辅助股票筛选决策
"""

from typing import List, Tuple, Dict
from dataclasses import dataclass
from enum import Enum


class SignalType(Enum):
    """信号类型"""
    BUY = "买入信号"
    SELL = "卖出信号"
    NEUTRAL = "中性"
    HOLD = "持有"


@dataclass
class TechnicalSignal:
    """技术信号数据类"""
    indicator: str
    signal: SignalType
    value: float
    description: str


class TechnicalIndicators:
    """技术指标计算类"""

    @staticmethod
    def calculate_macd(prices: List[float], fast=12, slow=26, signal=9) -> Dict[str, float]:
        """
        计算MACD指标

        Args:
            prices: 价格序列（收盘价）
            fast: 快速EMA周期
            slow: 慢速EMA周期
            signal: 信号线周期

        Returns:
            Dict[str, float]: 包含MACD、Signal、Histogram的字典
        """
        if len(prices) < slow + signal:
            return {"MACD": 0, "Signal": 0, "Histogram": 0}

        # 简化的EMA计算（实际应用中应使用更精确的方法）
        def ema(data, period):
            return sum(data[-period:]) / period

        ema_fast = ema(prices, fast)
        ema_slow = ema(prices, slow)
        macd = ema_fast - ema_slow

        # 简化的信号线计算
        signal_line = macd * 0.8  # 简化处理
        histogram = macd - signal_line

        return {
            "MACD": round(macd, 4),
            "Signal": round(signal_line, 4),
            "Histogram": round(histogram, 4)
        }

    @staticmethod
    def calculate_kdj(highs: List[float], lows: List[float], closes: List[float], n=9) -> Dict[str, float]:
        """
        计算KDJ指标

        Args:
            highs: 最高价序列
            lows: 最低价序列
            closes: 收盘价序列
            n: 计算周期

        Returns:
            Dict[str, float]: 包含K、D、J的字典
        """
        if len(closes) < n:
            return {"K": 50, "D": 50, "J": 50}

        high_n = max(highs[-n:])
        low_n = min(lows[-n:])
        close = closes[-1]

        if high_n == low_n:
            rsv = 50
        else:
            rsv = (close - low_n) / (high_n - low_n) * 100

        # 简化的K、D、J计算
        k = rsv * (1/3) + 50 * (2/3)
        d = k * (1/3) + 50 * (2/3)
        j = 3 * k - 2 * d

        return {
            "K": round(k, 2),
            "D": round(d, 2),
            "J": round(j, 2)
        }

    @staticmethod
    def calculate_rsi(prices: List[float], period=14) -> float:
        """
        计算RSI指标

        Args:
            prices: 价格序列
            period: 计算周期

        Returns:
            float: RSI值
        """
        if len(prices) < period + 1:
            return 50.0

        gains = []
        losses = []

        for i in range(len(prices) - 1, len(prices) - period - 1, -1):
            change = prices[i] - prices[i - 1]
            if change > 0:
                gains.append(change)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(change))

        avg_gain = sum(gains) / period
        avg_loss = sum(losses) / period

        if avg_loss == 0:
            return 100.0

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        return round(rsi, 2)

    @staticmethod
    def analyze_volume(current_volume: float, avg_volume: float) -> TechnicalSignal:
        """
        分析成交量

        Args:
            current_volume: 当前成交量
            avg_volume: 平均成交量

        Returns:
            TechnicalSignal: 成交量分析信号
        """
        ratio = current_volume / avg_volume if avg_volume > 0 else 1

        if ratio >= 2.0:
            return TechnicalSignal(
                indicator="成交量",
                signal=SignalType.BUY,
                value=ratio,
                description=f"放量明显，成交量是均量的{ratio:.1f}倍"
            )
        elif ratio >= 1.5:
            return TechnicalSignal(
                indicator="成交量",
                signal=SignalType.BUY,
                value=ratio,
                description=f"温和放量，成交量是均量的{ratio:.1f}倍"
            )
        elif ratio <= 0.5:
            return TechnicalSignal(
                indicator="成交量",
                signal=SignalType.SELL,
                value=ratio,
                description=f"缩量明显，成交量仅为均量的{ratio:.1f}倍"
            )
        else:
            return TechnicalSignal(
                indicator="成交量",
                signal=SignalType.NEUTRAL,
                value=ratio,
                description=f"成交量正常，是均量的{ratio:.1f}倍"
            )

    @staticmethod
    def analyze_macd_signal(macd_data: Dict[str, float]) -> TechnicalSignal:
        """
        分析MACD信号

        Args:
            macd_data: MACD数据字典

        Returns:
            TechnicalSignal: MACD分析信号
        """
        histogram = macd_data.get("Histogram", 0)

        if histogram > 0:
            if histogram > 0.5:
                return TechnicalSignal(
                    indicator="MACD",
                    signal=SignalType.BUY,
                    value=histogram,
                    description="MACD金叉且柱状线扩大，买入信号较强"
                )
            else:
                return TechnicalSignal(
                    indicator="MACD",
                    signal=SignalType.BUY,
                    value=histogram,
                    description="MACD金叉，有买入迹象"
                )
        else:
            if histogram < -0.5:
                return TechnicalSignal(
                    indicator="MACD",
                    signal=SignalType.SELL,
                    value=histogram,
                    description="MACD死叉且柱状线扩大，卖出信号较强"
                )
            else:
                return TechnicalSignal(
                    indicator="MACD",
                    signal=SignalType.HOLD,
                    value=histogram,
                    description="MACD死叉，观望为宜"
                )

    @staticmethod
    def analyze_kdj_signal(kdj_data: Dict[str, float]) -> TechnicalSignal:
        """
        分析KDJ信号

        Args:
            kdj_data: KDJ数据字典

        Returns:
            TechnicalSignal: KDJ分析信号
        """
        k = kdj_data.get("K", 50)
        d = kdj_data.get("D", 50)
        j = kdj_data.get("J", 50)

        if k < 20 and d < 20:
            return TechnicalSignal(
                indicator="KDJ",
                signal=SignalType.BUY,
                value=k,
                description=f"KDJ低位(K={k}, D={d})，超卖区域，可能反弹"
            )
        elif k > 80 and d > 80:
            return TechnicalSignal(
                indicator="KDJ",
                signal=SignalType.SELL,
                value=k,
                description=f"KDJ高位(K={k}, D={d})，超买区域，注意回调"
            )
        elif k > d and j > 100:
            return TechnicalSignal(
                indicator="KDJ",
                signal=SignalType.BUY,
                value=k,
                description=f"KDJ金叉且J线强势(J={j})，买入信号"
            )
        elif k < d:
            return TechnicalSignal(
                indicator="KDJ",
                signal=SignalType.SELL,
                value=k,
                description=f"KDJ死叉，卖出信号"
            )
        else:
            return TechnicalSignal(
                indicator="KDJ",
                signal=SignalType.NEUTRAL,
                value=k,
                description=f"KDJ中性区域(K={k}, D={d})，观望"
            )

    @staticmethod
    def analyze_rsi_signal(rsi: float) -> TechnicalSignal:
        """
        分析RSI信号

        Args:
            rsi: RSI值

        Returns:
            TechnicalSignal: RSI分析信号
        """
        if rsi < 30:
            return TechnicalSignal(
                indicator="RSI",
                signal=SignalType.BUY,
                value=rsi,
                description=f"RSI={rsi}，超卖区域，可能反弹"
            )
        elif rsi > 70:
            return TechnicalSignal(
                indicator="RSI",
                signal=SignalType.SELL,
                value=rsi,
                description=f"RSI={rsi}，超买区域，注意回调风险"
            )
        elif 40 <= rsi <= 60:
            return TechnicalSignal(
                indicator="RSI",
                signal=SignalType.NEUTRAL,
                value=rsi,
                description=f"RSI={rsi}，中性区域，趋势不明"
            )
        elif rsi > 50:
            return TechnicalSignal(
                indicator="RSI",
                signal=SignalType.BUY,
                value=rsi,
                description=f"RSI={rsi}，偏多信号"
            )
        else:
            return TechnicalSignal(
                indicator="RSI",
                signal=SignalType.SELL,
                value=rsi,
                description=f"RSI={rsi}，偏空信号"
            )

    @staticmethod
    def comprehensive_analysis(signals: List[TechnicalSignal]) -> Dict[str, any]:
        """
        综合分析多个技术信号

        Args:
            signals: 技术信号列表

        Returns:
            Dict[str, any]: 综合分析结果
        """
        buy_signals = sum(1 for s in signals if s.signal == SignalType.BUY)
        sell_signals = sum(1 for s in signals if s.signal == SignalType.SELL)
        total_signals = len(signals)

        buy_ratio = buy_signals / total_signals if total_signals > 0 else 0

        if buy_ratio >= 0.7:
            overall_signal = SignalType.BUY
            rating = "5星"
            recommendation = "强烈推荐"
        elif buy_ratio >= 0.5:
            overall_signal = SignalType.BUY
            rating = "4星"
            recommendation = "推荐买入"
        elif buy_ratio >= 0.3:
            overall_signal = SignalType.NEUTRAL
            rating = "3星"
            recommendation = "谨慎关注"
        else:
            overall_signal = SignalType.SELL
            rating = "2星"
            recommendation = "建议观望"

        return {
            "overall_signal": overall_signal,
            "rating": rating,
            "recommendation": recommendation,
            "buy_count": buy_signals,
            "sell_count": sell_signals,
            "total_count": total_signals,
            "buy_ratio": round(buy_ratio * 100, 1)
        }


# 使用示例
if __name__ == "__main__":
    # 示例价格数据
    prices = [10.0, 10.2, 10.5, 10.3, 10.6, 10.8, 11.0, 11.2, 11.1, 11.3]
    highs = [10.5, 10.7, 10.8, 10.6, 10.9, 11.1, 11.3, 11.5, 11.4, 11.6]
    lows = [9.8, 10.0, 10.2, 10.1, 10.3, 10.5, 10.8, 11.0, 10.9, 11.1]

    # 计算指标
    tech = TechnicalIndicators()
    macd = tech.calculate_macd(prices)
    kdj = tech.calculate_kdj(highs, lows, prices)
    rsi = tech.calculate_rsi(prices)

    print(f"MACD: {macd}")
    print(f"KDJ: {kdj}")
    print(f"RSI: {rsi}")

    # 分析信号
    signals = [
        tech.analyze_macd_signal(macd),
        tech.analyze_kdj_signal(kdj),
        tech.analyze_rsi_signal(rsi),
        tech.analyze_volume(1500000, 1000000)
    ]

    print("\n技术信号分析:")
    for signal in signals:
        print(f"{signal.indicator}: {signal.signal.value} - {signal.description}")

    # 综合分析
    comprehensive = tech.comprehensive_analysis(signals)
    print(f"\n综合评级: {comprehensive['rating']}")
    print(f"投资建议: {comprehensive['recommendation']}")
    print(f"买入信号占比: {comprehensive['buy_ratio']}%")
