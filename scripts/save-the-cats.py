#!/usr/bin/env -S uv run --python 3.13t

# jokes aside, this module downloads cats from images at http.cat,
# crops them to only save the cat images in their frames
# (without the titles & subtitles under those frames)
# so that they can be used to later display cats in the http.cat game

# btw, i have no idea how to benchmark this
# if you have one, DM me on Discord: @bswck

# /// script
# requires-python = ">=3.13"
# dependencies = ["httpx", "numpy", "pillow"]
# ///

import os
import sys
from collections import deque
from collections.abc import Callable, Iterable
from concurrent.futures import ThreadPoolExecutor
from contextlib import suppress
from contextvars import Context, ContextVar, copy_context
from dataclasses import dataclass, field
from functools import partial
from hashlib import md5
from http.client import responses as http_responses
from io import BytesIO
from itertools import chain
from operator import attrgetter
from pathlib import Path
from typing import Any, ClassVar, Literal, NamedTuple, Self, cast

import httpx
import numpy as np
from PIL import Image as imagelib

CACHE_DIR = Path(".purrr_cache/")
CAT_DIR = Path("static/cats/")

pixel_counts_var: ContextVar[dict[int, int]] = ContextVar("pixel_counts")
code_var: ContextVar[int] = ContextVar("cat_id")

# early bindings
get_pixel_counts = pixel_counts_var.get
get_code = code_var.get

consume: Callable[[Iterable[Any]], Any] = partial(deque, maxlen=0)
# pass messages ending with "\n" for no print buffer collisions
atomic_print = partial(print, end="")

is_bright_enough = (100, 100, 100).__lt__
is_dark_enough = (100, 100, 100).__ge__


class CatManager(NamedTuple):
    cache: Path = CACHE_DIR
    shelter: Path = CAT_DIR


@dataclass
class Cat:
    code: int
    filename: str
    image: imagelib.Image
    mgr: CatManager

    context: Context = field(default_factory=copy_context)

    _url_template: ClassVar[str] = "https://http.cat/images-original/{}"

    @property
    def url(self) -> str:
        return self._url_template.format(self.filename)

    @property
    def shelter(self) -> Path:
        return self.mgr.shelter / self.filename

    @classmethod
    def fetch(
        cls, code: int, mgr: CatManager, pixel_counts: dict[int, int] | None = None
    ) -> Self:
        code_var.set(code)
        if pixel_counts is not None:
            # cat ids are keys, hence no race conditions
            pixel_counts_var.set(pixel_counts)
        filename = f"{code}.jpg"
        try:
            box = (cache_fn := mgr.cache / filename).read_bytes()
            atomic_print(
                f"🛈 Pulled the Schroedinger cat in danger called {filename} from the cache "
                "to not make Schroedinger angry\n",
            )
        except FileNotFoundError:  # the cat contents weren't found in our cache
            box_room = httpx.get(cls._url_template.format(filename))
            try:
                box_room.raise_for_status()
            except httpx.HTTPStatusError as status_err:
                raise status_err from None
            box = box_room.read()  # find the box in the room
            cache_fn.write_bytes(box)
            atomic_print(
                f"🛈 Pulled the Schroedinger cat in danger called {filename} "
                "from the Internet and saved its contents in our cache\n",
            )

        image = imagelib.open(BytesIO(box))  # let's view our box cat as an image
        return cls(code, filename, image, mgr=mgr)

    @classmethod
    def fetch_or_none(
        cls, code: int, mgr: CatManager, pixel_counts: dict[int, int] | None = None
    ) -> Self:
        try:
            return cls.fetch(code=code, mgr=mgr, pixel_counts=pixel_counts)
        except httpx.HTTPStatusError as err:
            atomic_print(
                f"🛈 Error pulling the Schroedinger cat {code} from the Internet "
                f"(https://http.cat/status/{err.response.status_code})\n",
                file=sys.stderr,
            )
            return None

    def get_catful_frame(self) -> imagelib.Image:
        """Return the cropped image of the cat frame only with cat in it."""
        box = get_frame_vertices(
            self.image.size,
            self.image.load(),
            predicate=is_bright_enough,
        )
        return self.image.crop(box)

    def get_catless_frame(self) -> imagelib.Image:
        """Return the cropped image of the cat frame only without cat in it."""
        cat_frame = self.get_catful_frame()
        cat_frame_array = np.array(cat_frame.convert("RGBA"))
        height, width, _ = cat_frame_array.shape
        pixels = cat_frame.load()
        left, top, right, bottom = get_frame_vertices(
            (width, height),
            pixels,
            predicate=is_dark_enough,
        )
        cat_frame_array[top:bottom, left:right, :] = [0, 0, 0, 0]
        return imagelib.fromarray(cat_frame_array)

    def save(
        self, what: Literal["full", "frame", "emptyframe"], *, where: Path | None = None
    ) -> None:
        match what:
            case "full":
                image = self.image
            case "frame":
                image = self.get_catful_frame()
            case "emptyframe":
                image = self.get_catless_frame()
        image.save(where := where or self.shelter)
        atomic_print(
            f"✔ The cat named {self.filename} was saved! (In {where}, in its {what} form)\n"
        )


