from .editor import ImageEditor
from .load import download, upload


async def reupload(url: str, ratio: float) -> str:
    image = await download(url)
    editor = ImageEditor(image, ratio)
    editor.crop()
    return await upload(editor.image)
