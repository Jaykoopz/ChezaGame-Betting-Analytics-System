from scripts.logger import ParserLogger
import re
from pathlib import Path
import pandas as pd
from scripts.models import Bet, Selection


class SlipParser:

    def __init__(self):
        self.folder = Path("data/processed")
        self.logger = ParserLogger()

    # ==========================================
    # MAIN PARSER
    # ==========================================
    def parse(self):

        files = sorted(self.folder.glob("*.txt"))

        bets = []
        selections = []

        parsed = 0
        failed = 0

        print(f"Processing {len(files)} OCR files...\n")

        for file in files:

            text = file.read_text(
                encoding="utf-8",
                errors="ignore"
            )

            text = self.clean_text(text)

            lines = [
                line.strip()
                for line in text.split("\n")
                if line.strip()
            ]

            # -------------------------
            # OCR QUALITY CHECK
            # -------------------------
            keywords = [
                "Stake",
                "Bet",
                "Odds",
                "Won",
                "Lost",
                "Cancelled"
            ]

            found = any(word in text for word in keywords)

            if len(lines) < 5 or not found:

                print(f"Skipping {file.name}")

                self.logger.log(
                    file.name,
                    "Poor OCR",
                    text
                )

                failed += 1
                continue

            bet = self.parse_bet(lines)

            if (
                bet.bet_id == ""
                or bet.stake == 0
            ):

                self.logger.log(
                    file.name,
                    "Incomplete bet detected",
                    text
                )

                failed += 1

            else:
                parsed += 1

            bets.append(vars(bet))

            selections.extend(
                self.parse_selections(
                    lines,
                    bet.bet_id
                )
            )

        print("\n========== PARSER REPORT ==========")
        print(f"Successfully Parsed : {parsed}")
        print(f"Needs Review        : {failed}")
        print("===================================\n")

        return (
            pd.DataFrame(bets),
            pd.DataFrame(selections)
        )

    # ==========================================
    # CLEAN OCR TEXT
    # ==========================================
    def clean_text(self, text):

        text = text.replace("®", "")
        text = text.replace("|", " ")
        text = text.replace("—", "-")

        while "  " in text:
            text = text.replace("  ", " ")

        return text

    # ==========================================
    # PARSE BET INFORMATION
    # ==========================================
    def parse_bet(self, lines):

        bet = Bet()

        for i, line in enumerate(lines):

            line = line.strip()

            # --------------------------
            # BET ID (OCR tolerant)
            # --------------------------
            if "Bet" in line:

                digits = re.findall(r"\d+", line)

                if digits:

                    betid = "".join(digits)

                    if len(betid) >= 12:
                        bet.bet_id = betid

            # --------------------------
            # DATE
            # --------------------------
            date = re.search(
                r"\d{2}[/-]\d{2}[/-]\d{4}",
                line
            )

            if date:
                bet.date = date.group()

            # --------------------------
            # STAKE
            # --------------------------
            elif "Stake" in line:

                bet.stake = self.extract_number(line)

            # --------------------------
            # TOTAL ODDS
            # --------------------------
            elif (
                "Tot Odds" in line
                or "Total Odds" in line
            ):

                bet.total_odds = self.extract_number(line)

            # --------------------------
            # CANCELLED BET
            # --------------------------
            elif "Cancelled" in line:

                bet.result = "Cancelled"
                bet.returns = bet.stake

            # --------------------------
            # WON BET
            # --------------------------
            elif re.search(r"\bWon\b", line):

                bet.result = "Won"

                payout = 0

                for j in range(
                    i,
                    min(i + 6, len(lines))
                ):

                    nums = re.findall(
                        r"\d[\d,]*\.?\d*",
                        lines[j]
                    )

                    if nums:

                        value = float(
                            nums[-1].replace(",", "")
                        )

                        if value > bet.stake:

                            payout = value
                            break

                bet.returns = payout

            # --------------------------
            # LOST BET
            # --------------------------
            elif re.search(r"\bLost\b", line):

                bet.result = "Lost"
                bet.returns = 0

            # --------------------------
            # NUMBER OF SELECTIONS
            # --------------------------
            elif "selection" in line.lower():

                m = re.search(r"\d+", line)

                if m:
                    bet.selections = int(m.group())

        bet.profit = bet.returns - bet.stake

        print("\n--------------------------------")
        print("BET PARSED")
        print(vars(bet))
        print("--------------------------------")

        return bet
        # ==========================================
    # PARSE INDIVIDUAL SELECTIONS
    # ==========================================
    def parse_selections(self, lines, bet_id):

        selections = []

        current_match = ""

        for line in lines:

            line = line.strip()

            # --------------------------
            # MATCH NAME
            # --------------------------
            if " - " in line:

                current_match = line

            # --------------------------
            # PICK
            # --------------------------
            if "Pick:" in line:

                parts = line.split("Pick:")

                market = parts[0].strip()

                outcome = ""

                if len(parts) > 1:
                    outcome = parts[1].strip()

                selections.append({

                    "Bet ID": bet_id,
                    "Match": current_match,
                    "Market": market,
                    "Outcome": outcome

                })

        return selections

    # ==========================================
    # NUMBER EXTRACTION
    # ==========================================
    def extract_number(self, text):

        nums = re.findall(r"\d[\d,]*\.?\d*", text)

        if not nums:
            return 0.0

        values = []

        for n in nums:

            try:
                values.append(
                    float(
                        n.replace(",", "")
                    )
                )

            except ValueError:
                pass

        if not values:
            return 0.0

        return max(values)

    # ==========================================
    # OCR HELPER
    # Attempts to recover badly-read Bet IDs
    # ==========================================
    def recover_bet_id(self, text):

        patterns = [
            r"Bet\s*ID[:\s]*([\d\s]{12,})",
            r"Bet\s*D[:\s]*([\d\s]{12,})",
            r"Bet\s*1D[:\s]*([\d\s]{12,})",
            r"Bet\s*0[:\s]*([\d\s]{12,})"
        ]

        for pattern in patterns:

            m = re.search(
                pattern,
                text,
                re.IGNORECASE
            )

            if m:

                digits = re.sub(
                    r"\D",
                    "",
                    m.group(1)
                )

                if len(digits) >= 12:
                    return digits

        return ""

    # ==========================================
    # OCR HELPER
    # Detect cancelled bets
    # ==========================================
    def is_cancelled(self, text):

        return "Cancelled" in text

    # ==========================================
    # OCR HELPER
    # Detect OCR quality
    # ==========================================
    def has_required_keywords(self, text):

        keywords = [

            "Stake",
            "Bet",
            "Odds",
            "Won",
            "Lost",
            "Cancelled"

        ]

        return any(
            word in text
            for word in keywords
        )