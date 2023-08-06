import aiohttp
import io
from PIL import Image

class Image:
    async def generate(self, prompt, negative):
        async with aiohttp.ClientSession() as session:
            async with session.post('https://api.lexica.ai/v1/image/generate', json={
                'text': prompt,
                'not_include': negative,
                'num_images': 1 # мы получаем только одно изображение
            }) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    image_url = data['images'][0]
                    async with session.get(image_url) as image_resp:
                        if image_resp.status == 200:
                            image_data = await image_resp.read()
                            img = Image.open(io.BytesIO(image_data))
                            return img
                else:
                    raise Exception('Error generating image')