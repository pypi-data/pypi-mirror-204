import asyncio
import json
import os
import sys
import time
from datetime import datetime as Datetime
from datetime import timezone
from enum import Enum
from pathlib import Path
from typing import Optional
from zoneinfo import ZoneInfo

import nest_asyncio
import pyperclip
import typer
from colorama import Fore

from beni import bcolor, bexecute, bfile, binput, bpath

_app = typer.Typer()


def main():
    nest_asyncio.apply()
    _app()


def exit(errorMsg: str):
    print(errorMsg)
    sys.exit(errorMsg and 1 or 0)


# ------------------------------------------------------------------------


@_app.command('time')
def showtime(
    value: str = typer.Argument('', help='时间戳（支持整形和浮点型）或日期（格式: 2021-11-23）', show_default=False, metavar='[Timestamp or Date]'),
    value2: str = typer.Argument('', help='时间（格式: 09:20:20），只有第一个参数为日期才有意义', show_default=False, metavar='[Time]')
):
    '''
    格式化时间戳

    beni showtime

    beni showtime 1632412740

    beni showtime 1632412740.1234

    beni showtime 2021-9-23

    beni showtime 2021-9-23 09:47:00
    '''

    timestamp: float | None = None
    if not value:
        timestamp = time.time()
    else:
        try:
            timestamp = float(value)
        except:
            try:
                if value2:
                    timestamp = Datetime.strptime(f'{value} {value2}', '%Y-%m-%d %H:%M:%S').timestamp()
                else:
                    timestamp = Datetime.strptime(f'{value}', '%Y-%m-%d').timestamp()
            except:
                pass

    if timestamp is None:
        color = typer.colors.BRIGHT_RED
        typer.secho('参数无效', fg=color)
        typer.secho('\n可使用格式: ', fg=color)
        msgAry = str(showtime.__doc__).strip().replace('\n\n', '\n').split('\n')[1:]
        msgAry = [x.strip() for x in msgAry]
        typer.secho('\n'.join(msgAry), fg=color)
        raise typer.Abort()

    print()
    print(timestamp)
    print()
    localtime = time.localtime(timestamp)
    tzname = time.tzname[(time.daylight and localtime.tm_isdst) and 1 or 0]
    bcolor.printx(time.strftime('%Y-%m-%d %H:%M:%S %z', localtime), tzname, colorList=[Fore.YELLOW])
    print()

    # pytz版本，留作参考别删除
    # tzNameList = [
    #     'Asia/Tokyo',
    #     'Asia/Kolkata',
    #     'Europe/London',
    #     'America/New_York',
    #     'America/Chicago',
    #     'America/Los_Angeles',
    # ]
    # for tzName in tzNameList:
    #     tz = pytz.timezone(tzName)
    #     print(Datetime.fromtimestamp(timestamp, tz).strftime(fmt), tzName)

    datetime_utc = Datetime.fromtimestamp(timestamp, tz=timezone.utc)
    tzname_list = [
        'Australia/Sydney',
        'Asia/Tokyo',
        'Asia/Kolkata',
        'Africa/Cairo',
        'Europe/London',
        'America/Sao_Paulo',
        'America/New_York',
        'America/Chicago',
        'America/Los_Angeles',
    ]
    for tzname in tzname_list:
        datetime_tz = datetime_utc.astimezone(ZoneInfo(tzname))
        dstStr = ''
        dst = datetime_tz.dst()
        if dst:
            dstStr = f'(DST+{dst})'
        print(f'{datetime_tz} {tzname} {dstStr}')

    print()

# ------------------------------------------------------------------------


@_app.command()
def format_json_file(file_path: str, encoding: str = 'utf8'):
    '''格式化 JSON 文件'''
    file = bpath.get(file_path)
    content = file.read_text(encoding=encoding)
    data = json.loads(content)
    file.write_text(json.dumps(data, indent=4, ensure_ascii=False, sort_keys=True), encoding=encoding)


# ------------------------------------------------------------------------

class MirrorType(str, Enum):
    pip = 'pip'
    npm = 'npm'
    all = 'all'


@_app.command()
def mirror(
    mirror_type: MirrorType = typer.Argument(MirrorType.all),
    enabled: bool = typer.Argument(True),
):
    '''设置镜像地址'''
    async def _():
        if mirror_type in (MirrorType.pip, MirrorType.all):
            file = bpath.getUser('pip/pip.ini')
            if enabled:
                content = '\n'.join([
                    '[global]',
                    'index-url = https://mirrors.aliyun.com/pypi/simple',
                ])
                await bfile.writeText(file, content)
                bcolor.printYellow('写入文件', file)
                print(content)
            else:
                await bpath.remove(file)
                bcolor.printRed('删除文件', file)
        if mirror_type in (MirrorType.npm, MirrorType.all):
            file = bpath.getUser('.bashrc')
            if enabled:
                content = '\n'.join([
                    'registry=https://registry.npm.taobao.org/',
                    'electron_mirror=https://npm.taobao.org/mirrors/electron/',
                ])
                await bfile.writeText(file, content)
                bcolor.printYellow('写入文件', file)
                print(content)
            else:
                await bpath.remove(file)
                bcolor.printRed('删除文件', file)
    asyncio.run(_())


