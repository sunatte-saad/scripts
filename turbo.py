from dotenv import load_dotenv

from PIL import Image
from io import BytesIO
import os
import gradio as gr
import base64
import requests

load_dotenv()

user=os.getenv("adictologin")
password=os.getenv("adictopassword")
url=os.getenv("adictourl")

def text2image(prompt:str,
               style:str="Deadpool XL Turbo",
               steps:int=6,
               guidance_scale:float=1.5,
               height:int=768,
               width:int=768,
               hr:float=1):
    payload={
  "prompt": prompt,
  "negative_prompt": "",
  "styles": [
    style
  ],
  "seed": -1,
    "enable_hr": True,
     "denoising_strength": 0.75,
  "hr_scale": hr,
   "hr_second_pass_steps": 10,
  "batch_size": 1,
  "steps": steps,
  "cfg_scale": guidance_scale,
  "width": width,
  "height": height,

  "override_settings": {"sd_model_checkpoint": "turbo"}
}
    response=requests.post(url+"sdapi/v1/txt2img",json=payload,auth=(user,password))
    data=response.json()
    imagebase64=data["images"][0]
    image_bytes = base64.b64decode(imagebase64)
    image_buffer = BytesIO(image_bytes)
    image = Image.open(image_buffer)
    return image

def get_styles():
    response=requests.get(url+"sdapi/v1/prompt-styles",auth=(user,password))
    data=response.json()
    return [data[i]['name'] for i in range(len(data))]
styles=get_styles()
iface=gr.Interface(fn=text2image,
                      inputs=[gr.Textbox(lines=2,placeholder="Enter your text here"),
                              gr.Dropdown(choices=styles),
                                          gr.Slider(minimum=1,maximum=20,step=1,label="Steps",value=6),
                                          gr.Slider(minimum=0.1,maximum=10,step=0.1,label="Guidance Scale",value=1.5),

                                          gr.Slider(minimum=512,maximum=2048,step=64,label="Height",value=768),

                                          gr.Slider(minimum=512,maximum=2048,step=64,label="Width",value=768),
                                          gr.Slider(minimum=1,maximum=2,step=0.1,label="HR",value=1.3)],

                      outputs="image",
                      title="Real time Image Generation",
                      description="Love wins <3",

                      allow_flagging="never",
                      live=True

)

iface.launch(share=True,)


