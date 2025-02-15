import json
import base64
from enum import Enum

import requests
from app.config import VENICE_API_KEY, PLACEHOLDER_IMAGE_URL


class NegativePrompts(Enum):
    GENERAL = "not professional"
    QUALITY = ("worst quality, normal quality, low quality, low res, blurry, jpeg artifacts, grainy, not high "
               "definition, not clear")
    ARTISTIC = ("bad anatomy, bad proportions, deformed, disconnected limbs, disfigured, extra arms, extra limbs, "
                "extra hands, fused fingers, gross proportions, long neck, malformed limbs, mutated, missing arms, "
                "missing fingers, poorly drawn hands, poorly drawn face")
    PLACE = "out of frame, not centered"
    BASIC = GENERAL + ", grainy, not clear, blurry, " + ARTISTIC + ", " + PLACE

class VeniceAiModelsEnum(Enum):
    FLUENTLY_XL = "fluently-xl"
    FLUX_DEV = "flux-dev"
    FLUX_DEV_UNCENSORED = "flux-dev-uncensored"
    PONY_REALISM = "pony-realism"
    STABLE_DIFFUSION_35 = "stable-diffusion-3.5"
    LUSTIFY_SDXL = "lustify-sdxl"

class VeniceAiModelStyles(Enum):
    THREE_D_MODEL = "3D Model"
    ANALOG_FILM = "Analog Film"
    ANIME = "Anime"
    CINEMATIC = "Cinematic"
    COMIC_BOOK = "Comic Book"
    CRAFT_CLAY = "Craft Clay"
    DIGITAL_ART = "Digital Art"
    ENHANCE = "Enhance"
    FANTASY_ART = "Fantasy Art"
    ISOMETRIC = "Isometric Style"
    LINE_ART = "Line Art"
    LOWPOLY = "Lowpoly"
    NEON_PUNK = "Neon Punk"
    ORIGAMI = "Origami"
    PHOTOGRAPHIC = "Photographic"
    PIXEL_ART = "Pixel Art"
    TEXTURE = "Texture"
    ADVERTISING = "Advertising"
    FOOD_PHOTOGRAPHY = "Food Photography"
    REAL_ESTATE = "Real Estate"
    ABSTRACT = "Abstract"
    CUBIST = "Cubist"
    GRAFFITI = "Graffiti"
    HYPERREALISM = "Hyperrealism"
    IMPRESSIONIST = "Impressionist"
    POINTILLISM = "Pointillism"
    POP_ART = "Pop Art"
    PSYCHEDELIC = "Psychedelic"
    RENAISSANCE = "Renaissance"
    STEAMPUNK = "Steampunk"
    SURREALIST = "Surrealist"
    TYPOGRAPHY = "Typography"
    WATERCOLOR = "Watercolor"
    FIGHTING_GAME = "Fighting Game"
    GTA = "GTA"
    SUPER_MARIO = "Super Mario"
    MINECRAFT = "Minecraft"
    POKEMON = "Pokemon"
    RETRO_ARCADE = "Retro Arcade"
    RETRO_GAME = "Retro Game"
    RPG_FANTASY = "RPG Fantasy Game"
    STRATEGY_GAME = "Strategy Game"
    STREET_FIGHTER = "Street Fighter"
    ZELDA = "Legend of Zelda"
    ARCHITECTURAL = "Architectural"
    DISCO = "Disco"
    DREAMSCAPE = "Dreamscape"
    DYSTOPIAN = "Dystopian"
    FAIRY_TALE = "Fairy Tale"
    GOTHIC = "Gothic"
    GRUNGE = "Grunge"
    HORROR = "Horror"
    MINIMALIST = "Minimalist"
    MONOCHROME = "Monochrome"
    NAUTICAL = "Nautical"
    SPACE = "Space"
    STAINED_GLASS = "Stained Glass"
    TECHWEAR = "Techwear Fashion"
    TRIBAL = "Tribal"
    ZENTANGLE = "Zentangle"
    COLLAGE = "Collage"
    FLAT_PAPERCUT = "Flat Papercut"
    KIRIGAMI = "Kirigami"
    PAPER_MACHE = "Paper Mache"
    PAPER_QUILLING = "Paper Quilling"
    PAPERCUT_COLLAGE = "Papercut Collage"
    PAPERCUT_SHADOW_BOX = "Papercut Shadow Box"
    STACKED_PAPERCUT = "Stacked Papercut"
    THICK_LAYERED_PAPERCUT = "Thick Layered Papercut"
    ALIEN = "Alien"
    FILM_NOIR = "Film Noir"
    HDR = "HDR"
    LONG_EXPOSURE = "Long Exposure"
    NEON_NOIR = "Neon Noir"
    SILHOUETTE = "Silhouette"
    TILT_SHIFT = "Tilt-Shift"

class ImageService():
    def __init__(self, model_name = VeniceAiModelsEnum.FLUENTLY_XL.value):
        self.model_name = model_name
        self.api_url = "https://api.venice.ai/api/v1/image/generate"
        self.headers = {
            "Authorization": f"Bearer {VENICE_API_KEY}",
            "Content-Type": "application/json"
        }

    def generate_image(self, prompt, style="3D Model"):
        payload = {
            "model": f"{self.model_name}",
            "prompt": prompt,
            "width": 1024,
            "height": 1024,
            "steps": 30,
            "hide_watermark": True,
            "return_binary": False,
            "seed": 123,
            "cfg_scale": 14,
            "style_preset": style,
            "negative_prompt": NegativePrompts.BASIC.value,
            "safe_mode": False
        }

        response = requests.request("POST", self.api_url, json=payload, headers=self.headers)

        if response.status_code == 200:
            try:
                image_json = json.loads(response.text)
                image_to_encode =  image_json['images'][0]
                return base64.b64decode(image_to_encode, validate=True)
            except:
                return None
        else:
            return None