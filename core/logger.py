from datetime import datetime

from core.db import get_connection

# ==========================================
# LOG EVENT
# ==========================================
def log_event(
    task_id,
    status,
    processing_time=None,
    remark=""
):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO logs (

            task_id,
            status,
            processing_time,
            timestamp,
            remark

        ) VALUES (?, ?, ?, ?, ?)
        """,
        (
            task_id,
            status,
            processing_time,
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            remark
        )
    )

    conn.commit()

    conn.close()