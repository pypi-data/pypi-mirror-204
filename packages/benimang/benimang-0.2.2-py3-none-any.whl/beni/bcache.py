from __future__ import annotations

import asyncio
import pickle
from datetime import datetime, timedelta
from functools import wraps
from pathlib import Path
from typing import Any, Callable, Coroutine, cast
from uuid import uuid4

from beni import bfile, bfunc, bpath, btime
from beni.bfunc import getWrapped

_foreverDatetime = datetime(9999, 9, 9)


class BCacheFileManager:

    def __init__(self, cacheDir: Path) -> None:
        self._cacheDir = cacheDir
        self._waitingWriteDeadlineFile = False
        self._deadlineFile = cacheDir.joinpath('deadline.dat')
        if self._deadlineFile.exists():
            try:
                with open(self._deadlineFile, 'rb') as f:
                    self._deadlineDict = pickle.loads(f.read())
            except:
                self._deadlineDict = {}
        else:
            self._deadlineDict = {}

    async def put(self, key: str, data: Any, duration: timedelta | None = None, deadline: datetime | None = None):
        assert not (duration and deadline), 'BCacheFileManager.put 不允许 duration 和 deadline 同时设置'
        file = self._getFile(key)
        try:
            await bfile.writeBytes(
                file,
                pickle.dumps(data),
            )
            if file in self._deadlineDict:
                del self._deadlineDict[file]
                await self._updateDeadlineFile()
            if not deadline:
                if duration:
                    deadline = btime.datetime() + duration
                else:
                    deadline = _foreverDatetime
            self._deadlineDict[file] = deadline
            await self._updateDeadlineFile()
            return True
        except:
            await bpath.remove(file)
            if file in self._deadlineDict:
                del self._deadlineDict[file]
                await self._updateDeadlineFile()
            return False

    async def get(self, key: str):
        file = self._getFile(key)

        # 判断缓存超时直接退出
        if file in self._deadlineDict:
            if btime.datetime() > self._deadlineDict[file]:
                del self._deadlineDict[file]
                await self._updateDeadlineFile()
                await bpath.remove(file)
                return
            if file.is_file():
                return pickle.loads(await bfile.readBytes(file))
            else:
                del self._deadlineDict[file]
                await self._updateDeadlineFile()
        else:
            await bpath.remove(file)

    async def clear(self, key: str):
        await bpath.remove(self._getFile(key))

    def _getFile(self, key: str):
        return bpath.get(self._cacheDir, bfunc.crcStr(key))

    async def _updateDeadlineFile(self):
        if not self._waitingWriteDeadlineFile:
            self._waitingWriteDeadlineFile = True
            asyncio.create_task(
                self._writeDeadlineFile()
            )

    async def _writeDeadlineFile(self):
        await asyncio.sleep(2)
        self._waitingWriteDeadlineFile = False
        try:
            await bfile.writeBytes(
                self._deadlineFile,
                pickle.dumps(self._deadlineDict),
            )
        except:
            pass

    def forFunc(self, key: str, duration: timedelta | None = None, deadline: datetime | None = None):
        def fun(func: bfunc.AsyncFun) -> bfunc.AsyncFun:
            @wraps(func)
            async def wrapper(*parlist: Any, **pardict: Any):
                try:
                    cacheResult = await self.get(key)
                    if cacheResult:
                        return cacheResult
                    else:
                        result = await func(*parlist, **pardict)
                        await self.put(key, result, duration, deadline)
                        return result
                except:
                    await self.clear(key)
                    raise
            return cast(Any, wrapper)
        return fun


def cacheFunc(func: bfunc.AsyncFun) -> bfunc.AsyncFun:
    @wraps(func)
    async def wraper(*parList: Any, **parDict: Any):
        baseFunc = getWrapped(func)
        cacheData = _cacheFuncDict.get(baseFunc)
        if not cacheData:
            cacheData = _CacheFuncData()
            _cacheFuncDict[baseFunc] = cacheData
        key = (parList, parDict)
        while True:
            result = cacheData.getResult((parList, parDict))
            if result is not None:
                return result
            elif cacheData.running:
                await cacheData.event.wait()
            else:
                cacheData.running = True
                seed = cacheData.seed
                try:
                    result = await func(*parList, **parDict)
                    if seed == cacheData.seed:
                        cacheData.setResult(key, result)
                        return result
                except:
                    return None
                finally:
                    cacheData.running = False
                    cacheData.event.set()
                    cacheData.event.clear()
    return cast(Any, wraper)


def cacheFuncClear(func: Callable[..., Coroutine[Any, Any, object]]):
    baseFunc = getWrapped(func)
    cacheData = _cacheFuncDict.get(baseFunc)
    if cacheData:
        cacheData.clearResult()


_cacheFuncDict: dict[Callable[..., Coroutine[Any, Any, object]], _CacheFuncData] = {}


class _CacheFuncData:

    def __init__(self) -> None:
        self.event = asyncio.Event()
        self.running = False
        self.seed = uuid4()
        self._resultList: list[tuple[tuple[tuple[Any, ...], dict[str, Any]], Any]] = []

    def getResult(self, key: tuple[tuple[Any, ...], dict[str, Any]]):
        for xx in self._resultList:
            if xx[0] == key:
                return xx[1]

    def setResult(self, key: tuple[tuple[Any, ...], dict[str, Any]], result: Any):
        self._resultList = list(filter(lambda x: x[0] != key, self._resultList))
        self._resultList.append((key, result))

    def clearResult(self):
        self._resultList.clear()
        self.seed = uuid4()
