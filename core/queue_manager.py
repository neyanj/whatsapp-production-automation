import queue
import time
import random

from config import (
    BATCH_COOLDOWN,
    BATCH_SIZE,
    MAX_DELAY,
    MAX_RETRY,
    MIN_DELAY
)

from core.db import get_connection
from core.logger import log_event
from core.sender import send_message

# ==========================================
# GLOBAL QUEUE
# ==========================================
task_queue = queue.Queue()

# ==========================================
# UPDATE TASK STATUS
# ==========================================
def update_task(task_id, status):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        UPDATE tasks

        SET status=?

        WHERE id=?
        """,
        (status, task_id)
    )

    conn.commit()

    conn.close()

# ==========================================
# WORKER FUNCTION
# ==========================================
def worker(driver, worker_id):

    processed = 0

    while True:

        try:
            task = task_queue.get(timeout=5)

        except queue.Empty:

            print(
                f"✅ Worker {worker_id} completed"
            )

            break

        except Exception as e:

            print(
                f"❌ Queue Error: {e}"
            )

            break

        try:

            task_id = task["id"]

            recipient = task["recipient"]

            recipient_type = task[
                "recipient_type"
            ]

            message = task["message"]

            success = False

            print(
                f"\\n📤 Worker {worker_id} processing: {recipient}"
            )

            # ==================================
            # RETRY LOOP
            # ==================================
            for attempt in range(MAX_RETRY):

                print(
                    f"🔁 Attempt {attempt + 1}"
                )

                start = time.time()

                log_event(
                    task_id,
                    "PROCESSING"
                )

                success = send_message(
                    driver,
                    recipient,
                    recipient_type,
                    message
                )

                end = time.time()

                processing_time = round(
                    end - start,
                    2
                )

                if success:

                    update_task(
                        task_id,
                        "SENT"
                    )

                    log_event(
                        task_id,
                        "SENT",
                        processing_time
                    )

                    print(
                        f"✅ SENT → {recipient}"
                    )

                    break

                else:

                    log_event(
                        task_id,
                        "RETRY",
                        processing_time
                    )

                    print(
                        f"⚠️ RETRY → {recipient}"
                    )

                    time.sleep(2)

            # ==================================
            # FAILED
            # ==================================
            if not success:

                update_task(
                    task_id,
                    "FAILED"
                )

                log_event(
                    task_id,
                    "FAILED"
                )

                print(
                    f"❌ FAILED → {recipient}"
                )

            processed += 1

            # ==================================
            # BATCH COOL DOWN
            # ==================================
            if processed % BATCH_SIZE == 0:

                print(
                    f"⏳ Cooling for {BATCH_COOLDOWN} sec..."
                )

                time.sleep(
                    BATCH_COOLDOWN
                )

            # ==================================
            # RANDOM DELAY
            # ==================================
            delay = random.uniform(
                MIN_DELAY,
                MAX_DELAY
            )

            print(
                f"⏳ Waiting {round(delay, 2)} sec"
            )

            time.sleep(delay)

        except Exception as e:

            print(f"❌ Worker Error: {e}")

            log_event(
                task_id,
                "WORKER_ERROR",
                remark=str(e)
            )

        finally:

            task_queue.task_done()