# ------------------------------------------------------------------------

@_app.command()
def venv(
    addPackages: list[str] = typer.Argument(None),
    path: Path = typer.Option(None, help="指定路径，默认当前目录"),
    clear: bool = typer.Option(False, help='删除venv目录后重新安装，可以保证环境干净'),
    clear_all: bool = typer.Option(False, help='删除venv.lock文件和venv目录后重新安装，可以保证环境干净的情况下将包更新'),
):
    '''python 虚拟环境配置'''
    path = path or Path(os.getcwd())
    clear = clear or clear_all

    async def _():
        venvDir = bpath.get(path, 'venv')
        _assertDirOrNotExists(venvDir)
        if not venvDir.exists():
            await binput.confirm('指定目录为非venv目录，是否确认新创建？')
        if clear:
            await bpath.remove(venvDir)
        if not venvDir.exists():
            await bexecute.run(f'python.exe -m venv {venvDir}')
        vevnListFile = bpath.get(path, 'venv.list')
        _assertFileOrNotExists(vevnListFile)
        if not vevnListFile.exists():
            await bfile.writeText(vevnListFile, '')
        await tidyVenvFile(vevnListFile, addPackages)
        venvLockFile = bpath.get(path, 'venv.lock')
        _assertFileOrNotExists(venvLockFile)
        if clear_all:
            await bpath.remove(venvLockFile)
        elif venvLockFile.exists():
            await tidyVenvFile(venvLockFile, addPackages)
        targetFile = venvLockFile if venvLockFile.exists() else vevnListFile
        pip = bpath.get(venvDir, 'Scripts/pip.exe')
        await pipInstall(pip, targetFile)
        await bexecute.run(f'{pip} freeze > {venvLockFile}')

    async def pipInstall(pip: Path, file: Path):
        python = pip.with_name('python.exe')
        assert python.is_file()
        assert not await bexecute.run(f'{python} -m pip install --upgrade pip'), '更新 pip 失败'
        assert pip.is_file()
        assert not await bexecute.run(f'{pip} install -r {file}'), '执行失败'

    async def tidyVenvFile(file: Path, addPackages: list[str]):
        addPackageNames = [getPackageName(x) for x in addPackages]
        ary = (await bfile.readText(file)).strip().replace('\r\n', '\n').replace('\r\n', '\n').split('\n')
        ary = list(filter(lambda x: getPackageName(x) not in addPackageNames, ary))
        ary.extend(addPackages)
        ary.sort()
        await bfile.writeText(file, '\n'.join(ary).strip())

    def getPackageName(value: str):
        sepList = ['>', '<', '=']
        for sep in sepList:
            if sep in value:
                return value.split(sep)[0]
        return value

    asyncio.run(_())


def _assertFileOrNotExists(file: Path):
    assert file.is_file() or not file.exists(), f'必须是文件 {file=}'


def _assertDirOrNotExists(folder: Path):
    assert folder.is_dir() or not folder.exists(), f'必须是文件 {folder=}'


# ------------------------------------------------------------------------


@_app.command()
def bin(
    name: str = typer.Argument(None, help="如果有多个使用,分割"),
    is_file: bool = typer.Option(False, '--is-file', '-f', help="文件形式指定参数，行为单位"),
    ak: str = typer.Option(..., help="七牛云账号AK"),
    sk: str = typer.Option(..., help="七牛云账号SK"),
    output: Optional[Path] = typer.Option(None, '--output', '-o', help="本地保存路径")
):
    '''从七牛云下载执行文件'''

    async def _():
        try:
            from beni.bqiniu import QiniuBucket
            nonlocal output
            bucketName = 'pytask'
            bucketUrl = 'http://qiniu-cdn.pytask.com'
            if output is None:
                output = Path(os.curdir)
            bucket = QiniuBucket(bucketName, bucketUrl, ak, sk)
            targetList: list[str] = []
            if is_file:
                content = await bfile.readText(Path(name))
                targetList.extend(content.replace('\r\n', '\n').split('\n'))
            else:
                targetList.extend(name.strip().split(','))
            for target in targetList:
                file = output.joinpath(target).resolve()
                if file.exists():
                    print(f'exists {file}')
                else:
                    key = f'bin/{target}.zip'
                    await bucket.downloadPrivateFileUnzip(key, output)
                    bcolor.printGreen(f'added  {file}')
        except Exception as e:
            print(e)

    asyncio.run(_())


# ------------------------------------------------------------------------


@_app.command()
def proxy(
    port: int = typer.Option(15236, help="代理服务器端口"),
):
    '''生成终端设置代理服务器的命令'''
    msg = '\r\n'.join([
        f'set http_proxy=http://localhost:{port}',
        f'set https_proxy=http://localhost:{port}',
        f'set all_proxy=http://localhost:{port}',
        '',
    ])
    print('\r\n' + msg)
    pyperclip.copy(msg)
    print('已复制')
