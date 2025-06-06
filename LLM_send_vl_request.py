import asyncio
import aiohttp
import base64
import os

async def send_image(session, api_key, endpoint_url, image_path):
    # Encode image to base64
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')

    headers = {
        "Content-Type": "application/json"
    }
    
    # 只有当 api_key 不为 None 时才添加到 headers
    if api_key:
        headers["x-api-key"] = api_key

    payload = {
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What's in this image?"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    },
                    {"type": "text", "text": "Are you sure?"}
                ]
            }
        ],
        "max_tokens": 300
    }

    async with session.post(endpoint_url, headers=headers, json=payload, ssl=False) as response:
        return await response.json()

async def main():
    api_key = None  # 本地测试不需要 API 密钥
    endpoint_url = "http://localhost:18011/v1/chat/completions"

    # 获取图片文件夹
    image_folder = "/vllm_all/vllm_debug/vllm/test_pic"
    
    # 获取第一张图片
    image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.jpg', '.jpeg'))]
    if not image_files:
        print("没有找到JPEG图片")
        return
        
    # 使用第一张图片
    image_path = os.path.join(image_folder, image_files[0])
    print(f"使用图片: {image_path}")
    
    # 发送10个相同图片的请求
    async with aiohttp.ClientSession() as session:
        tasks = [send_image(session, api_key, endpoint_url, image_path) for _ in range(10)]
        results = await asyncio.gather(*tasks)

        for i, result in enumerate(results):
            print(f"请求 {i+1} 结果:", result)

if __name__ == "__main__":
    asyncio.run(main())
