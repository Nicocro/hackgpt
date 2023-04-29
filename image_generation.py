import json
import os

import torch
from diffusers import StableDiffusionImg2ImgPipeline, \
    StableDiffusionPipeline


# check device
def check_cuda_device():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(device)
    return device


def get_image_to_image_model(path=None, device=None):
    model_id = "stabilityai/stable-diffusion-2"
    if path:
        pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
            path,
            torch_dtype=torch.float16)
    else:
        pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
            model_id,
            torch_dtype=torch.float16)
    if device:
        if device == "cuda" or device == "cpu":
            pipe.to(device)
    else:
        device = check_cuda_device()
        pipe.to(device)

    return pipe


def get_the_model(path=None, device=None):
    model_id = "stabilityai/stable-diffusion-2"
    if path:
        pipe = StableDiffusionPipeline.from_pretrained(path, torch_dtype=torch.float16)
    else:
        pipe = StableDiffusionPipeline.from_pretrained(model_id,
                                                       torch_dtype=torch.float16)
    if device:
        pipe.to(device)
    else:
        device = check_cuda_device()
        pipe.to(device)

    return pipe


def generate_image(model, prompt):
    image = model(prompt).images[0]
    return image


def generate_story(pipe, original_image, steps, iterations=10):
    image_dic = {}
    img = original_image
    for idx, step in enumerate(steps):
        print(idx)
        image = pipe(prompt=step, image=img, strength=0.75, guidance_scale=7.5,
                     num_inference_steps=iterations).images[0]
        image_dic[f"step_{idx}"] = {
            "image": image,
            "prompt": step
        }
        img = image
        break

    return image_dic


def save_list_to_json(prompt_list, path_to_save):
    with open(path_to_save, 'w') as f:
        # write the list to the file in JSON format
        json.dump(prompt_list, f)


def save_images(image_dic, path_to_save):
    prompts = []
    for image_item in image_dic:
        _data = image_dic[image_item]
        image, prompt = _data["image"], _data["prompt"]
        image.save(os.path.join(path_to_save, f"{image_item}.png"))
        prompts.append(prompt)

    save_list_to_json(prompt, os.path.join(path_to_save, "prompt.json"))


def load_json(path_json):
    # Load the JSON file as a dictionary
    with open(path_json, "r") as infile:
        data = json.load(infile)

    return data
