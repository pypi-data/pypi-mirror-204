from pathlib import Path
from typing import Any, Callable
from zipfile import ZIP_DEFLATED, ZipFile

from beni import bexecute, bpath


async def _zip(zfile: Path, path_dict: dict[str, Path]):
    await bpath.make(zfile.parent)
    with ZipFile(zfile, 'w', ZIP_DEFLATED) as f:
        for fname in sorted(path_dict.keys()):
            file = path_dict[fname]
            if file.is_file():
                f.write(file, fname)


async def zipFile(zfile: Path | str, targetFile: Path | str, name: str | None = None):
    zfile = bpath.get(zfile)
    targetFile = bpath.get(targetFile)
    if name is None:
        name = targetFile.name
    await _zip(zfile, {name: targetFile})


async def zipFolder(zfile: Path | str, targetDir: Path | str, filterFunc: Callable[[Path], bool] | None = None):
    zfile = bpath.get(zfile)
    targetDir = bpath.get(targetDir)
    ary = await bpath.listPath(targetDir, True)
    if filterFunc:
        ary = list(filter(filterFunc, ary))
    await _zip(zfile, {str(x.relative_to(targetDir)): x for x in ary})


async def unzip(file: Path | str, outputDir: Path | str | None = None):
    file = bpath.get(file)
    outputDir = outputDir or file.parent
    with ZipFile(file) as f:
        for subFile in sorted(f.namelist()):
            try:
                # zipfile 代码中指定了cp437，这里会导致中文乱码
                encodeSubFile = subFile.encode('cp437').decode('gbk')
            except:
                encodeSubFile = subFile
            f.extract(subFile, outputDir)
            # 处理压缩包中的中文文件名在windows下乱码
            if subFile != encodeSubFile:
                toFile = bpath.get(outputDir, encodeSubFile)
                bpath.get(outputDir, subFile).rename(toFile)


async def sevenZip(zfile: Path | str, target: Path | str):
    await _runSeven('a', zfile, target)


async def sevenUnzip(zfile: Path | str, output: Path | str):
    await _runSeven('x', f'-o{output}', zfile)


async def sevenRename(zfile: Path | str, fromName: str, toName: str):
    await _runSeven('rn', zfile, fromName, toName)


async def _runSeven(*parList: Any):
    resultBytes, errorBytes, _ = await bexecute.runQuiet('7zr', *parList)
    assert not errorBytes, errorBytes.decode('gbk')
    assert b'Everything is Ok' in resultBytes, resultBytes.decode('gbk')
