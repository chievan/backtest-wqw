import numpy as np
import scipy.io as sio
from option_backtester.base import *


def pbeta(mRp, mRb):
    """
    计算各组合维度alpha值

    参数
    --------
    mRp: m*n ndarray 组合收益率序列
    mRb：m*n ndarray 市场基准收益率序列

    返回值
    --------
    m*1 ndarray beta值
    """
    mRp = checkarray(mRp)
    mRb = checkarray(mRb)
    m = row_count(mRp)
    if row_count(mRb) != m:
        mRb = repmat(mRb, m, 0)
    temp = np.ones((m, 2))
    for i in range(m):
        temp[i, :] = np.polyfit(mRb[i, :], mRp[i, :], 1)
    return temp[:, 0:1]


def psharpe(mRp, mRf):
    '''
    参数：
    mRp: the portfolio return [m * n]
    mRf: the risk-free rate [1×n] or [m×n]
    返回值：
    y: the sharpe ratio[m×1]
    '''
    mRp = checkarray(mRp)
    mRf = checkarray(mRf)
    m = row_count(mRp)
    if row_count(mRf) != m:
        mRf = repmat(mRf, m, 0)
    y = np.zeros((m, 1))
    std_Rp = np.std(mRp, axis=1, ddof=1, keepdims=True)
    i = np.where(std_Rp == 0)[0]
    y[i] = np.nan
    i = np.where(std_Rp != 0)[0]
    if not isempty(i):
        y[i] = (np.mean(mRp[i, :]-mRf[i, :], 1, keepdims=True))/std_Rp[i]
    return y


# if __name__ == "__main__":
#     mRp = sio.loadmat(r"D:\FAIS2\Sources\PM\pyfinmdl\matfiles\sharpe")["mRp"]
#     mRf = sio.loadmat(r"D:\FAIS2\Sources\PM\pyfinmdl\matfiles\sharpe")["mRf"]
#     y = psharpe(mRp, mRf)
#     print(y)
#     print(y.shape)
#     print(type(y))


def ptreynor(mRp, mRb, mRf):
    '''
    计算treynor比例
    :param mRp: m * n
    :param mRb: m * n
    :param mRf: m * n
    :return: y: m * 1
    '''
    mRp = checkarray(mRp)
    mRf = checkarray(mRf)
    mRb = checkarray(mRb)
    m = row_count(mRp)
    if row_count(mRb) != m:
        mRb = repmat(mRb, m, 0)
    if row_count(mRf) != m:
        mRf = repmat(mRf, m, 0)
    y = (np.mean(mRp, 1, keepdims=True) - np.mean(mRf, 1, keepdims=True)) / pbeta(mRp, mRb)
    return y


# if __name__ == "__main__":
#     mRp = sio.loadmat(r"D:\FAIS2\Sources\PM\pyfinmdl\matfiles\treynor")["mRp"]
#     mRf = sio.loadmat(r"D:\FAIS2\Sources\PM\pyfinmdl\matfiles\treynor")["mRf"]
#     mRb = sio.loadmat(r"D:\FAIS2\Sources\PM\pyfinmdl\matfiles\treynor")["mRb"]
#     y = ptreynor(mRp, mRb, mRf)
#     # y = palpha(mRp, mRb)
#     print(y)
#     print(y.shape)
#     print(type(y))
#     print(y.ndim)


def pjensen(mRp, mRb, mRf):
    '''
    计算jensen比例
    :param mRp: m * n
    :param mRb: m * n
    :param mRf: m * n
    :return: y: m * 1
    '''
    mRp = checkarray(mRp)
    mRf = checkarray(mRf)
    mRb = checkarray(mRb)
    m = row_count(mRp)
    if row_count(mRb) != m:
        mRb = repmat(mRb, m, 0)
    if row_count(mRf) != m:
        mRf = repmat(mRf, m, 0)
    y = np.mean(mRp, 1, keepdims=True) - (np.mean(mRf, 1, keepdims=True) + (np.mean(mRb, 1, keepdims=True) - np.mean(mRf, 1, keepdims=True)) * pbeta(mRp, mRb))
    return y

# if __name__ == "__main__":
#     mRp = sio.loadmat(r"D:\FAIS2\Sources\PM\pyfinmdl\matfiles\treynor")["mRp"]
#     mRf = sio.loadmat(r"D:\FAIS2\Sources\PM\pyfinmdl\matfiles\treynor")["mRf"]
#     mRb = sio.loadmat(r"D:\FAIS2\Sources\PM\pyfinmdl\matfiles\treynor")["mRb"]
#     y = pjensen(mRp, mRb, mRf)
#     print(y)
#     print(y.shape)
#     print(type(y))
#     print(y.ndim)


