from random import randint, uniform, getrandbits, seed
from typing import Tuple, Callable
import sys
from string import ascii_uppercase, ascii_lowercase, digits
import datetime


def random_int(**kwargs) -> int:
    return randint(-sys.maxsize, sys.maxsize)


def random_string(**kwargs) -> str:
    STRING_CHARS = ascii_uppercase + ascii_lowercase + digits
    return "".join(
        STRING_CHARS[randint(0, len(STRING_CHARS) - 1)] for _ in range(randint(0, 10))
    )


def random_float(**kwargs) -> float:
    return uniform(-sys.maxsize, sys.maxsize)


def random_bool(**kwargs) -> bool:
    return bool(getrandbits(1))


def random_none(**kwargs) -> None:
    return None


def random_datetime(**kwargs) -> datetime.time:
    return datetime.time(
        hour=randint(0, 23),
        minute=randint(0, 59),
        second=randint(0, 59),
        microsecond=randint(0, 999999),
    )


def random_dict(
    max_height, max_depth, key_generators, val_generators, nested_generators, **kwargs
):
    non_nested_generators = tuple(set(val_generators) - set(nested_generators))

    if max_depth <= 1:
        val_generators = non_nested_generators

    return generate(
        max_height=max_height,
        max_depth=max_depth - 1,
        key_generators=key_generators,
        val_generators=val_generators,
        nested_generators=nested_generators,
    )


def random_array(
    max_height, max_depth, key_generators, val_generators, nested_generators, **kwargs
):
    all_generators = val_generators + nested_generators
    # Create a random list of generators
    generators = []
    for i in range(randint(0, max_height)):
        # If we are at a top level depth don't allow any nested generators
        if max_depth > 2:
            generators.append(all_generators[randint(0, len(all_generators) - 1)])
        else:
            generators.append(val_generators[randint(0, len(val_generators) - 1)])

    result = []
    for generator in generators:
        result.append(
            generator(
                max_height=max_height,
                max_depth=max_depth - 1,
                key_generators=key_generators,
                val_generators=val_generators,
                nested_generators=nested_generators,
            )
        )

    return result


def generate(
    max_height: int = 3,
    max_depth: int = 3,
    rand_seed: int = None,
    key_generators: Tuple[Callable] = (random_string,),
    val_generators: Tuple[Callable] = (
        random_int,
        random_string,
        random_float,
    ),
    nested_generators: Tuple[Callable] = (random_dict, random_array),
):
    """
    Generate a random dictionary.

    :param max_height: Maximum number of keys at a level in the dictionary
    :param max_depth: Maximum depth of generated dictionary
    """

    # Validation Logic
    if max_height < 1 or max_depth < 1:
        raise AttributeError("max_height and max_depth must be greater than 0")

    if rand_seed:
        seed(rand_seed)

    # Create a random list of generators
    if max_depth > 1:
        all_generators = val_generators + nested_generators
    else:
        all_generators = val_generators
    generator_tuples = []
    for i in range(randint(0, max_height)):
        generator_tuples.append(
            (
                key_generators[randint(0, len(key_generators) - 1)],
                all_generators[randint(0, len(all_generators) - 1)],
            )
        )

    result = {}
    for key_gen, val_gen in generator_tuples:
        if max_depth > 1:
            new_val = val_gen(
                max_height=max_height,
                max_depth=max_depth,
                key_generators=key_generators,
                val_generators=val_generators,
                nested_generators=nested_generators,
            )
        else:
            new_val = val_gen()
        result[key_gen()] = new_val

    return result
