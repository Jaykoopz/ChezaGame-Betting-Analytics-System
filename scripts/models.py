from dataclasses import dataclass


@dataclass
class Bet:

    bet_id: str = ""

    date: str = ""

    stake: float = 0.0

    total_odds: float = 0.0

    returns: float = 0.0

    profit: float = 0.0

    result: str = "Unknown"

    selections: int = 0


@dataclass
class Selection:

    bet_id: str = ""

    match: str = ""

    market: str = ""

    outcome: str = ""

    odds: float = 0.0

    result: str = ""