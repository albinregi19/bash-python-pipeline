import pandas as pd
import json
import logging
import os

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

# Configure logging
logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("Pipeline Started")

try:
    # Read CSV
    df = pd.read_csv("data/iris.csv")
    logging.info("CSV file loaded successfully.")

    # Total records before cleaning
    total_records = len(df)

    # Remove duplicate rows
    duplicates_removed = total_records - len(df.drop_duplicates())
    df = df.drop_duplicates()

    # Remove rows with missing values
    missing_rows = df.isnull().any(axis=1).sum()
    df = df.dropna()

    # Save cleaned CSV
    os.makedirs("output", exist_ok=True)
    df.to_csv("output/cleaned.csv", index=False)

    # Create summary
    summary = {
        "total_records": total_records,
        "records_after_cleaning": len(df),
        "duplicates_removed": duplicates_removed,
        "rows_with_missing_values": int(missing_rows),
        "species_count": df.iloc[:, -1].value_counts().to_dict()
    }

    # Save JSON summary
    with open("output/summary.json", "w") as json_file:
        json.dump(summary, json_file, indent=4)

    logging.info("Summary JSON created.")
    logging.info("Cleaned CSV created.")
    logging.info("Pipeline completed successfully.")

    print("Pipeline completed successfully.")

except FileNotFoundError:
    logging.error("CSV file not found.")
    print("Error: iris.csv not found.")

except Exception as e:
    logging.error(f"Unexpected Error: {e}")
    print(f"Error: {e}")