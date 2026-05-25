from pydantic import BaseModel, PrivateAttr, model_validator
from mimetypes import guess_type
from requests import get
from PIL import Image, ImageOps
from io import BytesIO

from typing import Self




class RemoteFile(BaseModel):
    name: str
    mime: str|None = None
    url: str
    _data: bytes|None = PrivateAttr(
        default=None
    )

    @model_validator(mode="before")
    def validate(
        cls,
        data: dict
    ) -> dict:
        if not "mime" in data:
            data["mime"] = guess_type(data["name"])
        return data

    def get_data(
        self
    ) -> bytes:
        if not self._data:
            response = get(self.url)
            response.raise_for_status()
            self._data = response.content
        return self._data
    
    def clear_cache(
        self
    ) -> None:
        self._data = None

class RemoteImage():
    def __init__(
            self,
            file: RemoteFile
        ) -> None:
        """
        Converts a RemoteFile to a RemoteImage with special PIL
        functionality
        """
        self.name = file.name
        self.mime = file.mime
        self.url = file.url
        self._data = file._data

    def get_data(
        self
    ) -> bytes:
        if not self._data:
            response = get(self.url)
            response.raise_for_status()
            self._data = response.content
        return self._data

    def clear_cache(
        self
    ) -> None:
        self._data = None

    def compress_image(
        self,
        max_dimention: int = 1440,
        jpeg_quality: int = 85
    ) -> Self:
        """
        Compresses the image to a jpeg with a max width/height
        (whichever is largest) to `max_dimention` with quality
        `jpeg_quality`. Returns itself in order to make it work easier
        with inline dict constructors.
        """
        image = Image.open(BytesIO(self.get_data()))
        image = ImageOps.exif_transpose(image)

        width, height = image.size
        ratio = max(width, height) / max_dimention
        new_size = (int(width/ratio), int(height/ratio))
        if ratio > 1:
            image = image.resize(new_size, Image.LANCZOS)

        if image.mode in ("RGBA", "LA", "P"):
            image = image.convert("RGB")
        
        buffer = BytesIO()
        image.save(buffer,"jpeg",quality=jpeg_quality,optimize=True)
        self._data = buffer.getbuffer()

        return self