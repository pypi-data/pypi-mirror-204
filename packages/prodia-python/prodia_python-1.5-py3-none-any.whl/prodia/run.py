import requests
import time
import os

def run(key=None, prompt="kittens on cloud", negative_prompt="", model="v1-5-pruned-emaonly.ckpt [81761151]", sampler="Euler", aspect_ratio="square", steps=25, cfg_scale=7, seed=-1, upscale=False):
    if key is None:
        print("API key cant be None, get your API kay at https://app.prodia.com/api")
    else:
        if prompt=="kittens on cloud":
            print("Prompt not defined, used default (kittens on cloud))
        url = "https://api.prodia.com/v1/job"
        payload = {
            "prompt": prompt,
            "model": model,
            "sampler": sampler,
            "negative_prompt": negative_prompt,
            "steps": steps,
            "cfg_scale": cfg_scale,
            "seed": seed,
            "upscale": upscale,
            "aspect_ratio": aspect_ratio
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "X-Prodia-Key": key
        }
        headersrecieve = {
            "accept": "application/json",
            "X-Prodia-Key": key
        }
        print(f"Generating image with params:\n{payload}")
        response = requests.post(url, json=payload, headers=headers)
        job_id = response.json()['job']
        time.sleep(5)

        rec_url = f'https://api.prodia.com/v1/job/{job_id}'
        stt = True
        while stt is True:
            rec = requests.get(rec_url, headers=headersrecieve)
            status = rec.json()['status']
            if status == "succeeded":
                print(f"Image {job_id} generated!")
                image_url = rec.json()['imageUrl']
                return image_url
                stt = False
            elif status == "generating":
                print("Still working...")
                time.sleep(5)

