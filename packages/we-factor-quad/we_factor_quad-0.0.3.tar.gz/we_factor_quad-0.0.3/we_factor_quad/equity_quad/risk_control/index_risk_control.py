# 核心考察的，是使用指定的因子组，来对指定对象(指定的指数)进行风险控制，考察的内容是3个点
# 1. 能不能总体上控得住，
# 2. 能不能一直控得住，
# 3. 控制下的偏离不能太远
import numpy as np
import pandas as pd
from we_report.data_type import report_data
import matplotlib.pyplot as plt
from copy import deepcopy
from we_factor_quad.equity_quad.factor_quad_equity import FactorQuadEQ
from typing import Union, List, Dict
from we_factor_quad.test_settings import StocksOutputReport
from we_factor_quad.test_settings import settings
import we_factor_quad.data_api as data_api
from we_factor_quad.equity_quad.risk_control.stock_risk_control import RiskDecomposition


class CompareReportsPortfolio:
    """
    基于 portfolio 的风险控制报告的生成，继续参照 CompareReports 的报告控制方法
    """

    def __init__(self, decomp_names: List[str], risk_decomp: List[RiskDecomposition]):
        self.decomp_names = decomp_names
        self.risk_decomp = risk_decomp
        assert len(self.decomp_names) == len(self.risk_decomp), "输入的分解模型 vs 模型名称 长度不一致"

    def get_reports(self, report_contents: Union[str, List] = "full", output_file: str = 'stock_risk_report.xlsx'):
        """
        生成报告
        :param report_contents:
        :param output_file:
        :return:
        """


# ---------------
# 测试样例


def test_risk_decomposition_index():
    start_dt = '20100101'
    end_dt = '20221201'
    index_ticker_list = ['000300.SH', '399997.CSI']
    weight_file = None  # 需要外部输入index 权重的文件
    target_vol = 0.1  # 期望的波动率
    local_path = settings.seadrive_local_path
    model_list = StocksOutputReport.compare_model  # 目前的数值为 ['we', 'barra']

    code_map = {
        # 同花顺内部代码 -> 常见形式代码
        # 'I07706': '399997.SZ',
        'ind422': '000300.SH',
        'ind427': '000905.SH',
        'ind377': '000016.SH',
        'I06011': '000852.SH'
    }

    def test_get_index_report(model_list: List):
        risk_decomp_list = []
        for model in model_list:
            myquad = FactorQuadEQ.create_factor_quad(factor_system=eval(f'StocksOutputReport.{model}_factor_case_name'),
                                                     start_date=StocksOutputReport.start,
                                                     end_date=StocksOutputReport.end,
                                                     from_src=StocksOutputReport.from_local,
                                                     local_path=local_path)
            myquad.capped_psi_adjustment()  # todo 确定是要计算 capped_psi() 的吧
            mydecomp = RiskDecomposition(factor_quad=myquad)  # 在这里就应该指定和选择了
            risk_decomp_list.append(mydecomp)

        # 提取portfolio 中的stock的价格与权重
        # portfolio_data load
        portfolio_data = None  # 从 data_api 中导入所有的数据，未必是这个名字

        # 生成报告
        # myreport = CompareReportsPortfolio(decomp_names=model_list, risk_decomp=risk_decomp_list,
        #                                    portfolio_data=portfolio_data)

    test_get_index_report(model_list)


if __name__ == '__main__':
    test_risk_decomposition_index()