def get_frame_vertices(
    image_size: tuple[int, int],
    pixels: Any,
    predicate: Callable[[tuple[int, int, int]], bool],
) -> tuple[int, int, int, int]:
    """
    Find the vertices of the frame where the cat is trapped.

    Parameters
    ----------
    image_size
        Tuple containing the width and height of the image.
    pixels
        Pixel data of the image.
    predicate
        Predicate that tells which pixels signify frame edge.

    Returns
    -------
    tuple
        A tuple (left, top, right, bottom) representing the boundary indices.
    """
    axes = [image_size[1] // 2, 0]  # y, x
    # convenient, chainable structure: #0->(left, top), #1->(right, low)
    vertices: tuple[list[int], list[int]] = ([], [])
    pixel_count = axis = 0

    for axis, other_axis_value in enumerate(axes):
        other_axis = (axis + 1) % 2
        dim = image_size[axis]

        for dist in range(dim):
            # key: #0, #1
            n_filled = 0
            # we check both lhs and rhs 'at the same time'
            for key, axis_value in enumerate((dist, dim - dist - 1)):
                # only feed vertices one item per list for every axis
                n_filled += (filled := len(vertices[key]) > axis)
                if filled:
                    if key == 1:
                        break
                    continue
                pixel_count += 1
                if predicate(
                    pixels[
                        (axis_value, other_axis_value)
                        if axis < other_axis
                        else (other_axis_value, axis_value)
                    ]
                ):
                    vertices[key].insert(axis, axis_value + key)
                    axes[other_axis] = axis_value
            if n_filled == 2:
                break

    with suppress(LookupError):
        get_pixel_counts()[get_code()] = pixel_count
    return cast("tuple[int, int, int, int]", tuple(chain.from_iterable(vertices)))


def save_cats(where: Callable[[Cat], Path] | None = None) -> None:
    pixel_counts: dict[int, int] = {}
    mgr = CatManager()

    with ThreadPoolExecutor(
        max_workers=8,
        thread_name_prefix="cat-saving-thread-",
    ) as executor:
        cat_generator = filter(
            None,
            executor.map(
                partial(
                    Cat.fetch_or_none,
                    mgr=mgr,
                    pixel_counts=pixel_counts,
                ),
                map(int, http_responses),
            ),
        )
        first_cat = next(cat_generator)
        executor.submit(
            first_cat.context.run,
            first_cat.save,
            what="emptyframe",
            where=mgr.shelter / "frame.png",
        ).result()
        executor.map(
            next,
            (
                cat.context.run(
                    cat.save,
                    what="frame",
                    where=(where or attrgetter("shelter"))(cat),
                )
                for cat in chain([first_cat], cat_generator)
            ),
        )


def hashed_fn(cat: Cat) -> Path:
    return (
        cat.mgr.shelter
        / f"{md5(str(cat.code).encode(), usedforsecurity=False).hexdigest()}.jpg"
    )


if __name__ == "__main__":
    os.makedirs(CAT_DIR, exist_ok=True)
    os.makedirs(CACHE_DIR, exist_ok=True)
    save_cats(where=hashed_fn if "--hashed" in sys.argv else None)
