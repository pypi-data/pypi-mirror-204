import os
import shutil
import sys
import uuid
from contextlib import asynccontextmanager
from pathlib import Path

from beni import bfunc


def get(path: str | Path, expand: str = ''):
    if type(path) is not Path:
        path = Path(path)
    return path.joinpath(expand).resolve()


def getUser(expand: str = ''):
    return get(Path('~').expanduser(), expand)


def getDesktop(expand: str = ''):
    return getUser(f'Desktop/{expand}')


def getWorkspace(expand: str = ''):
    if sys.platform == 'win32':
        return get(f'C:/beni-workspace/{expand}')
    else:
        return get(f'/data/beni-workspace/{expand}')


def getTempFile():
    return getWorkspace(f'temp/{uuid.uuid4()}.tmp')


def getTempDir():
    return getWorkspace(f'temp/{uuid.uuid4()}')


def changeRelative(target: Path | str, fromRelative: Path | str, toRelative: Path | str):
    target = get(target)
    fromRelative = get(fromRelative)
    toRelative = get(toRelative)
    assert target.is_relative_to(fromRelative)
    return toRelative.joinpath(target.relative_to(fromRelative))


def openDir(dir: Path | str):
    os.system(f'start explorer {dir}')


def _remove(*pathList: Path | str):
    for path in pathList:
        path = get(path)
        if path.is_file():
            path.unlink(True)
        elif path.is_dir():
            shutil.rmtree(path)


async def remove(*pathList: Path | str):
    return await bfunc.runInThread(
        lambda: _remove(*pathList)
    )


def _make(*pathList: Path | str):
    for path in pathList:
        path = get(path)
        path.mkdir(parents=True, exist_ok=True)


async def make(*pathList: Path | str):
    return await bfunc.runInThread(
        lambda: _make(*pathList)
    )


def _clearDir(*dirList: Path | str):
    for dir in dirList:
        _remove(*[x for x in get(dir).iterdir()])


async def clearDir(*dirList: Path | str):
    return await bfunc.runInThread(
        lambda: _clearDir(*dirList)
    )


def _copy(src: Path | str, dst: Path | str):
    src = get(src)
    dst = get(dst)
    _make(dst.parent)
    if src.is_file():
        shutil.copyfile(src, dst)
    elif src.is_dir():
        shutil.copytree(src, dst)
    else:
        if not src.exists():
            raise Exception(f'copy error: src not exists {src}')
        else:
            raise Exception(f'copy error: src not support {src}')


async def copy(src: Path | str, dst: Path | str):
    return await bfunc.runInThread(
        lambda: _copy(src, dst)
    )


def _copyMany(dataDict: dict[Path | str, Path | str]):
    for src, dst in dataDict.items():
        _copy(src, dst)


async def copyMany(dataDict: dict[Path | str, Path | str]):
    return await bfunc.runInThread(
        lambda: _copyMany(dataDict)
    )


def _move(src: Path | str, dst: Path | str, force: bool = False):
    src = get(src)
    dst = get(dst)
    if dst.exists():
        if force:
            _remove(dst)
        else:
            raise Exception(f'move error: dst exists {dst}')
    _make(dst.parent)
    os.rename(src, dst)


async def move(src: Path | str, dst: Path | str, force: bool = False):
    return await bfunc.runInThread(
        lambda: _move(src, dst, force)
    )


def _moveMany(dataDict: dict[Path | str, Path | str], force: bool = False):
    for src, dst in dataDict.items():
        _move(src, dst, force)


async def moveMany(dataDict: dict[Path | str, Path | str], force: bool = False):
    return await bfunc.runInThread(
        lambda: _moveMany(dataDict, force)
    )


def renameName(src: Path | str, name: str):
    src = get(src)
    src.rename(src.with_name(name))


def renameStem(src: Path | str, stemName: str):
    src = get(src)
    src.rename(src.with_stem(stemName))


def renameSuffix(src: Path | str, suffixName: str):
    src = get(src)
    src.rename(src.with_suffix(suffixName))


def _listPath(path: Path | str, recursive: bool = False):
    '''获取指定路径下文件以及目录列表'''
    path = get(path)
    if recursive:
        return list(path.glob('**/*'))
    else:
        return list(path.glob("*"))


async def listPath(path: Path | str, recursive: bool = False):
    return await bfunc.runInThread(
        lambda: _listPath(path, recursive)
    )


def _listFile(path: Path | str, recursive: bool = False):
    '''获取指定路径下文件列表'''
    path = get(path)
    if recursive:
        return list(filter(lambda x: x.is_file(), path.glob('**/*')))
    else:
        return list(filter(lambda x: x.is_file(), path.glob('*')))


async def listFile(path: Path | str, recursive: bool = False):
    return await bfunc.runInThread(
        lambda: _listFile(path, recursive)
    )


def _listDir(path: Path | str, recursive: bool = False):
    '''获取指定路径下目录列表'''
    path = get(path)
    if recursive:
        return list(filter(lambda x: x.is_dir(), path.glob('**/*')))
    else:
        return list(filter(lambda x: x.is_dir(), path.glob('*')))


async def listDir(path: Path | str, recursive: bool = False):
    return await bfunc.runInThread(
        lambda: _listDir(path, recursive)
    )


@asynccontextmanager
async def useTempFile():
    tempFile = getTempFile()
    try:
        yield tempFile
    finally:
        await remove(tempFile)


@asynccontextmanager
async def useTempDir(isMakeDir: bool = False):
    tempDir = getTempDir()
    if isMakeDir:
        await make(tempDir)
    try:
        yield tempDir
    finally:
        await remove(tempDir)


@asynccontextmanager
async def useDir(path: str | Path):
    path = Path(path)
    currentPath = os.getcwd()
    try:
        os.chdir(str(path))
        yield
    finally:
        os.chdir(currentPath)
