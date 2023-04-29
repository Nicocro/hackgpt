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

    print(device)

    return pipe


def gen_initial_img(int_prompt):
    model = get_the_model(None)
    image = model(int_prompt, num_inference_steps=25).images[0]

    return image


def generate_story(int_prompt, steps, iterations=25):
    image_dic = {}
    init_img = gen_initial_img(int_prompt)
    img2img_model = get_image_to_image_model()
    img = init_img

    for idx, step in enumerate(steps):
        image = img2img_model(prompt=step, image=img, strength=0.75, guidance_scale=7.5,
                              num_inference_steps=iterations).images[0]
        image_dic[idx] = {
            "image": image,
            "prompt": step
        }
        img = image

    return init_img, image_dic
