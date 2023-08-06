from typing import Dict, List
import datetime as datetime
import pandas as pd
import numpy as np
import wiserdata as wedata
import we_dms.wiser_data_api.return_api as return_api
import we_dms.wiser_data_api.basic_info_api as basic_info_api
import we_dms.wiser_data_api.wedata_api as wedata_api
from we_factor_quad.equity_quad.factor_portfolio.universe_helper import fill_notupdated_constituents

def wiser_download_em_result(case_name: str,
                             which: str,
                             start_date: str,
                             end_date: str,
                             universe: List = [],
                             mode="local",
                             seadrive_localpath: str = None) -> pd.DataFrame:
    """
    加载四元组数据，可以从本地也可以远程
    :param case_name: 数据库中的数据存储是按照case 来开平行世界的数据库的；在seadrive中对应一个文件夹
    :param which:  ['characteristic_scale', 'characteristic_covariance',
            'characteristic_idiosyncratic_volatility', 'characteristic_exposure'] 中之一
    :param start_date: 开始日期
    :param end_date: 结束日期
    :param universe: 代码对象空间
    :param mode: if "local", then use sea_drive, if not, try to load from wiserdata api remotely,默认使用sea_drive
    :return:
    """
    param = {
        'domain': 'descriptor',
        'phylum': 'characteristic',
        'class': f'{which}',  # 只能一个个来
        'fields': [],
        'user': '',
        'case': f'{case_name}',
        'start_date': start_date,
        'end_date': end_date,
        'codes': universe,
    }

    ntries = 10
    if mode.lower() == 'local':  # 本地模式

        from pathlib import Path
        assert seadrive_localpath is not None, "missing value for seadrive_localpath!"  # 如果是local模式，则必须要非None
        print("check ", seadrive_localpath, case_name)
        loader = wedata.LocalClient(Path(seadrive_localpath, 'case_' + case_name))
        # loader = wedata.LocalClient(LOCAL_PATH+'case_'+case_name)
        print(f'准备下载 {which}...')
        while True:
            try:
                df_ = loader.query(param)
                break
            except Exception as exx:
                print('异常：', repr(exx))
                import pdb
                pdb.set_trace()
    else:  # login as admin # to be deprecated
        while True:
            # 下载时总遇到 Exception
            try:
                df_ = wiser_data_query_split(param, years_split=1)
                break
            except Exception as exx:
                ntries -= 1
                if ntries < 0:
                    raise ValueError("Tries many times! Error")
                print('异常：', repr(exx))
    return df_


def wiser_data_query_split(param: Dict, years_split: int = 1):
    """
    :param param:
    :param years_split:
    :return:
    """
    # wedata 数据下载有限制，本方法为分时间段（years_split年）下载数据

    if (datetime.datetime.strptime(param['end_date'], '%Y%m%d') - datetime.datetime.strptime(
            param['start_date'], '%Y%m%d')).days <= years_split * 365:
        tmp_res = wedata.query(param)
    else:
        _param = param.copy()
        tmp_res = pd.DataFrame({})

        # 初始值
        _start_date = param['start_date']
        _end_date = (
                datetime.datetime.strptime(_start_date, '%Y%m%d') +
                datetime.timedelta(days=years_split * 365)).strftime('%Y%m%d')

        while _start_date < param['end_date']:
            _param.update({'start_date': _start_date})
            _param.update({'end_date': _end_date})
            wedata.login('admin',
                         'admin')  # TODO 后续所有的链接登录的账号和密码，应进行配置化， login - if previous query takes too long, login may expire
            print(_param)  # print parameter in case the query fail and we need to provide info to wiserdata support
            _tmp_data = wedata.query(_param)
            tmp_res = pd.concat([tmp_res, _tmp_data], axis=0)
            _start_date = _end_date
            _end_date = (datetime.datetime.strptime(_start_date, '%Y%m%d') + datetime.timedelta(
                days=years_split * 365)).strftime('%Y%m%d')
            if _end_date >= param['end_date']:
                _end_date = param['end_date']

    return tmp_res


