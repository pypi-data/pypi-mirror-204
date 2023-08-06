class settings:
    # 这部分参数，用于生成报告
    # 报告统计时间区间
    report_start_date = '20201101'
    report_end_date = '20221031'
    # 四元组数据来源，local是读本地pkl文件，remote为从wiserdata下载数据
    quad_from_local = 1
    # seadrive_local_path = r'D:\seadrive_cache_folder\zhouly\群组资料库'
    # seadrive_local_path = r"D:\zhouly\群组资料库"
    seadrive_local_path = r'C:\Users\Administrator\seadrive_root\yangyn\群组资料库'
    # seadrive_local_path = r'D:/seadrive_files/xiazeyu/Shared with groups/'
    # we因子模型与要对比的barra模型 case名
    we_factor_case_name = 'HF25_SRAM'
    barra_factor_case_name = '202211_PRE_BARRA'
    # we模型与barra模型风格因子名
    we_factors_name = ['beta', 'ceg', 'dtop', 'etop', 'gpm', 'log_bp', 'log_markcap', 'log_st_mean', 'log_std', 'mbs',
                       'reversal_short', 'roe', 'rstr', 'tagr']
    barra_factors_name = ['Beta', 'Book-to-Price', 'Dividend Yield', 'Earnings Quality', 'Earnings Variability',
                          'Earnings Yield', 'Growth', 'Investment Quality', 'Leverage', 'Liquidity',
                          'Long-Term Reversal',
                          'Mid Capitalization',
                          'Momentum', 'Profitability', 'Residual Volatility', 'Size']
    # 个股分析代码及股票名称
    report_stock_codes = ['300750.SZ', '000002.SZ', '601398.SH', '002069.SZ', '600196.SH', '002460.SZ', '600519.SH',
                          '600518.SH']
    report_stock_names = ['宁德时代', '万科', '工商银行', '獐子岛', '复星医药', '赣锋锂业', '茅台', '康美药业', '乐视']
    index_weight_file = ['', 'Baijiu_w.csv']
    index_ticker_list = ['000300.SH', '399997.CSI']
    index_truncate_before = ['2010-1', '2015-1']

    # Factor Summary report
    factor_summary_start_date = '20200101'
    factor_summary_end_date = '20221231'
    factor_model = 'model_202209'
    factor_group = 'volatility'

    factor_group_start_date = '20200101'
    factor_group_end_date = '20221231'

    compare_model = ['we', 'barra']

class StocksOutputReport:
    start = settings.report_start_date
    end = settings.report_end_date
    from_local = settings.quad_from_local
    we_factor_case_name = settings.we_factor_case_name
    barra_factor_case_name = settings.barra_factor_case_name
    we_factors_name = settings.we_factors_name
    barra_factors_name = settings.barra_factors_name
    report_stock_codes = list(settings.report_stock_codes)
    report_stock_names = list(settings.report_stock_names)
    compare_model = settings.compare_model

class IndexOutputReport:
    ticker_list = settings.index_ticker_list
    truncate_before = settings.index_truncate_before
    weight_file = settings.index_weight_file



class IndexOutputReport:
    ticker_list = settings.index_ticker_list
    truncate_before = settings.index_truncate_before
    weight_file = settings.index_weight_file


class FmpUniverseConfig:
    """
    设定所有可用的universe，由多个指数叠加
    """
    universe_config = {'default_universe': ("ind422", "I06011", "I00275"),  # 沪深三百，中证500 + 中证 1000
                       'alternative_universe': ("ind422",)
                       }

