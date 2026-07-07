from scripts.ocr_parser import OCRParser
from scripts.slip_parser import SlipParser
from scripts.database_builder import DatabaseBuilder
from scripts.analytics import Analytics

from scripts.betting_intelligence import BettingIntelligence
from scripts.pattern_detector import PatternDetector
from scripts.report_generator import ReportGenerator

print("=" * 60)
print("CHEZAGAME BETTING ANALYTICS SYSTEM")
print("Version 1.2")
print("=" * 60)

# STEP 1 - OCR
print("\nSTEP 1 - OCR Processing")
ocr = OCRParser()
ocr.process_images()

# STEP 2 - PARSE
print("\nSTEP 2 - Parsing OCR Text")
parser = SlipParser()

bets_df, selections_df = parser.parse()
print("\nBETS DATAFRAME")
print(bets_df.head())

print("\nCOLUMNS")
print(bets_df.columns.tolist())
print("\nBETS DATAFRAME COLUMNS")
print(bets_df.columns.tolist())

# STEP 3 - DATABASE
print("\nSTEP 3 - Building Database")
builder = DatabaseBuilder()
builder.save(bets_df, selections_df)

# STEP 4 - ANALYTICS
print("\nSTEP 4 - Analytics")

analytics = Analytics(bets_df, selections_df)

summary = analytics.summary()

print("\n========== SUMMARY ==========\n")

for k, v in summary.items():
    print(f"{k:<20}: {v}")

print("\n========== INSIGHTS ==========\n")

for i in analytics.insights():
    print(f"[{i['type'].upper()}] {i['message']}")

print("\nSTEP 5 - Betting Intelligence")

brain = BettingIntelligence(
    bets_df,
    selections_df
)

report = brain.run()

print("\n===== INTELLIGENCE REPORT =====\n")

for item in report:
    print("•", item)

# ----------------------------------
# STEP 6
# ----------------------------------

print("\nSTEP 6 - Pattern Detection")

patterns = PatternDetector(
    bets_df,
    selections_df
)

patterns.report()

print("\nSTEP 6 - Report Generation")

generator = ReportGenerator()

# Build the report text
full_report = "\n".join(report)

# Save it
generator.save(full_report)

print("\nCBAS completed successfully!")