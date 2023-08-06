from typing import List, Dict


class Revision:
    def __init__(
        self,
        revision: int,
        id: str,
    ):
        self.revision = revision
        self.id = id

    def serialize(self):
        return {
            "revision": self.revision,
            "id": self.id,
        }

    @staticmethod
    def parse(data: Dict[str, str | int]):
        return Revision(
            revision=data["revision"],  # type: ignore
            id=data["id"],  # type: ignore
        )

    def __repr__(self) -> str:
        return self.serialize().__repr__()


class Response:
    def __init__(
        self,
        count: int,
        successes: int,
        response: List[Revision],
    ):
        self.count = count
        self.successes = successes
        self.response = response

    def serialize(self):
        return {
            "count": self.count,
            "successes": self.successes,
            "response": [r.serialize() for r in self.response],
        }

    @staticmethod
    def parse(data: Dict[str, int | List[Dict[str, str | int]]]):
        return Response(
            count=data["count"],  # type: ignore
            successes=data["successes"],  # type: ignore
            response=[
                Revision.parse(r)
                for r in data["response"]  # type: ignore
            ],
        )

    def __repr__(self) -> str:
        return self.serialize().__repr__()
