import pandas as pd
import logging
from pathlib import Path
from datetime import datetime
from config.employee_config import CONFIG

# LOGGING
def setup_logging():
    log_folder = Path("logs")
    log_folder.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_folder / f"pipeline_{timestamp}.log"
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s"
    )
    logging.info("Logging initialized")
    return log_file

# LOAD DATA
def load_data(file_path):
    logging.info(f"Loading file: {file_path}")
    file_extension = Path(file_path).suffix.lower()
    if file_extension == ".xlsx":
        df = pd.read_excel(file_path)

    elif file_extension == ".csv":
        df = pd.read_csv(file_path)

    else:
        raise ValueError(
            f"Unsupported file type: {file_extension}"
        )

    logging.info(
        f"Dataset loaded successfully. "
        f"Rows={len(df)} "
        f"Columns={len(df.columns)}"
    )
    return df

# DROP COLUMNS
def drop_columns(df, columns):

    existing_columns = [
        col for col in columns
        if col in df.columns
    ]

    if not existing_columns:
        logging.info(
            "No columns found for removal"
        )
        return df

    df = df.drop(columns=existing_columns)

    logging.info(
        f"Removed columns: {existing_columns}"
    )
    return df

# APPLY VALUE MAPPINGS
def apply_mappings(df, mappings):
    for column, mapping in mappings.items():
        if column not in df.columns:
            logging.warning(
                f"Column not found for mapping: {column}"
            )
            continue

        before_unique = df[column].nunique(
            dropna=False
        )
        df[column] = df[column].replace(mapping)
        after_unique = df[column].nunique(
            dropna=False
        )

        logging.info(
            f"Mapping applied to '{column}'. "
            f"Unique values: "
            f"{before_unique} -> {after_unique}"
        )

    return df

# STANDARDIZE DATA TYPES
def standardize_data_types(df, data_types):

    logging.info(
        "Starting datatype standardization"
    )

    for column, dtype in data_types.items():
        if column not in df.columns:
            logging.warning(
                f"Column not found: {column}"
            )
            continue
        try:
            if dtype == "datetime":
                df[column] = pd.to_datetime(
                    df[column],
                    errors="coerce",
                    format= "%Y-%m-%d"
                )
            elif dtype == "Int64":
                df[column] = pd.to_numeric(
                    df[column],
                    errors="coerce"
                ).astype("Int64")

            elif dtype == "float64":
                df[column] = pd.to_numeric(
                    df[column],
                    errors="coerce"
                ).astype("float64")

            elif dtype == "string":
                df[column] = (
                    df[column]
                    .astype("string")
                    .str.strip()
                )
            else:
                logging.warning(
                    f"Unsupported datatype "
                    f"'{dtype}' for '{column}'"
                )
                continue

            logging.info(
                f"Converted '{column}' to {dtype}"
            )

        except Exception as e:
            logging.error(
                f"Failed converting "
                f"'{column}' to {dtype}. "
                f"Error: {e}"
            )

    return df

# REMOVE DUPLICATES
def remove_duplicates(df):
    df['Date of Hire'] = df.groupby('Employee ID')['Date of Hire'].transform('first')
    before_count = len(df)
    df = df.drop_duplicates()
    removed_count = (
        before_count - len(df)
    )
    logging.info(
        f"Removed {removed_count} duplicate rows"
    )
    return df

# DATA QUALITY CHECKS
def data_quality_checks(df):
    logging.info(
        "Starting quality checks"
    )
    missing_summary = (
        df.isna()
          .sum()
          .sort_values(
              ascending=False
          )
    )
    for column, missing_count in missing_summary.items():
        if missing_count > 0:
            logging.warning(
                f"Column '{column}' contains "
                f"{missing_count} null values"
            )
    logging.info(
        "Quality checks completed"
    )
    return df

# SAVE OUTPUT
def save_output(df, output_file):
    output_path = Path(output_file)
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )
    df.to_csv(
        output_file,
        index=False
    )
    logging.info(
        f"Output saved: {output_file}"
    )

# MAIN
def main():
    setup_logging()
    logging.info(
        "========== PIPELINE STARTED =========="
    )
    try:
        df = load_data(
            CONFIG["input_file"]
        )

        df = drop_columns(
            df,
            CONFIG.get("drop_columns", [])
        )

        df = apply_mappings(
            df,
            CONFIG.get("mappings",{})
        )

        df = standardize_data_types(
            df,
            CONFIG.get("data_types",{})
        )

        if CONFIG.get("remove_duplicates",False):
            df = remove_duplicates(df)

        df = data_quality_checks(df)

        save_output(
            df,
            CONFIG["output_file"]
        )

        logging.info(
            "========== PIPELINE COMPLETED SUCCESSFULLY =========="
        )

    except Exception as e:

        logging.exception(
            f"Pipeline failed: {e}"
        )

if __name__ == "__main__":
    main()