def load_universe(universe_identifier: tuple[str],
                  start_date: str,
                  end_date: str,
                  rename_mapping=None) -> (pd.DataFrame, pd.DataFrame):
    """
    加载指定指数中的所有成分股
    Args:
        rename_mapping:
        universe_identifier: 数据库中的指数代码，比如ind422是沪深300， I00275中证500， I06011中证1000
        start_date:
        end_date:
    Returns: 一个wide panel dataframe，里面是所有universe下股票的monthly return
    """
    # 数据库中的日期直接用“20100101”这种字符串判断又是会判错边界，改成下面这种形式最保险
    temp_start = pd.to_datetime(start_date, format='%Y%m%d').strftime('%Y-%m-%d %H:%M:%S')
    temp_end = pd.to_datetime(end_date, format='%Y%m%d').strftime('%Y-%m-%d %H:%M:%S')

    A_SHARE_CODE_MAP = basic_info_api.basic_sec_info().set_index('SEC_ID')['SEC_CODE'].to_dict()
    # A_SHARE_CODE_MAP缺了这俩股票，补充一下
    A_SHARE_CODE_MAP.update({'SSH601607': '601607', 'SSH600849': '600849'})

    if end_date == '':
        range_filter = [f">= '{temp_start}'"]
    else:
        range_filter = [f">= '{temp_start}'", f" <= '{temp_end}'"]

    if isinstance(universe_identifier, str):
        universe_identifier = [universe_identifier]
    universe_identifier = "','".join(universe_identifier)
    param = {
        'domain': 'sheet',
        'phylum': 'ths',
        'class': 'index_weight',
        'fields': ['TD_DATE', 'INDEX_ID', 'CONSTITUENT_SEC_ID'],
        'start_date': '',
        'end_date': '',
        'codes': [],
        'form': 'normal',
        'filters': {
            'TD_DATE': range_filter,
            'INDEX_ID': [f"in ('{universe_identifier}')"]
        },
    }
    wedata.login('admin', 'admin')
    all_constituents = wedata.query(param).drop_duplicates(subset=['TD_DATE', 'CONSTITUENT_SEC_ID'])
    all_constituents = all_constituents.sort_values(by=["TD_DATE", "INDEX_ID", "CONSTITUENT_SEC_ID"]).reset_index(drop=True)
    all_constituents.rename(columns={"TD_DATE": 'date', "CONSTITUENT_SEC_ID": 'code'}, inplace=True)
    all_constituents['code'] = all_constituents['code'].map(A_SHARE_CODE_MAP)
    all_constituents['date'] = pd.to_datetime(all_constituents['date'])
    padded_constituents = fill_notupdated_constituents(all_constituents=all_constituents)
    pivoted_constituents = padded_constituents.pivot(index='date', columns='code', values="INDEX_ID")
    pivoted_constituents = ~pd.isnull(pivoted_constituents)
    pivoted_constituents = pivoted_constituents.asfreq('BM', method='pad')
    if rename_mapping:
        return pivoted_constituents.rename(columns=rename_mapping)
    else:
        return pivoted_constituents





def wiser_fetch_fmp_weights(seadrive_localpath: str,
                            start_date: str,
                            end_date: str,
                            factor_system: str = 'HF25_SRAM'):
    """

    Args:
        start_date:
        end_date:
        factor_system:
        seadrive_localpath: 本地seadrive的群组资料库地址

    Returns:
    """
    data_file_dir = f"{seadrive_localpath}\case_{factor_system}"
    client = wedata.LocalClient(data_file_dir)
    wedata.login(username='admin', password='admin')
    param = {
        'domain': 'descriptor',
        'phylum': 'characteristic',
        'class': 'factor_mimicking_portfolio_weights',
        'case': factor_system,
        'start_date': start_date,
        'end_date': end_date,
    }
    # 调用query函数
    weights_df = client.query(param)[['date', "factors", "code", "weight"]]
    pivoted_weights = weights_df.pivot(index=['date', 'factors'], columns='code',
                                       values='weight').reset_index().fillna(0.0)
    pivoted_weights['date'] = pd.to_datetime(pivoted_weights['date'])

    return pivoted_weights