def psortinomar(mRp):
    '''
    中信证券个性化指标需求
    :param mRp: m * n
    :return: y：m * 1
    '''
    mRp = checkarray(mRp)
    semiStd = psemistd(mRp, 0)
    m = row_count(mRp)
    y = np.zeros((m, 1))
    i = np.where(semiStd == 0)[0]
    if not isempty(i):
        y[i] = 0
    i = np.where(semiStd != 0)[0]
    if not isempty(i):
        y[i] = (np.mean(mRp[i, :], 1, keepdims=True) - np.min(mRp[i, :], 1, keepdims=True)) / semiStd[i, :]
    return y


# if __name__ == "__main__":
#     mRp = sio.loadmat(r"D:\FAIS2\Sources\PM\pyfinmdl\matfiles\treynor")["mRp"]
#     y = psortinomar(mRp)
#     print(y)
#     print(y.shape)
#     print(type(y))
#     print(y.ndim)


def praroc(mRp, mRb, dCon, iDay, iT = 1):
    '''
    中间函数NormalVaR增加了参数控制绝对、相对，Raroc默认用相对VaR
    :param mRp: m * n
    :param mRb: m * n 或者 1 * n
    :param dCon: 置信度 1*1
    :param iDay: 预测天数 1*1
    :return: y: raroc比例
    '''
    mRp = checkarray(mRp)
    mRb = checkarray(mRb)
    dCon = checkarray(dCon)
    iDay = checkarray(iDay)
    iT = checkarray(iT)
    m = row_count(mRp)
    if row_count(mRb) != m:
        mRb = repmat(mRb, m, 0)
    y = (np.mean(mRp, 1, keepdims=True) - np.mean(mRb, 1, keepdims=True)) / abs(pnormalvar.pnormalvar(mRp, dCon, iDay, iT))
    return y


# if __name__ == "__main__":
#     mRp = sio.loadmat(r"D:\FAIS2\Sources\PM\pyfinmdl\matfiles\treynor")["mRp"]
#     mRb = sio.loadmat(r"D:\FAIS2\Sources\PM\pyfinmdl\matfiles\treynor")["mRb"]
#     dCon = 0.95
#     iDay = 2
#     y = praroc(mRp, mRb, dCon, iDay)
#     print(y)
#     print(y.shape)
#     print(type(y))
#     print(y.ndim)


def downcaptreturn(CR, CRbm, iPara):
    '''
    计算下行捕获收益率
    :param CR: 产品收益率[M×N]，M为产品个数，N为每个产品的收益率数据个数
    :param CRbm: HS300相对应时间的基准收益率[1×N]或[M×N]，N为每个产品的收益率数据个数
    :param iPara: iPara = 0表示用算术法，iPara = 1表示用几何法
    :return: DownpCaptReturn，[M×1]M
    '''
    CR = checkarray(CR)
    CRbm = checkarray(CRbm)
    iPara = checkarray(iPara)
    M = row_count(CR)
    DownCaptReturn = np.zeros((M, 1))
    if row_count(CRbm) == 1:
        CRbm = np.ones((M, 1)) * CRbm
    for i in range(M):
        temp = np.where(CRbm[i, :] < 0)[0]
        temp = checkarray(temp)
        if not isempty(temp):
            ind = col_count(temp)
            upCR = CR[i, temp]
            if iPara == 0:
                DownCaptReturn[i, 0] = np.sum(upCR, 1, keepdims=True) / ind
            else:
                DownCaptReturn[i, 0] = (np.prod(1 + upCR)) ** (1 / ind) - 1
    return DownCaptReturn


# if __name__ == "__main__":
#     CR = sio.loadmat(r"D:\FAIS2\Sources\PM\pyfinmdl\matfiles\downreturn")["CR"]
#     CRbm = sio.loadmat(r"D:\FAIS2\Sources\PM\pyfinmdl\matfiles\downreturn")["CRbm"]
#     iPara = sio.loadmat(r"D:\FAIS2\Sources\PM\pyfinmdl\matfiles\downreturn")["iPara"]
#     y = downcaptreturn(CR, CRbm, iPara)
#     print(y)
#     print(y.shape)
#     print(type(y))
#     print(y.ndim)


