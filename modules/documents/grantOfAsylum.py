from PIL      import Image
from typing   import Self
from datetime import date
import os, numpy as np

from modules.constants.screen   import *
from modules.constants.delays   import *
from modules.constants.other    import *
from modules.documents.document import Document, getBox
from modules.documents.passport import Nation
from modules.textRecognition    import parseText, parseDate
from modules.utils              import *

class GrantOfAsylum(Document):
    BACKGROUNDS = None

    TABLE_OFFSET = (225, 23)
    TEXT_COLOR   = (125, 109, 121)
    LAYOUT = {
        "seal-area":    getBox(235,  43, 534, 122),
        "first-name":   getBox(371, 131, 524, 142),
        "last-name":    getBox(371, 149, 524, 160),
        "nation":       getBox(407, 179, 524, 190),
        "number":       getBox(407, 197, 524, 208),
        "birth":        getBox(427, 215, 492, 226),
        "height":       getBox(407, 233, 456, 244),
        "weight":       getBox(407, 251, 524, 266),
        "fingerprints": getBox(247, 273, 524, 338),
        "expiration":   getBox(407, 349, 472, 360),
        "label":        getBox(225, 361, 544, 390),
        "picture":      getBox(245, 123, 364, 266) 
    }

    @staticmethod
    def load():
        GrantOfAsylum.BACKGROUNDS = Document.getBgs(
            GrantOfAsylum.LAYOUT, GrantOfAsylum.TABLE_OFFSET, Image.open(
                os.path.join(GrantOfAsylum.TAS.ASSETS, "papers", "grantOfAsylum.png")
            ).convert("RGB")
        )

        GrantOfAsylum.BACKGROUNDS["label"] = np.asarray(GrantOfAsylum.BACKGROUNDS["label"])
        
        sealWhiteBg = GrantOfAsylum.BACKGROUNDS["seal-area"].copy()
        sealWhiteBg.paste((255, 255, 255), (0, 0) + sealWhiteBg.size)
        GrantOfAsylum.BACKGROUNDS["seal-white"] = sealWhiteBg

    @staticmethod
    def checkMatch(docImg: Image.Image) -> bool:
        return np.array_equal(np.asarray(docImg.crop(GrantOfAsylum.LAYOUT["label"])), GrantOfAsylum.BACKGROUNDS["label"])
    
    @staticmethod
    def parse(docImg: Image.Image) -> Self:
        return GrantOfAsylum(
            name = Name(
                parseText(
                    docImg.crop(GrantOfAsylum.LAYOUT["first-name"]), GrantOfAsylum.BACKGROUNDS["first-name"],
                    GrantOfAsylum.TAS.FONTS["bm-mini"], GrantOfAsylum.TEXT_COLOR, PERMIT_PASS_NAME_CHARS,
                    endAt = "  "
                ),
                parseText(
                    docImg.crop(GrantOfAsylum.LAYOUT["last-name"]), GrantOfAsylum.BACKGROUNDS["last-name"],
                    GrantOfAsylum.TAS.FONTS["bm-mini"], GrantOfAsylum.TEXT_COLOR, PERMIT_PASS_NAME_CHARS,
                    endAt = "  "
                ),
            ),
            nation = Nation(parseText(
                docImg.crop(GrantOfAsylum.LAYOUT["nation"]), GrantOfAsylum.BACKGROUNDS["nation"],
                GrantOfAsylum.TAS.FONTS["bm-mini"], GrantOfAsylum.TEXT_COLOR, PERMIT_PASS_CHARS,
                endAt = "  "
            )),
            number = parseText(
                docImg.crop(GrantOfAsylum.LAYOUT["number"]), GrantOfAsylum.BACKGROUNDS["number"],
                GrantOfAsylum.TAS.FONTS["bm-mini"], GrantOfAsylum.TEXT_COLOR, PASSPORT_NUM_CHARS,
                endAt = "  "
            ),
            birth = parseDate(
                docImg.crop(GrantOfAsylum.LAYOUT["birth"]), GrantOfAsylum.BACKGROUNDS["birth"],
                GrantOfAsylum.TAS.FONTS["bm-mini"], GrantOfAsylum.TEXT_COLOR
            ),
            height = int(parseText(
                docImg.crop(GrantOfAsylum.LAYOUT["height"]), GrantOfAsylum.BACKGROUNDS["height"],
                GrantOfAsylum.TAS.FONTS["bm-mini"], GrantOfAsylum.TEXT_COLOR, HEIGHT_CHARS,
                endAt = "cm"
            )[:-2]),
            weight = int(parseText(
                docImg.crop(GrantOfAsylum.LAYOUT["weight"]), GrantOfAsylum.BACKGROUNDS["weight"],
                GrantOfAsylum.TAS.FONTS["bm-mini"], GrantOfAsylum.TEXT_COLOR, WEIGHT_CHARS,
                endAt = "kg"
            )[:-2]),
            expiration = parseDate(
                docImg.crop(GrantOfAsylum.LAYOUT["expiration"]), GrantOfAsylum.BACKGROUNDS["expiration"],
                GrantOfAsylum.TAS.FONTS["bm-mini"], GrantOfAsylum.TEXT_COLOR
            ),
            sealArea     = docImg.crop(GrantOfAsylum.LAYOUT["seal-area"]),
            picture      = docImg.crop(GrantOfAsylum.LAYOUT["picture"]),
            fingerprints = docImg.crop(GrantOfAsylum.LAYOUT["fingerprints"])
        )
    
    def __init__(self, name, nation, number, birth, height, weight, expiration, sealArea, picture, fingerprints):
        self.name: Name       = name
        self.nation: Nation   = nation
        self.number           = number
        self.birth: date      = birth
        self.height           = height
        self.weight           = weight
        self.expiration: date = expiration
        self.sealArea:     Image.Image = sealArea
        self.picture:      Image.Image = picture
        self.fingerprints: Image.Image = fingerprints
    
    def checkForgery(self) -> bool:        
        return all(Document.checkNoSeal(
            np.asarray(self.sealArea), GrantOfAsylum.BACKGROUNDS["seal-area"],
            seal, GrantOfAsylum.BACKGROUNDS["seal-white"]
        ) for seal in GrantOfAsylum.TAS.MOA_SEALS)
    
    def __repr__(self) -> str:
        return f"""==- Grant Of Asylum -==
name:       {self.name}
nation:     {self.nation}
number:     {self.number}
birth:      {self.birth}
height:     {self.height}
weight:     {self.weight}
expiration: {self.expiration}
"""