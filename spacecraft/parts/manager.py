import random


class PartsManager:
    def __init__(self):
        self.__parts: dict[str, "BasePart"] = dict()

    def get(self, part_id: str) -> "BasePart | None":
        part = self.__parts.get(part_id, None)
        if part is not None:
            return part
        else:
            raise KeyError(f"the part with ID={part_id} does not exist")

    def get_all(self) -> set["BasePart"]:
        return set(self.__parts.values())

    @staticmethod
    def __generate_random_part_id() -> str:
        # generate random 2 byte number
        rand_number: int = random.randint(0, 2 ** 16 - 1)

        # convert to hex string with two digits
        rand_hex: str = "{:04x}".format(rand_number)
        return rand_hex

    def __generate_unique_part_id(self):
        # generate part IDs until a unique one is found
        while (part_id := self.__generate_random_part_id()) in self.__parts:
            pass
        return part_id

    def add(self, part: "BasePart"):
        # assign part id
        part._part_id = self.__generate_unique_part_id()

        # add part
        self.__parts[part.part_id] = part
