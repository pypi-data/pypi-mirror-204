from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, NamedTuple, Tuple, cast

from qiniu import Auth, BucketManager, build_batch_delete, etag, put_file
from qiniu.http import ResponseInfo

from beni import bfunc, bhttp, bpath, bzip


class QiniuItem(NamedTuple):
    key: str
    size: int
    qetag: str
    time: int


_FileListResult = tuple[dict[str, Any], Any, Any]


class QiniuBucket():

    def __init__(self, bucket: str, baseUrl: str, ak: str, sk: str) -> None:
        self.q = Auth(ak, sk)
        self.bucket = bucket
        self.baseUrl = baseUrl

    async def uploadFile(self, key: str, localFile: Path | str):
        token = self.q.upload_token(self.bucket, key)
        _, info = await bfunc.runInThread(
            lambda: cast(Tuple[Any, ResponseInfo], put_file(token, key, localFile, version='v2'))
        )
        assert info.exception is None
        assert info.status_code == 200

    def getPrivateFileUrl(self, key: str):
        return self.q.private_download_url(f'{self.baseUrl}/{key}')

    @asynccontextmanager
    async def _downloadPrivateFile(self, key: str):
        url = self.getPrivateFileUrl(key)
        async with bpath.useTempFile() as tempFile:
            tempFile = bpath.getTempFile()
            await bhttp.download(url, tempFile)
            assert tempFile.exists()
            yield tempFile

    async def downloadPrivateFile(self, key: str, localFile: Path | str):
        async with self._downloadPrivateFile(key) as tempFile:
            await bpath.move(tempFile, localFile, True)

    async def downloadPrivateFileUnzip(self, key: str, outputDir: Path | str):
        async with self._downloadPrivateFile(key) as tempFile:
            async with bpath.useTempDir() as tempDir:
                await bzip.unzip(tempFile, tempDir)
                for file in await bpath.listFile(tempDir, True):
                    toFile = bpath.changeRelative(file, tempDir, outputDir)
                    await bpath.move(file, toFile, True)

    async def downloadPrivateFileSevenUnzip(self, key: str, outputDir: Path | str):
        async with self._downloadPrivateFile(key) as tempFile:
            async with bpath.useTempDir() as tempDir:
                await bzip.sevenUnzip(tempFile, tempDir)
                for file in await bpath.listFile(tempDir, True):
                    toFile = bpath.changeRelative(file, tempDir, outputDir)
                    await bpath.move(file, toFile, True)

    async def getFileList(self, prefix: str, limit: int = 100) -> tuple[list[QiniuItem], str | None]:
        bucket = BucketManager(self.q)
        result, _, _ = await bfunc.runInThread(
            lambda: cast(_FileListResult, bucket.list(self.bucket, prefix, None, limit))
        )
        assert type(result) is dict
        fileList = [QiniuItem(x['key'], x['fsize'], x['hash'], x['putTime']) for x in result['items']]
        return fileList, cast(str | None, result.get('marker', None))

    async def getFileListByMarker(self, marker: str, limit: int = 100):
        bucket = BucketManager(self.q)
        result, _, _ = await bfunc.runInThread(
            lambda: cast(_FileListResult, bucket.list(self.bucket, None, marker, limit))
        )
        assert type(result) is dict
        fileList = [QiniuItem(x['key'], x['fsize'], x['hash'], x['putTime']) for x in result['items']]
        return fileList, cast(str | None, result.get('marker', None))

    async def deleteFiles(self, *keyList: str):
        bucket = BucketManager(self.q)
        result, _ = await bfunc.runInThread(
            lambda: cast(tuple[Any, Any], bucket.batch(build_batch_delete(self.bucket, keyList)))
        )
        assert result

    async def hashFile(self, file: Path | str):
        return await bfunc.runInThread(
            lambda: etag(file)
        )
