import asyncio
from pathlib import Path
from typing import Any

from beni import bbyte, bpath


async def winscp(winscp_exe: Path | str, key_file: str, server: str, cmd_list: list[str], show_cmd: bool = True):
    logFile = bpath.getUser('executeWinScp.log')
    await bpath.remove(logFile)
    ary = [
        'option batch abort',
        'option transfer binary',
        f'open sftp://{server} -privatekey={key_file} -hostkey=*',
    ]
    ary += cmd_list
    ary += [
        'close',
        'exit',
    ]
    # /console
    cmd = f'{winscp_exe} /log={logFile} /loglevel=0 /command ' + ' '.join("%s" % x for x in ary)
    if show_cmd:
        print(cmd)
    return await run(cmd)


async def runTry(*args: Any, output: str = '', error: str = ''):
    outputBytes, errorBytes, _ = await runQuiet(*args)
    if output and output not in bbyte.decode(outputBytes):
        raise Exception(f'命令执行失败: {" ".join([str(x) for x in args])}')
    if error and error not in bbyte.decode(errorBytes):
        raise Exception(f'命令执行失败: {" ".join([str(x) for x in args])}')


async def runQuiet(*args: Any):
    proc = await asyncio.create_subprocess_shell(
        ' '.join([str(x) for x in args]),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    return await proc.communicate() + (proc.returncode or 0,)


async def run(*args: Any):
    proc = await asyncio.create_subprocess_shell(
        ' '.join([str(x) for x in args]),
    )
    await proc.communicate()
    return proc.returncode or 0

# -------------------------------------------------------

# def execute(*pars: str, show_cmd: bool = True, show_output: bool = False, ignore_error: bool = False):
#     cmd = ' '.join(pars)
#     if show_cmd:
#         info(cmd)
#     p = subprocess.Popen(
#         cmd,
#         shell=True,
#         stdout=subprocess.PIPE,
#         stderr=subprocess.PIPE,
#     )
#     outBytes, errBytes = p.communicate()
#     p.kill()
#     if show_output:
#         outStr = decode(outBytes).replace('\r\n', '\n')
#         errStr = decode(errBytes).replace('\r\n', '\n')
#         if outStr:
#             info(f'output:\n{outStr}')
#         if errStr:
#             info(f'error:\n{errStr}')
#     if not ignore_error and p.returncode != 0:
#         raise Exception('执行命令出错')
#     return p.returncode, outBytes, errBytes
