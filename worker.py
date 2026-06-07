import time
import random

from selenium import webdriver
from selenium.webdriver.chrome.service import (
    Service
)

from webdriver_manager.chrome import (
    ChromeDriverManager
)

from config import (
    PROFILE_PATH,
    MIN_DELAY,
    MAX_DELAY,
    POLL_INTERVAL
)

from core.db import (
    get_connection
)

from core.sender import (
    wait_for_whatsapp,
    send_message
)

# ==========================================
# DRIVER SETUP
# ==========================================

options = webdriver.ChromeOptions()

options.add_argument(
    f"--user-data-dir={PROFILE_PATH}"
)

options.add_argument(
    "--start-maximized"
)

driver = webdriver.Chrome(
    service=Service(
        ChromeDriverManager().install()
    ),
    options=options
)

# ==========================================
# WAIT FOR WHATSAPP
# ==========================================

loaded = wait_for_whatsapp(
    driver
)

if not loaded:

    driver.quit()

    raise SystemExit

# ==========================================
# MAIN LOOP
# ==========================================

print(
    "\n🚀 Worker Started"
)

while True:

    try:

        conn = get_connection()

        cur = conn.cursor()

        # ==================================
        # FETCH PENDING TASKS
        # ==================================

        cur.execute(
            """
            SELECT *

            FROM tasks

            WHERE status='PENDING'

            AND (

                schedule_time IS NULL

                OR

                datetime(schedule_time)
                <= datetime('now')

            )

            ORDER BY id ASC

            LIMIT 5
            """
        )

        tasks = cur.fetchall()

        conn.close()

        if not tasks:

            print(
                "⏳ No Pending Tasks"
            )

            time.sleep(
                POLL_INTERVAL
            )

            continue

        # ==================================
        # PROCESS TASKS
        # ==================================

        for task in tasks:

            task_id = task["id"]

            recipient = task["recipient"]

            message = task["message"]

            print(
                f"\\n📨 TASK {task_id}"
            )

            # ==============================
            # MARK PROCESSING
            # ==============================

            conn = get_connection()

            cur = conn.cursor()

            cur.execute(
                '''
                UPDATE tasks

                SET status='PROCESSING'

                WHERE id=?
                ''',
                (task_id,)
            )

            conn.commit()

            conn.close()

            # ==============================
            # SEND
            # ==============================

            success = send_message(
                driver,
                recipient,
                message
            )

            # ==============================
            # UPDATE STATUS
            # ==============================

            conn = get_connection()

            cur = conn.cursor()

            if success:

                cur.execute(
                    '''
                    UPDATE tasks

                    SET status='SENT'

                    WHERE id=?
                    ''',
                    (task_id,)
                )

            else:

                cur.execute(
                    '''
                    UPDATE tasks

                    SET status='FAILED'

                    WHERE id=?
                    ''',
                    (task_id,)
                )

            conn.commit()

            conn.close()

            # ==============================
            # SAFE DELAY
            # ==============================

            delay = random.uniform(
                MIN_DELAY,
                MAX_DELAY
            )

            print(
                f"⏳ Waiting {delay:.2f}s"
            )

            time.sleep(delay)

    except Exception as e:

        print(
            f"❌ Worker Error: {e}"
        )

        time.sleep(5)