def wiser_fetch_factor_return(seadrive_localpath: str,
                              start_date: str,
                              end_date: str,
                              factor_system: str = 'HF25_SRAM'):
    """

    Args:
        seadrive_localpath:
        start_date:
        end_date:
        factor_system:

    Returns:

    """
    data_file_dir = f"{seadrive_localpath}\case_{factor_system}"
    client = wedata.LocalClient(data_file_dir)
    wedata.login(username='admin', password='admin')
    param = {
        'domain': 'descriptor',
        'phylum': 'characteristic',
        'class': 'factor_return',
        'case': factor_system,
        'start_date': start_date,
        'end_date': end_date,
    }
    factor_return = client.query(param)[['date', 'factors', 'factor_returns']]
    factor_return['date'] = pd.to_datetime(factor_return['date'])
    factor_return = factor_return.pivot(index='date', columns='factors', values='factor_returns')
    # factor_return是预测值，延后一月
    if factor_return.index.min().month == pd.to_datetime(start_date).month:
        factor_return = factor_return.iloc[1:, :]
    return factor_return

def wiser_query_dwd_data(dwd_list, start, end, pile=False, rename=False, sample_stk=None, split_download=True,
                         years_split=3):
    """
    Grab dwd data from wedata
    :param dwd_list: a list of dwd table name
    :param sample_stk: a list of stock code ,usually use representative old stocks
    :return: a dataframe of query data, index=time, columns=stock id, values= queried data
    """
    TIME_COL_NAME = 'TRADE_DT'
    CODE_COL_NAME = 'CODE_ID'

    def convert_date_wedata(dt):
        res = pd.to_datetime(dt)
        if res is None:
            return ""
        else:
            return res.strftime("%Y%m%d")

    import wiserdata as wedata
    res = {}
    if sample_stk is not None:
        col_sample_stk = ['TRADE_DT'] + [''.join(i.split('.')) for i in sample_stk]
    else:
        col_sample_stk = []

    wedata.login('admin', 'admin')
    # 循环读取wedata原始数据
    for tab in dwd_list[:]:
        param = {
            'domain': 'sheet',
            'phylum': 'direct',
            'class': tab.replace('dwd_', ''),
            'fields': col_sample_stk,
            'start_date': convert_date_wedata(start),
            'end_date': convert_date_wedata(end),
            'codes': []
        }
        print('param', tab, param)
        # wedata 数据下载有限制，本方法为分时间段（years_split年）下载数据
        if not split_download or (
                (datetime.datetime.strptime(param['end_date'], '%Y%m%d') - datetime.datetime.strptime(
                    param['start_date'], '%Y%m%d')).days <= years_split * 365):
            tmp_res = wedata.extract(param)
        else:
            _param = param.copy()
            tmp_res = pd.DataFrame({})

            # 初始值
            _start_date = param['start_date']
            _end_date = (
                    datetime.datetime.strptime(_start_date, '%Y%m%d') + datetime.timedelta(
                days=years_split * 365)).strftime(
                '%Y%m%d')

            while _start_date < param['end_date']:
                print(f'downloading {_start_date}-{_end_date}')
                _param.update({'start_date': _start_date})
                _param.update({'end_date': _end_date})
                _tmp_data = wedata.extract(param)
                tmp_res = pd.concat([tmp_res, _tmp_data], axis=0)
                _start_date = _end_date
                _end_date = (datetime.datetime.strptime(_start_date, '%Y%m%d') + datetime.timedelta(
                    days=years_split * 365)).strftime('%Y%m%d')
                if _end_date >= param['end_date']:
                    _end_date = param['end_date']
        tmp_res.drop_duplicates(inplace=True)
        data = tmp_res
        if len(data) == 0:
            print(f'dwd data {tab} can`t show ')
            continue
        # df = pd.concat([i for i in data.values()]).sort_values('TRADE_DT').set_index('TRADE_DT')
        df = data.sort_values('TRADE_DT').set_index('TRADE_DT')
        df.index = pd.to_datetime(df.index.astype('str'))
        if 'OPDATE' in df.columns:
            del df['OPDATE']
        df.columns = [i[:6] + '.' + i[6:] for i in df.columns]
        if pile:
            df = df.stack().reset_index()
            if rename:
                df.columns = [TIME_COL_NAME, CODE_COL_NAME, tab.replace('dwd_', '')]
            df[tab.replace('dwd_', '')] = df[tab.replace('dwd_', '')].astype('float')
        res[tab] = df
        print(f' dwd data {tab} loaded!')
    return res

