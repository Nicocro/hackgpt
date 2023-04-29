import torch

from diffusers import StableDiffusionImg2ImgPipeline, \
    StableDiffusionPipeline


def check_cuda_device():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(device)
    return device


def get_the_model(device=None):
    model_id = "stabilityai/stable-diffusion-2"
    pipe = StableDiffusionPipeline.from_pretrained(model_id,
                                                   torch_dtype=torch.float16)
    if device:
        pipe.to(device)
    else:
        device = check_cuda_device()
        pipe.to(device)

    return pipe


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


def gen_initial_img(int_prompt):
    # image = get_the_model(num_inference_steps=100).images[0]
    model = get_the_model(None)
    image = model(int_prompt, num_inference_steps=100).images[0]

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
