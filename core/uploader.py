import pandas as pd

from datetime import datetime

from core.db import get_connection

from core.validator import (
    validate_row,
    detect_recipient_type
)


def clean_text(value):

    if pd.isna(value):
        return ""

    return str(value).strip()


def upload_excel(file_path):

    # ======================================
    # LOAD EXCEL
    # ======================================

    df = pd.read_excel(
        file_path,
        dtype=str
    )

    # ======================================
    # NORMALIZE HEADERS
    # ======================================

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
    )

    conn = get_connection()

    cur = conn.cursor()

    inserted = 0
    failed = 0

    # ======================================
    # ITERATE ROWS
    # ======================================

    for index, row in df.iterrows():

        valid, reason = validate_row(row)

        if not valid:

            print(
                f"Row {index+1} Failed: {reason}"
            )

            failed += 1

            continue

        try:

            # ==============================
            # RECIPIENT
            # ==============================

            recipient = clean_text(
                row["recipient"]
            )

            recipient_type = (
                detect_recipient_type(
                    recipient
                )
            )

            # ==============================
            # MESSAGE
            # ==============================

            raw_message = row["message"]

            if pd.isna(raw_message):

             message = ""

            else:

                message = str(raw_message)

                # preserve exact formatting
                message = (
                    message
                    .replace("\r\n", "\n")
                    .replace("\r", "\n")
                )

                 # remove trailing spaces only
                message = "\n".join(
                     line.rstrip()
                        for line in message.split("\n")
                    )

            # ==============================
            # SCHEDULE TIME
            # ==============================

            raw_schedule = clean_text(
                row.get(
                    "schedule_time",
                    ""
                )
            )

            if raw_schedule:

                try:

                    schedule_time = (
                        pd.to_datetime(
                            raw_schedule
                        ).strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )
                    )

                except:

                    schedule_time = None

            else:

                schedule_time = None

            # ==============================
            # INSERT
            # ==============================

            cur.execute(
                """
                INSERT INTO tasks (

                    recipient,
                    recipient_type,
                    message,
                    schedule_time,
                    status,
                    created_at

                )

                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    recipient,
                    recipient_type,
                    message,
                    schedule_time,
                    "PENDING",
                    datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                )
            )

            inserted += 1

        except Exception as e:

            print(
                f"Insert Error Row "
                f"{index+1}: {e}"
            )

            failed += 1

    conn.commit()

    conn.close()

    return inserted, failed