"""
股票风险评估工具
评估股票投资风险，提供风险预警和应对建议
"""

from typing import List, Dict, Tuple
from dataclasses import dataclass
from enum import Enum


class RiskLevel(Enum):
    """风险等级"""
    LOW = "低风险"
    MEDIUM = "中等风险"
    HIGH = "高风险"
    EXTREME = "极高风险"


class RiskCategory(Enum):
    """风险类别"""
    MARKET = "市场风险"
    SECTOR = "行业风险"
    COMPANY = "公司风险"
    TECHNICAL = "技术风险"
    VALUATION = "估值风险"
    LIQUIDITY = "流动性风险"


@dataclass
class RiskFactor:
    """风险因素数据类"""
    category: RiskCategory
    level: RiskLevel
    description: str
    impact: str
    suggestion: str


class RiskAssessment:
    """风险评估类"""

    def __init__(self):
        """初始化风险评估器"""
        self.risk_factors = []

    def assess_market_risk(self, market_trend: str, volatility: float) -> RiskFactor:
        """
        评估市场风险

        Args:
            market_trend: 市场趋势 (上涨/下跌/震荡)
            volatility: 波动率

        Returns:
            RiskFactor: 市场风险因素
        """
        if market_trend == "下跌" and volatility > 0.03:
            return RiskFactor(
                category=RiskCategory.MARKET,
                level=RiskLevel.HIGH,
                description="市场处于下跌趋势，波动率较高",
                impact="可能导致个股普遍下跌",
                suggestion="建议降低仓位，等待市场企稳信号"
            )
        elif market_trend == "震荡":
            return RiskFactor(
                category=RiskCategory.MARKET,
                level=RiskLevel.MEDIUM,
                description="市场震荡，方向不明",
                impact="个股表现分化",
                suggestion="建议精选个股，控制仓位"
            )
        else:
            return RiskFactor(
                category=RiskCategory.MARKET,
                level=RiskLevel.LOW,
                description="市场趋势向好",
                impact="有利于个股表现",
                suggestion="可适当增加仓位"
            )

    def assess_sector_risk(self, sector_trend: str, policy_risk: bool) -> RiskFactor:
        """
        评估行业风险

        Args:
            sector_trend: 行业趋势 (利好/利空/中性)
            policy_risk: 是否存在政策风险

        Returns:
            RiskFactor: 行业风险因素
        """
        if sector_trend == "利空" or policy_risk:
            return RiskFactor(
                category=RiskCategory.SECTOR,
                level=RiskLevel.HIGH,
                description="行业面临利空因素或政策风险",
                impact="板块整体承压",
                suggestion="建议规避该板块，关注政策动向"
            )
        elif sector_trend == "利好":
            return RiskFactor(
                category=RiskCategory.SECTOR,
                level=RiskLevel.LOW,
                description="行业处于利好周期",
                impact="板块整体受益",
                suggestion="可重点关注板块龙头"
            )
        else:
            return RiskFactor(
                category=RiskCategory.SECTOR,
                level=RiskLevel.MEDIUM,
                description="行业平稳运行",
                impact="关注个股基本面",
                suggestion="精选优质个股"
            )

    def assess_company_risk(self, financial_health: str, news_risk: List[str]) -> RiskFactor:
        """
        评估公司风险

        Args:
            financial_health: 财务健康状况 (良好/一般/较差)
            news_risk: 负面新闻列表

        Returns:
            RiskFactor: 公司风险因素
        """
        if financial_health == "较差" or len(news_risk) > 2:
            return RiskFactor(
                category=RiskCategory.COMPANY,
                level=RiskLevel.HIGH,
                description=f"公司财务状况{financial_health}，存在{len(news_risk)}项负面因素",
                impact="可能影响股价表现",
                suggestion="建议谨慎投资，关注公司改善措施"
            )
        elif financial_health == "一般":
            return RiskFactor(
                category=RiskCategory.COMPANY,
                level=RiskLevel.MEDIUM,
                description="公司财务状况一般，存在改善空间",
                impact="业绩波动可能较大",
                suggestion="建议持续跟踪财务数据"
            )
        else:
            return RiskFactor(
                category=RiskCategory.COMPANY,
                level=RiskLevel.LOW,
                description="公司财务状况良好",
                impact="基本面支撑较强",
                suggestion="可重点关注"
            )

    def assess_technical_risk(self, price_position: str, volume_trend: str) -> RiskFactor:
        """
        评估技术风险

        Args:
            price_position: 价格位置 (高位/低位/中位)
            volume_trend: 成交量趋势 (放量/缩量/正常)

        Returns:
            RiskFactor: 技术风险因素
        """
        if price_position == "高位" and volume_trend == "缩量":
            return RiskFactor(
                category=RiskCategory.TECHNICAL,
                level=RiskLevel.HIGH,
                description="股价处于高位且缩量",
                impact="可能面临回调风险",
                suggestion="建议逐步减仓，设置止损"
            )
        elif price_position == "高位":
            return RiskFactor(
                category=RiskCategory.TECHNICAL,
                level=RiskLevel.MEDIUM,
                description="股价处于高位",
                impact="追高风险较大",
                suggestion="建议等待回调机会"
            )
        elif price_position == "低位" and volume_trend == "放量":
            return RiskFactor(
                category=RiskCategory.TECHNICAL,
                level=RiskLevel.LOW,
                description="股价处于低位且放量",
                impact="可能筑底反弹",
                suggestion="可适当布局"
            )
        else:
            return RiskFactor(
                category=RiskCategory.TECHNICAL,
                level=RiskLevel.MEDIUM,
                description="技术面中性",
                impact="趋势方向不明确",
                suggestion="建议观察确认"
            )

    def assess_valuation_risk(self, pe_ratio: float, pb_ratio: float, industry_avg_pe: float) -> RiskFactor:
        """
        评估估值风险

        Args:
            pe_ratio: 市盈率
            pb_ratio: 市净率
            industry_avg_pe: 行业平均市盈率

        Returns:
            RiskFactor: 估值风险因素
        """
        premium_ratio = pe_ratio / industry_avg_pe if industry_avg_pe > 0 else 1

        if premium_ratio > 2.0:
            return RiskFactor(
                category=RiskCategory.VALUATION,
                level=RiskLevel.HIGH,
                description=f"估值偏高，PE为行业均值的{premium_ratio:.1f}倍",
                impact="回调风险较大",
                suggestion="建议等待估值回归合理区间"
            )
        elif premium_ratio > 1.5:
            return RiskFactor(
                category=RiskCategory.VALUATION,
                level=RiskLevel.MEDIUM,
                description=f"估值略高，PE为行业均值的{premium_ratio:.1f}倍",
                impact="短期可能承压",
                suggestion="建议关注业绩增长是否匹配"
            )
        elif premium_ratio < 0.7:
            return RiskFactor(
                category=RiskCategory.VALUATION,
                level=RiskLevel.LOW,
                description=f"估值较低，PE为行业均值的{premium_ratio:.1f}倍",
                impact="安全边际较高",
                suggestion="可重点关注"
            )
        else:
            return RiskFactor(
                category=RiskCategory.VALUATION,
                level=RiskLevel.MEDIUM,
                description="估值合理",
                impact="风险收益平衡",
                suggestion="可适当配置"
            )

    def assess_liquidity_risk(self, avg_volume: float, market_cap: float) -> RiskFactor:
        """
        评估流动性风险

        Args:
            avg_volume: 平均成交量
            market_cap: 市值

        Returns:
            RiskFactor: 流动性风险因素
        """
        turnover_rate = avg_volume / market_cap if market_cap > 0 else 0

        if turnover_rate < 0.01:
            return RiskFactor(
                category=RiskCategory.LIQUIDITY,
                level=RiskLevel.HIGH,
                description="流动性较差，换手率低",
                impact="买卖困难，冲击成本高",
                suggestion="建议谨慎参与，控制仓位"
            )
        elif turnover_rate < 0.03:
            return RiskFactor(
                category=RiskCategory.LIQUIDITY,
                level=RiskLevel.MEDIUM,
                description="流动性一般",
                impact="大额交易可能影响价格",
                suggestion="建议分批交易"
            )
        else:
            return RiskFactor(
                category=RiskCategory.LIQUIDITY,
                level=RiskLevel.LOW,
                description="流动性良好",
                impact="交易便利",
                suggestion="正常交易即可"
            )

    def comprehensive_assessment(self, risk_factors: List[RiskFactor]) -> Dict[str, any]:
        """
        综合风险评估

        Args:
            risk_factors: 风险因素列表

        Returns:
            Dict[str, any]: 综合风险评估结果
        """
        if not risk_factors:
            return {
                "overall_level": RiskLevel.MEDIUM,
                "risk_score": 50,
                "warning": "无法评估"
            }

        # 风险评分
        risk_scores = {
            RiskLevel.LOW: 25,
            RiskLevel.MEDIUM: 50,
            RiskLevel.HIGH: 75,
            RiskLevel.EXTREME: 100
        }

        total_score = sum(risk_scores[factor.level] for factor in risk_factors)
        avg_score = total_score / len(risk_factors)

        # 确定整体风险等级
        if avg_score >= 75:
            overall_level = RiskLevel.HIGH
            warning = "[警告] 高风险预警：多项风险因素集中，建议谨慎或规避"
        elif avg_score >= 50:
            overall_level = RiskLevel.MEDIUM
            warning = "[注意] 中等风险：存在一定风险，建议控制仓位"
        else:
            overall_level = RiskLevel.LOW
            warning = "[正常] 低风险：风险可控，可适当参与"

        return {
            "overall_level": overall_level,
            "risk_score": round(avg_score, 1),
            "warning": warning,
            "risk_count": len(risk_factors),
            "high_risk_count": sum(1 for f in risk_factors if f.level == RiskLevel.HIGH),
            "medium_risk_count": sum(1 for f in risk_factors if f.level == RiskLevel.MEDIUM),
            "low_risk_count": sum(1 for f in risk_factors if f.level == RiskLevel.LOW)
        }

    def generate_risk_report(self, stock_name: str, risk_factors: List[RiskFactor]) -> str:
        """
        生成风险报告

        Args:
            stock_name: 股票名称
            risk_factors: 风险因素列表

        Returns:
            str: 格式化的风险报告
        """
        assessment = self.comprehensive_assessment(risk_factors)

        report = []
        report.append(f"## {stock_name} 风险评估报告\n")
        report.append(f"### 整体风险等级：{assessment['overall_level'].value}")
        report.append(f"### 风险评分：{assessment['risk_score']}/100")
        report.append(f"### 风险预警：{assessment['warning']}\n")

        report.append("### 风险因素详情\n")

        for factor in risk_factors:
            report.append(f"#### {factor.category.value} - {factor.level.value}")
            report.append(f"- **描述**：{factor.description}")
            report.append(f"- **影响**：{factor.impact}")
            report.append(f"- **建议**：{factor.suggestion}\n")

        report.append("### 风险统计")
        report.append(f"- 高风险因素：{assessment['high_risk_count']}项")
        report.append(f"- 中等风险因素：{assessment['medium_risk_count']}项")
        report.append(f"- 低风险因素：{assessment['low_risk_count']}项")

        return "\n".join(report)


# 使用示例
if __name__ == "__main__":
    # 创建风险评估实例
    assessor = RiskAssessment()

    # 评估各项风险
    risk_factors = [
        assessor.assess_market_risk("震荡", 0.025),
        assessor.assess_sector_risk("中性", False),
        assessor.assess_company_risk("良好", []),
        assessor.assess_technical_risk("中位", "放量"),
        assessor.assess_valuation_risk(15.0, 2.5, 20.0),
        assessor.assess_liquidity_risk(50000000, 10000000000)
    ]

    # 生成风险报告
    report = assessor.generate_risk_report("示例股票", risk_factors)
    print(report)

    # 综合评估
    assessment = assessor.comprehensive_assessment(risk_factors)
    print(f"\n综合评估：{assessment}")
