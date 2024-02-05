import random
import hashlib

from spacecraft.parts.base import BasePart, BaseController


class PartsManager:
    def __init__(self):
        self.__parts: dict[str, BasePart] = dict()

    def get(self, part_id: str) -> BasePart | None:
        return self.__parts.get(part_id, None)

    def get_all(self) -> set[BasePart]:
        return set(self.__parts.values())

    def get_controllers(self) -> set[BaseController]:
        return set(filter(lambda x: isinstance(x, BaseController), self.__parts.values()))

    @staticmethod
    def __generate_random_part_id() -> str:
        # generate random 2 byte number
        rand_number: int = random.randint(0, 2 ** 16 - 1)

        # convert to hex string with two digits
        rand_hex: str = "{:04x}".format(rand_number)
        return rand_hex

    def __generate_random_unique_part_id(self):
        # generate part IDs until a unique one is found
        while (part_id := self.__generate_random_part_id()) in self.__parts:
            pass
        return part_id

    @staticmethod
    def __generate_hash_based_id(part: BasePart, x: int):
        return hashlib.sha1(
            f"{part.name}{x}".encode("utf-8"),
            usedforsecurity=False
        ).hexdigest()[:4]

    def __generate_unique_hash_based_id(self, part: BasePart) -> str:
        x: int = 0
        while (part_id := self.__generate_hash_based_id(part, x)) in self.__parts:
            x += 1
        return part_id

    def add(self, part: BasePart):
        # assign part id
        part._part_id = self.__generate_unique_hash_based_id(part)

        # add part
        self.__parts[part.part_id] = part

    def add_many(self, parts: list[BasePart]) -> None:
        for part in parts:
            self.add(part)
