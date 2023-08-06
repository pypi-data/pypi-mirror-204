from asyncio import run

import img_host

URL = "https://telegra.ph/file/334f0f0dc80e933f61a8c.jpg"


async def main():
    try:
        r = await img_host.reupload(URL, 6 / 4)
    except img_host.UploadError as e:
        print(e)
    else:
        print(r)


run(main())