# todo yanan :delete get_px_close_old after wedms instead
def get_px_close_old(start, end):
    px_close = wiser_query_dwd_data(['ths__we_sec_daily_quote_adjust_factor__s_dq_adjclose__forward'],
                                         start=start, end=end, rename=True, pile=True,
                                         )['ths__we_sec_daily_quote_adjust_factor__s_dq_adjclose__forward']
    px_close = px_close.pivot(index='TRADE_DT', columns='CODE_ID',
                                        values='ths__we_sec_daily_quote_adjust_factor__s_dq_adjclose__forward')
    return px_close

def get_px_close(start, end):
    px_close =  wedata_api.query_dwd_data(['ths__we_sec_daily_quote_adjust_factor__s_dq_adjclose__forward'],
                                         start=start, end=end, rename=True, pile=True,
                                         )['ths__we_sec_daily_quote_adjust_factor__s_dq_adjclose__forward']
    px_close = px_close.pivot(index='TRADE_DT', columns='CODE_ID',
                                        values='ths__we_sec_daily_quote_adjust_factor__s_dq_adjclose__forward')
    return px_close

def wiser_get_monthly_return(start: str,
                             end: str,
                             seadrive_localpath,
                             sample_stk=[]):
    '''
    use return api get monthly return data and  close
    Args:
        sample_stk:
        from_seadrive:
        start: start_date 格式为"xxxxxxxx"纯数字字符串！
        end: end_date 格式为"xxxxxxxx"纯数字字符串！

    Returns: monthly_ret adn close price

    '''
    client = wedata.LocalClient(f"{seadrive_localpath}/case_BasicData")
    wedata.login(username='admin', password='admin')
    param = {
        'domain': 'descriptor',
        'phylum': 'characteristic',
        'case': 'BasicData',
        'class': 'daily_excess_return',
        'start_date': start,
        'end_date': end,
    }
    if len(sample_stk) > 0:
        code_filter = {'code': [f"in {tuple(sample_stk)}"]}
        param.update({'filters': {}})
        param['filters'].update(code_filter)

    daily_returns = client.query(param)[['date', 'code', "daily_return"]]
    monthly_ret = produce_monthly_return_from_daily(start=start,
                                                    end=end,
                                                    daily_returns=daily_returns)
    return monthly_ret


def produce_monthly_return_from_daily(start,
                                      end,
                                      daily_returns: pd.DataFrame) -> pd.DataFrame:

    pivoted_daily_returns = (daily_returns.pivot(index='date', columns='code', values='daily_return')).replace(np.nan, 0.0)
    pivoted_daily_returns.index = pd.to_datetime(list(pivoted_daily_returns.index))
    pivoted_daily_returns.index = pivoted_daily_returns.index.to_period("M")
    monthly_return = pivoted_daily_returns.groupby(level=0).apply(lambda x: x.cumsum(skipna=True).iloc[-1, :]).replace(0.0, np.nan)
    monthly_return = monthly_return.to_timestamp('M')
    monthly_return.index = pd.date_range(start=start, end=end, freq='BM')
    monthly_return.iloc[0, :] = np.nan
    return monthly_return

def test_local_mode():
    seadrive_local_path = 'D:/seadrive_files/xiazeyu/Shared with groups/'
    res = wiser_download_em_result(case_name='HF25_SRA', start_date='20200101',
                                   which='characteristic_exposure',
                                   end_date='20200401', mode='local',
                                   seadrive_localpath=seadrive_local_path)
    return res


if __name__ == '__main__':
    start_date = "20200101"
    end_date = "20221031"
    wedata.login('admin', 'admin')
    # test_local_mode()
    get_px_close(start_date, end_date)
    # monthly_return1 = wiser_get_monthly_return(start=start_date, end=end_date, seadrive_localpath='D:\seadrive_cache_folder\zhouly\群组资料库')
    print(1)