def upcaptreturn(CR, CRbm, iPara):
    '''
    计算上行捕获收益率
    :param CR: 产品收益率[M×N]，M为产品个数，N为每个产品的收益率数据个数
    :param CRbm: HS300相对应时间的基准收益率[1×N]或[M×N]，N为每个产品的收益率数据个数
    :param iPara: iPara = 0表示用算术法，iPara = 1表示用几何法
    :return: DownpCaptReturn，[M×1]M
    '''
    CR = checkarray(CR)
    CRbm = checkarray(CRbm)
    iPara = checkarray(iPara)
    M = row_count(CR)
    UpCaptReturn = np.zeros((M, 1))
    if row_count(CRbm) == 1:
        CRbm = np.ones((M, 1)) * CRbm
    for i in range(M):
        temp = np.where(CRbm[i, :] > 0)[0]
        temp = checkarray(temp)
        if not isempty(temp):
            ind = col_count(temp)
            upCR = CR[i, temp]
            if iPara == 0:
                UpCaptReturn[i, 0] = np.sum(upCR, 1, keepdims=True) / ind
            else:
                UpCaptReturn[i, 0] = (np.prod(1 + upCR)) ** (1 / ind) - 1
    return UpCaptReturn


# if __name__ == "__main__":
#     CR = sio.loadmat(r"D:\FAIS2\Sources\PM\pyfinmdl\matfiles\downreturn")["CR"]
#     CRbm = sio.loadmat(r"D:\FAIS2\Sources\PM\pyfinmdl\matfiles\downreturn")["CRbm"]
#     iPara = sio.loadmat(r"D:\FAIS2\Sources\PM\pyfinmdl\matfiles\downreturn")["iPara"]
#     y = upcaptreturn(CR, CRbm, iPara)
#     print(y)
#     print(y.shape)
#     print(type(y))
#     print(y.ndim)


def calmarratio(mYield, yearReturn):
    '''
    计算calmar比例
    :param mYield: 组合收益率序列,[m*n],m个维度或组合,n个样本
    :param yearReturn: 组合年化收益率,[m*1]
    :return: y：calmar比率,[m*1]
    '''
    mYield = checkarray(mYield)
    yearReturn = checkarray(yearReturn)
#     计算区间的最大回撤
    maxdrawdown = max_drawdown.vmaxdrawdowninner_multi1(mYield)
    y = yearReturn / np.abs(maxdrawdown)
    return y


# if __name__ == '__main__':
#     mYield = sio.loadmat(r'D:\FAIS2\Sources\PM\pyfinmdl\matfiles\calmar')['mYield']
#     yearReturn = sio.loadmat(r'D:\FAIS2\Sources\PM\pyfinmdl\matfiles\calmar')['yearReturn']
#     y = calmarratio(mYield, yearReturn)
#     print(y)
#     print(y.shape)
#     print(type(y))
#     print(y.ndim)


def psterling(mRp, mRf):
    '''
    Sterling 指标：是度量投资组合的风险调整下资产回报的测度
    :param mRp: 组合历史收益率向量 [m*n] m代表资产种类 n代表取样天数
    :param mRf: 无风险收益率向量 [m*n]或[1*n]
    :return: y ： Sterling指标 [m*1]
    '''
    m = row_count(mRp)
    n = col_count(mRp)
    y =np.zeros((m, 1))
    NetAsset = np.zeros((m, n))
    MaximumD_mRp = max_drawdown.vmaxdrawdowninner_multi1(mRp)
    if row_count(mRf) != m:
        mRf = repmat(mRf, m, 0)
    y[MaximumD_mRp == 0] = np.nan
    i = np.where(MaximumD_mRp != 0)[0]
    if not isempty(i):
        y[i] = (np.mean(mRp[i, :] - mRf[i, :], 1, keepdims=True)) / MaximumD_mRp[i]
    return y
	

def palpha(mRp, mRb):
    """
    计算各组合维度alpha值

    参数
    --------
    mRp: m*n ndarray 组合收益率序列
    mRb：m*n ndarray 市场基准收益率序列

    返回值
    --------
    m*1 ndarray alpha值
    """
    mRp = checkarray(mRp)
    mRb = checkarray(mRb)
    m = row_count(mRp)
    if row_count(mRb) != m:
        mRb = repmat(mRb, m, 0)
    temp = np.ones((m, 2))
    for i in range(m):
        temp[i, :] = np.polyfit(mRb[i, :], mRp[i, :], 1)
    return temp[:, 1:2]


def pbeta(mRp, mRb):
    """
    计算各组合维度alpha值

    参数
    --------
    mRp: m*n ndarray 组合收益率序列
    mRb：m*n ndarray 市场基准收益率序列

    返回值
    --------
    m*1 ndarray beta值
    """
    mRp = checkarray(mRp)
    mRb = checkarray(mRb)
    m = row_count(mRp)
    if row_count(mRb) != m:
        mRb = repmat(mRb, m, 0)
    temp = np.ones((m, 2))
    for i in range(m):
        temp[i, :] = np.polyfit(mRb[i, :], mRp[i, :], 1)
    return temp[:, 0:1]


