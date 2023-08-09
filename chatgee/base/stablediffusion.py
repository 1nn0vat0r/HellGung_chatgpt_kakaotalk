from flask import Flask, Response, request
import torch
from torch import autocast
from diffusers import StableDiffusionPipeline
from io import BytesIO
import base64

app = Flask(__name__)

device = "cpu"  # CUDA가 없는 환경에서는 "cpu"로 설정합니다.
model_id = "CompVis/stable-diffusion-v1-4"
pipe = StableDiffusionPipeline.from_pretrained(model_id, revision="fp16", torch_dtype=torch.float16)

@app.route("/")
def generate():
    prompt = request.args.get('prompt', '')  # Get the 'prompt' parameter from the query string
    with autocast(device):
        image = pipe(prompt, guidance_scale=8.5).images[0]

    buffer = BytesIO()
    image.save(buffer, format="PNG")
    imgstr = base64.b64encode(buffer.getvalue())

    return Response(content=imgstr, mimetype="image/png")

if __name__ == '__main__':
    app.run()
