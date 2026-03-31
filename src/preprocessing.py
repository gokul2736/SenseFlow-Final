import os
import re
import warnings

import pandas as pd

warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")


# --------------------------------------------
# TEXT CLEANING FUNCTION (USED BY APP)
# --------------------------------------------
def clean_text(text):

    if not isinstance(text, str):
        return ""

    text = text.lower()

    text = re.sub(r"<.*?>", "", text)
    text = re.sub(r"https?://\S+|www\.\S+", "", text)

    text = re.sub(r"[^a-zA-Z0-9\s.,!?]", "", text)

    text = re.sub(r"\s+", " ", text).strip()

    return text


# --------------------------------------------
# DATASET BUILD PIPELINE
# --------------------------------------------
def build_dynamic_data_lake():

    print("--- SenseFlow: Initiating Dynamic Data Lake Pipeline ---")

    dfs = []
    raw_dir = "data/raw/"

    if not os.path.exists(raw_dir):
        print(f"ERROR: Directory '{raw_dir}' not found.")
        return

    for file in os.listdir(raw_dir):

        path = os.path.join(raw_dir, file)

        try:
            if file.endswith(".csv"):
                df = pd.read_csv(path)

            elif file.endswith((".xls", ".xlsx")):
                df = pd.read_excel(path, engine="openpyxl")

            else:
                continue

            text_col = None
            label_col = None

            if "body" in df.columns:
                text_col = "body"
            elif "content" in df.columns:
                text_col = "content"
            elif "text" in df.columns:
                text_col = "text"

            if "label" in df.columns:
                label_col = "label"
            elif "Class" in df.columns:
                label_col = "Class"

            if text_col and label_col:

                temp_df = df[[text_col, label_col]].rename(
                    columns={text_col: "text", label_col: "label"}
                )

                dfs.append(temp_df)

                print(f"✅ Successfully ingested: {file}")

            else:

                print(f"⚠️ Skipped {file}: Missing text/label columns")

        except Exception as e:

            print(f"❌ Error loading {file}: {e}")

    if not dfs:
        print("CRITICAL ERROR: No valid data found to merge.")
        return

    print("\nMerging datasets and purging duplicates...")

    master_df = pd.concat(dfs, ignore_index=True).drop_duplicates().dropna()

    def sanitize_text(text):

        text = str(text).lower()

        text = re.sub(r"<.*?>", "", text)

        text = re.sub(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "[EMAIL]", text
        )

        text = re.sub(r"http\S+", "[URL]", text)

        text = re.sub(r"[^a-z0-9\s]", "", text)

        return text.strip()

    print(f"Sanitizing {len(master_df)} emails...")

    master_df["clean_text"] = master_df["text"].apply(sanitize_text)

    master_df["label"] = (
        pd.to_numeric(master_df["label"], errors="coerce").fillna(0).astype(int)
    )

    output_dir = "data/processed"
    os.makedirs(output_dir, exist_ok=True)

    output_path = "data/processed/processed_data.csv"

    master_df[["clean_text", "label"]].to_csv(output_path, index=False)

    print(f"\n🎉 SUCCESS! Final Data Lake generated: {output_path}")
    print(f"Total Unique Training Samples: {len(master_df)}")


if __name__ == "__main__":
    build_dynamic_data_lake()
