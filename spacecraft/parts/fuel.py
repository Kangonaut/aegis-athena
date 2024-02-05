from spacecraft.parts.tank import BaseTank


class FuelTank(BaseTank):
    def __init__(self, name: str, capacity: float, fill_level: float, contents: str, contents_abbreviation: str | None):
        super().__init__(
            name=name,
            capacity=capacity,
            fill_level=fill_level,
            contents=contents,
            contents_abbreviation=contents_abbreviation
        )


class OxidizerTank(BaseTank):
    def __init__(self, name: str, capacity: float, fill_level: float, contents: str, contents_abbreviation: str | None):
        super().__init__(
            name=name,
            capacity=capacity,
            fill_level=fill_level,
            contents=contents,
            contents_abbreviation=contents_abbreviation
        )


class Lh2Tank(FuelTank):
    def __init__(self, name: str, capacity: float, fill_level: float):
        super().__init__(
            name=name,
            capacity=capacity,
            fill_level=fill_level,
            contents="liquid hydrogen",
            contents_abbreviation="LH2",
        )


class AerozineTank(FuelTank):
    def __init__(self, name: str, capacity: float, fill_level: float):
        super().__init__(
            name=name,
            capacity=capacity,
            fill_level=fill_level,
            contents="Aerozine 50",
            contents_abbreviation=None,
        )


class LoxTank(OxidizerTank):
    def __init__(self, name: str, capacity: float, fill_level: float):
        super().__init__(
            name=name,
            capacity=capacity,
            fill_level=fill_level,
            contents="liquid oxygen",
            contents_abbreviation="LOX",
        )


class N2o4Tank(OxidizerTank):
    def __init__(self, name: str, capacity: float, fill_level: float):
        super().__init__(
            name=name,
            capacity=capacity,
            fill_level=fill_level,
            contents="nitrogen tetroxide",
            contents_abbreviation="N2O4",
        )


class Ln2Tank(BaseTank):
    def __init__(self, name: str, capacity: float, fill_level: float):
        super().__init__(
            name=name,
            capacity=capacity,
            fill_level=fill_level,
            contents="liquid nitrogen",
            contents_abbreviation="LN2",
        )
