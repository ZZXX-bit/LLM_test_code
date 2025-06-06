#!/bin/bash

# 将图片转换为base64格式
IMAGE_PATH="/vllm_all/vllm_debug/vllm/test_pic/test2.jpg"
BASE64_IMAGE=$(base64 -w 0 "$IMAGE_PATH")

# 创建临时JSON文件
cat > request.json << EOF
{
  "model": "meta-llama/llama-4-scout-17b-16e-instruct",
  "messages": [
    {
      "role": "system", 
      "content": "Be a helpful assistant."
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Determine if there is visible smoke plume or fire flame in the image. only only only smokes. only 100% smokes avoid false alarms. avoid mistakes. Ignore clouds in sky. Not street light. Not house light. Not sky. Not cloud. Not fog. Not in sky. Ignore sky. Do not raise alarms for street lighting, cloud, fog, haze, or normal atmospheric conditions in the sky. Do not raise alarms for sunlight reflection, cloud cover, camera exposure shifts and camera lens reflections, lens flare, cloud formations, distant mist, bright ground, boats, water surfaces, flag poles or fences. Only raise an alarm for smoke plume or fire flame. At the end of your analysis, give short explanation of your reasoning. Just 100% smoke Say ( Alarm ) if you detect smoke plume or fire flame. If you don't detect then say ( No-Alarm )."
        },
        {
          "type": "image_url",
          "image_url": {
            "url": "data:image/jpeg;base64,${BASE64_IMAGE}"
          }
        }
      ]
    }
  ],
  "temperature": 0.6,
  "top_p": 0.9,
  "n": 1,
  "max_tokens": 512,
  "stream": false
}
EOF

# 发送10次请求
for i in 1 2 3 4 5 6 7 8 9 10
do
  echo "发送第 $i 次请求..."
  curl -X POST http://localhost:18011/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d @request.json
  echo -e "\n\n"
done 
