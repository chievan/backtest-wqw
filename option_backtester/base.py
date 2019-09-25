import numpy as np
import datetime
import pandas as pd


def cnan(iCol, iRow):
    V = np.full((iCol, iRow), np.nan)
    return V


def repmat(a, repeats, axis=None):
    data = a
    if isinstance(a, np.ndarray):
        if a.ndim == 1:
            data = np.matrix(a)
    data = np.repeat(data, repeats, axis)
    data = np.asarray(data)
    return data


def isempty(m):
    if isinstance(m, tuple):
        return len(m) == 0
    else:
        if isinstance(m, np.matrix) or isinstance(m, np.ndarray):
            return m.size == 0
        else:
            raise TypeError('Excepted tuple or matrix or ndarray for m, Please Check DataType')


def row_count(data):
    if isinstance(data, np.matrix):
        return np.size(data, 0)
    if isinstance(data, np.ndarray):
        if data.ndim == 1:
            return 1
        else:
            return data.shape[0]


def col_count(data):
    if isinstance(data, np.matrix):
        return np.size(data, 1)
    if isinstance(data, np.ndarray):
        if data.ndim == 1:
            return data.size
        else:
            return data.shape[1]


def datenum(timedata):
    if isinstance(timedata, str):
        timedata = pd.to_datetime(timedata)
    if isinstance(timedata, pd.Timestamp):
        timedata = datetime.datetime(timedata.year, timedata.month, timedata.day)
    if isinstance(timedata, datetime.datetime):
        return timedata.toordinal() + 366
    if isinstance(timedata, int) or isinstance(timedata, float) or isinstance(timedata, np.int32):
        return timedata
    return timedata


def daysact(vStartDate, vEndDate=None):
    if (vEndDate is None):
        vNumdays = datenum(vStartDate)
    else:
        vNumdays = datenum(vEndDate) - datenum(vStartDate)
    return vNumdays


def checkarray(data):
    if isinstance(data, np.int32) or isinstance(data, int) or isinstance(data, float) or isinstance(data, np.float32) or isinstance(data, np.ndarray) or isinstance(data, np.uint8):
        data = np.asarray(np.matrix(data))
    return data


def ismember(a, b):
    bind = {}
    for i, v in enumerate(b):
        if v not in bind:
            bind[v] = i
    loc = [bind.get(itm, np.nan) for itm in a]
    return loc


def arraysort(data):
    a = np.unique(data)
    Ind = np.zeros((col_count(data), ))
    count = 0
    for x in data:
        Ind[count] = np.argwhere(a == x)
        count = count + 1
    Ind = np.asarray(Ind, dtype=int)
    return a, Ind


if __name__ == '__main__':
    A = np.asarray([1, 2, 2, 5, 3, 4, 3])
    y = arraysort(A)
    print(y)

