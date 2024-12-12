#!/usr/bin/env -S uv run --python 3.13t

# jokes aside, this module downloads cats from images at http.cat,
# crops them to only save the cat images in their frames
# (without the titles & subtitles under those frames)
# so that they can be used to later display cats in the http.cat game

# btw, i have no idea how to benchmark this
# if you have one, DM me on Discord: @bswck

# /// script
# requires-python = ">=3.13"
# dependencies = ["httpx", "pillow"]
# ///

import os
from collections.abc import Callable, Iterable
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from contextvars import ContextVar
from functools import partial
from http.client import responses
from io import BytesIO
from itertools import chain
from pathlib import Path
from typing import Any

import httpx
from PIL import Image as imagelib

CACHE_DIR = Path(".boxed-cats/")
CAT_DIR = Path("cats/")
INTERNET_CAT_URL_TEMPLATE = "https://http.cat/{}"

pixel_counts_var: ContextVar[dict[int, int]] = ContextVar("pixel_counts")
cat_id_var: ContextVar[int] = ContextVar("cat_id")

# early bindings
get_pixel_tracker = pixel_counts_var.get
get_cat_id = cat_id_var.get

consume: Callable[[Iterable[Any]], Any] = partial(deque, maxlen=0)

is_bright_enough = (100, 100, 100).__lt__


def get_schroedinger_cat_box(
    cat_name: str,
    *,
    cache_dir: Path = CACHE_DIR,
) -> imagelib.Image:
    """Check if we have our boxed cat in the cache or download it from the Internet."""
    try:
        box = (cache_fn := cache_dir / cat_name).read_bytes()
        print(
            f"🛈 Pulled the Schroedinger cat in danger called {cat_name} from the cache "
            "to not make Schroedinger angry\n",
            end="",
        )
    except FileNotFoundError:  # the cat contents weren't found in our cache
        box_room = httpx.get(INTERNET_CAT_URL_TEMPLATE.format(cat_name))
        box = box_room.read()  # find the box in the room
        cache_fn.write_bytes(box)
        print(
            f"🛈 Pulled the Schroedinger cat in danger called {cat_name} "
            "from the Internet and saved its contents in our cache\n",
            end="",
        )
    return imagelib.open(BytesIO(box))  # let's view our box cat as an image


def get_box_vertices(image_size: tuple[int, int], pixels: Any) -> tuple[int, ...]:
    """Find the vertices of the box where the cat is trapped."""
    axes = [image_size[1] // 2, 0]  # y, x
    vertices: tuple[list[int], list[int]] = (
        [],
        [],
    )  # convenient, chainable structure: #0->(left, top), #1->(right, low)
    pixel_tracker = axis = 0

    for axis, other_axis_value in enumerate(axes):
        other_axis = (axis + 1) % 2
        dim = image_size[axis]

        # we check both lhs and rhs 'at the same time'
        for dist in range(dim):
            # key: #0, #1
            n_filled = 0
            for key, axis_value in enumerate((dist, dim - dist - 1)):
                # only feed vertices one item per list for every axis
                n_filled += (filled := len(vertices[key]) > axis)
                if filled:
                    if key == 1:
                        break
                    continue
                pixel_tracker += 1
                if is_bright_enough(
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

    get_pixel_tracker()[get_cat_id()] = pixel_tracker
    return tuple(chain.from_iterable(vertices))


def unbox_schroedinger_cat(image: imagelib.Image) -> imagelib.Image:
    """Unbox the cat (50% chance of survival)."""
    return image.crop(get_box_vertices(image.size, image.load()))  # type: ignore[arg-type]


def save_cat(
    cat_id: int,
    *,
    cache_dir: Path = CACHE_DIR,
    dest_dir: Path = CAT_DIR,
    pixel_counts: dict[int, int] | None = None,
) -> None:
    # unique for every thread
    cat_id_var.set(cat_id)
    cat_name = f"{cat_id}.jpg"

    if pixel_counts is not None:
        # cat ids are keys, hence no race conditions
        pixel_counts_var.set(pixel_counts)

    shelter = dest_dir / cat_name
    print(f"🛈 Downloading a cat named {cat_name} to {shelter}\n", end="")

    box = get_schroedinger_cat_box(cat_name, cache_dir=cache_dir)
    cat = unbox_schroedinger_cat(box)

    # ↓ here we're saving the cat!
    cat.save(shelter)  # type: ignore[arg-type]  # this is correct, shelter *should match* PathLike[str]
    print(f"✔ The cat named {cat_name} was saved! (In {shelter})\n", end="")


def save_cats() -> None:
    pixel_counts: dict[int, int] = {}

    with ThreadPoolExecutor(
        max_workers=8,
        thread_name_prefix="cat-saving-thread-",
    ) as executor:
        consume(
            executor.map(
                partial(save_cat, pixel_counts=pixel_counts), map(int, responses)
            )
        )


if __name__ == "__main__":
    os.makedirs(CAT_DIR, exist_ok=True)
    os.makedirs(CACHE_DIR, exist_ok=True)
    save_cats()
