from flask import (
    Flask,
    render_template,
    request,
    redirect
)

import os

from core.db import (
    init_db,
    get_connection
)

from core.uploader import upload_excel
from core.analytics import get_analytics

# ==========================================
# FLASK APP
# ==========================================
app = Flask(__name__)

# ==========================================
# INIT DATABASE
# ==========================================
init_db()

# ==========================================
# HOME PAGE
# ==========================================
@app.route("/", methods=["GET", "POST"])
def index():

    conn = get_connection()

    cur = conn.cursor()

    # ======================================
    # MANUAL TASK CREATION
    # ======================================
    if request.method == "POST":

        recipients = request.form.get(
            "recipient"
        )

        message = request.form.get(
            "message"
        )

        schedule_date = request.form.get(
    "schedule_date"
)

        schedule_clock = request.form.get(
    "schedule_clock"
)

        schedule_time = None

        if schedule_date and schedule_clock:

            schedule_time = (
                f"{schedule_date} {schedule_clock}:00"
            )
        split_recipients = recipients.split(
            "\n"
        )

        for recipient in split_recipients:

            recipient = recipient.strip()

            if not recipient:
                continue

            recipient_type = "group"

            if recipient.replace(
                "+", ""
            ).isdigit():

                recipient_type = "phone"

            cur.execute(
                """
                INSERT INTO tasks (

                    recipient,
                    recipient_type,
                    message,
                    schedule_time,
                    status,
                    created_at

                ) VALUES (?, ?, ?, ?, ?, datetime('now'))
                """,
                (
                    recipient,
                    recipient_type,
                    message,
                    schedule_time,
                    "PENDING"
                )
            )

        conn.commit()

        return redirect("/")

    # ======================================
    # FETCH TASKS
    # ======================================
    cur.execute(
        """
        SELECT *

        FROM tasks

        ORDER BY id DESC

        LIMIT 50
        """
    )

    tasks = cur.fetchall()

    conn.close()

    return render_template(
        "index.html",
        tasks=tasks
    )

# ==========================================
# EXCEL UPLOAD
# ==========================================
@app.route("/upload", methods=["POST"])
def upload():

    if "file" not in request.files:

        return "No file uploaded"

    file = request.files["file"]

    if file.filename == "":

        return "Empty filename"

    # ======================================
    # CREATE UPLOADS FOLDER
    # ======================================
    os.makedirs(
        "uploads",
        exist_ok=True
    )

    path = os.path.join(
        "uploads",
        file.filename
    )

    file.save(path)

    inserted, failed = upload_excel(path)

    return f"""

    Upload Completed

    Inserted: {inserted}

    Failed: {failed}

    <br><br>

    <a href='/'>Go Back</a>
    """

# ==========================================
# DASHBOARD
# ==========================================
@app.route("/dashboard")
def dashboard():

    conn = get_connection()

    cur = conn.cursor()

    # ======================================
    # ANALYTICS
    # ======================================
    analytics = get_analytics()

    # ======================================
    # RECENT TASKS
    # ======================================
    cur.execute(
        """
        SELECT *

        FROM tasks

        ORDER BY id DESC

        LIMIT 20
        """
    )

    tasks = cur.fetchall()

    # ======================================
    # RECENT LOGS
    # ======================================
    cur.execute(
        """
        SELECT *

        FROM logs

        ORDER BY id DESC

        LIMIT 50
        """
    )

    logs = cur.fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        analytics=analytics,
        tasks=tasks,
        logs=logs
    )
# ==========================================
# RUN APP
# ==========================================
if __name__ == "__main__":
    init_db()

    app.run(
        debug=True
    )