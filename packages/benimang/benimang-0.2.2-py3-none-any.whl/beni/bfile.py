from pathlib import Path
from typing import Any

import aiofiles

from beni import bfunc, block, bpath

_limit = 50


@block.useLimit(_limit)
async def writeText(file: Path | str, content: str, encoding: str = 'utf8', newline: str = '\n'):
    file = bpath.get(file)
    await bpath.make(file.parent)
    async with aiofiles.open(file, 'w', encoding=encoding, newline=newline) as f:
        return await f.write(content)


@block.useLimit(_limit)
async def writeBytes(file: Path | str, data: bytes):
    file = bpath.get(file)
    await bpath.make(file.parent)
    async with aiofiles.open(file, 'wb') as f:
        return await f.write(data)


@block.useLimit(_limit)
async def writeYaml(file: Path | str, data: Any):
    import yaml
    await writeText(file, yaml.safe_dump(data))


@block.useLimit(_limit)
async def writeJson(file: Path | str, data: Any, mini: bool = True):
    if mini:
        await writeText(file, bfunc.jsonDumpsMini(data))
    else:
        import json
        await writeText(file, json.dumps(data, ensure_ascii=False, sort_keys=True, indent=4))


@block.useLimit(_limit)
async def readText(file: Path | str, encoding: str = 'utf8', newline: str = '\n'):
    async with aiofiles.open(file, 'r', encoding=encoding, newline=newline) as f:
        return await f.read()


@block.useLimit(_limit)
async def readBytes(file: Path | str):
    async with aiofiles.open(file, 'rb') as f:
        return await f.read()


@block.useLimit(_limit)
async def readYaml(file: Path | str):
    import yaml
    return yaml.safe_load(
        await readText(file)
    )


@block.useLimit(_limit)
async def readJson(file: Path | str):
    import orjson
    return orjson.loads(await readBytes(file))


@block.useLimit(_limit)
async def readToml(file: Path | str):
    import tomllib
    return tomllib.loads(
        await readText(file)
    )


async def md5File(file: Path | str):
    return bfunc.md5Bytes(
        await readBytes(file)
    )


async def crcFile(file: Path | str):
    return bfunc.crcBytes(
        await readBytes(file)
    )