def pmcv(mRp, mRb, mRf):
    """
    计算m2测度

    参数
    --------
    mRp: m*n ndarray 组合收益率序列
    mRb：m*n ndarray 市场基准收益率序列
    mRf：m*n ndarray 无风险收益率序列

    返回值
    --------
    m*1 ndarray m2测度
    """
    mRp = checkarray(mRp)
    mRb = checkarray(mRb)
    mRf = checkarray(mRf)
    m = row_count(mRp)
    if row_count(mRb) != m:
        mRb = repmat(mRb, m, 0)
    if row_count(mRf) != m:
        mRf = repmat(mRf, m, 0)
    y = palpha(mRp, mRb) / ((np.std(mRp, 1, ddof=1, keepdims=True) / np.std(mRb, 1, ddof=1, keepdims=True)) - pbeta(mRp, mRb)) * np.abs(np.mean(mRb, 1, keepdims=True) - np.mean(mRf, 1, keepdims=True))
    return y


def pm2(mRp, mRb, mRf):
    """
    计算m2测度

    参数
    --------
    mRp: m*n ndarray 组合收益率序列
    mRb：m*n ndarray 市场基准收益率序列
    mRf：m*n ndarray 无风险收益率序列

    返回值
    --------
    m*1 ndarray m2测度
    """
    mRp = checkarray(mRp)
    mRf = checkarray(mRf)
    mRb = checkarray(mRb)
    m = row_count(mRp)
    if row_count(mRb) != m:
        mRb = repmat(mRb, m, 0)
    if row_count(mRf) != m:
        mRf = repmat(mRf, m, 0)
    y = (np.mean(mRp, 1) - np.mean(mRf, 1)) * (np.std(mRb, 1, ddof=1) / np.std(mRp, 1, ddof=1)) + np.mean(mRf, 1) - np.mean(mRb, 1)
    return y


def pinforatio(mRp, mRb):
    """
    计算信息比率

    参数
    --------
    mRp: m*n ndarray 组合收益率序列
    mRb：m*n ndarray 市场基准收益率序列

    返回值
    --------
    m*1 ndarray 信息比率
    """
    mRp = checkarray(mRp)
    mRb = checkarray(mRb)
    m = row_count(mRp)
    if row_count(mRp) != m:
        mRb = repmat(mRb, m, 0)
    y = (np.mean(mRp, 1) - np.mean(mRb, 1)) / np.std(mRp - mRb, 1, ddof=1) 
    return y

def psemistd(x, xd=None):
    """
    计算半标准差或者下行标准差

    参数
    --------
    x: m*n ndarray
    xd：m*n ndarray 目标值

    返回值
    --------
    m*1 ndarray 半标准差或者下行标准差，默认为半标准差
    """
    x = checkarray(x)
    if xd is None:
        xd = np.mean(x, 1, keepdims=True)
    xd = checkarray(xd)
    m = row_count(x)
    if row_count(xd) == 1:
        xd = repmat(xd, m, 0)
    y = np.zeros((m, 1))
    if col_count(xd) == 1:
        xd = xd * np.ones((1, col_count(x)))
    x = np.minimum(x - xd, 0)
    temp = np.zeros(x.shape)
    temp[x < 0] = 1
    count = np.sum(temp, 1, keepdims=True) - 1
    y = np.sqrt(np.sum(x ** 2, 1, keepdims=True)) / np.sqrt(count)
    return y


def psortino(mRp, mRf):
    """
    计算Sortino比率

    参数
    --------
    mRp: m*n ndarray 组合收益率序列
    mRf：m*n ndarray 无风险收益率序列

    返回值
    --------
    m*1 ndarray Sortino比率
    """
    mRp = checkarray(mRp)
    mRf = checkarray(mRf)
    semiStd = psemistd(mRp, 0)
    m = row_count(semiStd)
    if row_count(mRf) != m:
        mRf = repmat(mRf, m, 0)
    y = np.zeros((m, 1))
    Ind = np.where(semiStd == 0)[0]
    if not isempty(Ind):
        y[Ind] = 0
    Ind = np.where(semiStd != 0)[0]
    if not isempty(Ind):
        y[Ind] = np.mean(mRp[Ind, :] - mRf[Ind, :], 1, keepdims=True) / semiStd[Ind, :]
    return y


if __name__ == "__main__":
    mRp = sio.loadmat(r"D:\FAIS2\Sources\PM\pyfinmdl\matfiles\treynor")["mRp"]
    mRf = sio.loadmat(r"D:\FAIS2\Sources\PM\pyfinmdl\matfiles\treynor")["mRf"]
    y = psterling(mRp, mRf)
    print(y)
    print(y.shape)
    print(type(y))
    print(y.ndim)







