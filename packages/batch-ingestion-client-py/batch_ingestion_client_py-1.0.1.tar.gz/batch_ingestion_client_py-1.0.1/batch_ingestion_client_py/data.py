from typing import List, Dict, Literal, Any


class ValueInLanguage:
    TYPE = Dict[str, str]

    def __init__(
        self,
        language: str,
        value: str,
    ):
        self.language = language
        self.value = value

    def serialize(self):
        return {
            "language": self.language,
            "value": self.value,
        }

    @staticmethod
    def parse(data: TYPE):
        return ValueInLanguage(
            language=data["language"],
            value=data["value"],
        )

    def __repr__(self) -> str:
        return self.serialize().__repr__()


class DataValue:
    TYPE = Dict[str, str]

    def __init__(
        self,
        value: str,
        type: str,
    ):
        self.value = value
        self.type = type

    def serialize(self):
        return {
            "value": self.value,
            "type": self.type,
        }

    @staticmethod
    def parse(data: TYPE):
        return DataValue(
            value=data["value"],
            type=data["type"],
        )

    def __repr__(self) -> str:
        return self.serialize().__repr__()


class MainSnak:
    TYPE = Dict[str, str | DataValue.TYPE]

    def __init__(
        self,
        snaktype: str,
        property: str,
        datatype: str,
        datavalue: DataValue,
    ):
        self.snaktype = snaktype
        self.property = property
        self.datatype = datatype
        self.datavalue = datavalue

    def serialize(self):
        return {
            "snaktype": self.snaktype,
            "property": self.property,
            "datatype": self.datatype,
            "datavalue": self.datavalue.serialize(),
        }

    @staticmethod
    def parse(data: TYPE):
        return MainSnak(
            snaktype=data["snaktype"],  # type: ignore
            property=data["property"],  # type: ignore
            datatype=data["datatype"],  # type: ignore
            datavalue=DataValue.parse(data["datavalue"]),  # type: ignore
        )

    def __repr__(self) -> str:
        return self.serialize().__repr__()


class Claim:
    TYPE = Dict[str, str | MainSnak.TYPE]

    def __init__(
        self,
        mainsnak: MainSnak,
        type: str,
        rank: str,
    ):
        self.mainsnak = mainsnak
        self.type = type
        self.rank = rank

    def serialize(self):
        return {
            "mainsnak": self.mainsnak.serialize(),
            "type": self.type,
            "rank": self.rank,
        }

    @staticmethod
    def parse(data: TYPE):
        return Claim(
            mainsnak=MainSnak.parse(data["mainsnak"]),  # type: ignore
            type=data["type"],  # type: ignore
            rank=data["rank"],  # type: ignore
        )

    def __repr__(self) -> str:
        return self.serialize().__repr__()


class Entity:
    TYPE = Dict[str, str | List[Claim.TYPE] | Dict[str, ValueInLanguage.TYPE]]

    def __init__(
        self,
        id: str,
        mode: Literal["add", "remove"] | None = None,
        type: str = "item",
        labels: Dict[str, ValueInLanguage] | None = None,
        descriptions: Dict[str, ValueInLanguage] | None = None,
        claims: Dict[str, List[Claim]] | None = None,
    ):
        self.id = id
        self.mode = mode
        self.type = type
        self.labels = labels
        self.descriptions = descriptions
        self.claims = claims

    def serialize(self):
        e = {
            "id": self.id,
            "mode": self.mode,
            "type": self.type,
        }
        if self.labels is not None:
            e["labels"] = {
                key: value.serialize()
                for key, value in self.labels.items()
            }
        if self.descriptions is not None:
            e["descriptions"] = {
                key: value.serialize()
                for key, value in self.descriptions.items()
            }
        if self.claims is not None:
            e["claims"] = {
                key: [claim.serialize() for claim in value]
                for key, value in self.claims.items()
            }
        return e

    @staticmethod
    def parse(data: TYPE):
        return Entity(
            id=data["id"],  # type: ignore
            mode=data["mode"],  # type: ignore
            type=data["type"],  # type: ignore
            labels={
                key: ValueInLanguage.parse(value)
                for key, value in data["labels"].items()  # type: ignore
            } if "labels" in data else None,
            descriptions={
                key: ValueInLanguage.parse(value)
                for key, value in data["descriptions"].items()  # type: ignore
            } if "descriptions" in data else None,
            claims={
                key: [Claim.parse(claim) for claim in value]  # type: ignore
                for key, value in data["claims"].items()  # type: ignore
            } if "claims" in data else None,
        )

    def __repr__(self) -> str:
        return self.serialize().__repr__()


class Data:
    TYPE = Dict[str, str | List[Entity.TYPE | Any]]

    def __init__(
        self,
        key: str,
        entities: List[Entity],
    ):
        self.key = key
        self.entities = entities

    def serialize(self):
        return {
            "key": self.key,
            "entities": [
                entity.serialize()
                for entity in self.entities
            ],
        }

    @staticmethod
    def parse(data: TYPE):
        return Data(
            key=data["key"],  # type: ignore
            entities=[
                Entity.parse(entity)  # type: ignore
                for entity in data["entities"]  # type: ignore
            ],
        )

    def __repr__(self) -> str:
        return self.serialize().__repr__()
