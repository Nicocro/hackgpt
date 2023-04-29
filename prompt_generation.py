from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chat_models import ChatOpenAI
from langchain import LLMChain
import concurrent.futures

from typing import List, Any
import re

from dotenv import load_dotenv


load_dotenv()

# chat = ChatAnthropic()
chat = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")


def generate_the_original_story(user_description: str) -> str:
    system_template = "You are ChatGPT, a large language model trained by OpenAI. Follow the user's instructions " \
                      "carefully. Respond using markdown. "
    prompt_1 = SystemMessagePromptTemplate.from_template(system_template)

    human_template = "You are a story teller. You generate a story according to users description. The user " \
                     "description is {user_description}. Generate a story according to description "
    prompt_2 = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages([prompt_1, prompt_2])

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    return chain.run(user_description=user_description)


def generate_the_steps_in_the_story(story: str, n_steps=10) -> List[str]:
    system_template = "You are ChatGPT, a large language model trained by OpenAI. Follow the user's instructions " \
                      "carefully. Respond using markdown. "
    prompt_1 = SystemMessagePromptTemplate.from_template(system_template)

    human_template = """{story}\n Given the story split split it into {n_steps} steps. Every step should consist of 
    concise summary of the narrative. 

Use the following format:    
1. The first element of the story
2. The second element ...
...
N. The last n'th element of the story"""
    prompt_2 = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages([prompt_1, prompt_2])

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    return re.findall(r"\d+\..+", chain.run(story=story, n_steps=n_steps))


def generate_image_prompts_based_on_a_step(step: str) -> str:
    system_template = "You are ChatGPT, a large language model trained by OpenAI. Follow the user's instructions " \
                      "carefully. Respond using markdown. "
    prompt_1 = SystemMessagePromptTemplate.from_template(system_template)

    human_template = """Write the nice image prompts for image generation model for the step in the story. ,

    If the story speaks about some specific human, just say Men or Woman. Give a detailed artistic expressions that 
    are useful for an image generation model. 

    Here are some examples: 
    - hyper close up photography of a majestic long ear kitsune spirit, ethereal ghost veil, japanese forest scenery, adorable, summer background, dynamic focus, round eyes, Hyperrealist, photography, 8k, ultra high quality, insanely detailed , perfect shading, intricate design, beautiful composition, soft lighting, many particles, Sony a7 III

    - Iron Man, (Arnold Tsang, Toru Nakayama), Masterpiece, Studio Quality, 6k , toa, toaair, 1boy, glowing, axe, mecha, science_fiction, solo, weapon, jungle , green_background, nature, outdoors, solo, tree, weapon, mask, dynamic lighting, detailed shading, digital texture painting 

    - professional portrait photograph of a gorgeous Norwegian girl in winter clothing with long wavy blonde hair, ((sultry flirty look)), freckles, beautiful symmetrical face, cute natural makeup, ((standing outside in snowy city street)), stunning modern urban upscale environment, ultra realistic, concept art, elegant, highly detailed, intricate, sharp focus, depth of field, f/1.8, 85mm, medium shot, mid shot, (centered image composition), (professionally color graded), ((bright soft diffused light)), volumetric fog, trending on instagram, trending on tumblr, hdr 4k, 8k

    - detailed and realistic portrait of a woman with a few freckles, round eyes and short messy hair shot outside, wearing a white t shirt, staring at camera, chapped lips, soft natural lighting, portrait photography, magical photography, dramatic lighting, photo realism, ultra-detailed, intimate portrait composition, Leica 50mm, f1. 4


    Write a prompt for following step in the story: {step}

    """
    prompt_2 = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages([prompt_1, prompt_2])

    chain = LLMChain(llm=chat, prompt=chat_prompt)

    return chain.run(step=step)


def pipeline(user_description: str, n_steps: int = 10) -> dict:
    story = generate_the_original_story(user_description)
    steps = generate_the_steps_in_the_story(story, n_steps)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        image_prompts_futures = [
            executor.submit(generate_image_prompts_based_on_a_step, step)
            for step in steps
        ]

    image_prompts = [fut.result() for fut in image_prompts_futures]

    return {"story": story, "steps": steps, "image_prompts": image_prompts}


if __name__ == '__main__':
    user_description = "A story about a brave frog."
    from time import time

    start = time()
    res = pipeline(user_description)
    finish = time()
    print(f"Time: {finish - start}")
