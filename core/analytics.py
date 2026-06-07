from core.db import get_connection

def get_analytics():

    conn = get_connection()

    cur = conn.cursor()

    analytics = {}

    cur.execute(
        "SELECT COUNT(*) FROM tasks"
    )

    analytics["total"] = cur.fetchone()[0]

    cur.execute(
        "SELECT COUNT(*) FROM tasks WHERE status='SENT'"
    )

    analytics["sent"] = cur.fetchone()[0]

    cur.execute(
        "SELECT COUNT(*) FROM tasks WHERE status='FAILED'"
    )

    analytics["failed"] = cur.fetchone()[0]

    cur.execute(
        """
        SELECT AVG(processing_time)
        FROM tasks
        """
    )

    analytics["avg_time"] = round(
        cur.fetchone()[0] or 0,
        2
    )

    conn.close()

    return analytics