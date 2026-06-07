import time
import platform

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import (
    ActionChains
)

from core.validator import (
    detect_recipient_type,
    format_indian_number
)

# ==========================================
# CONTROL KEY
# ==========================================

SYSTEM_NAME = platform.system()

if SYSTEM_NAME == "Darwin":

    CONTROL_KEY = Keys.COMMAND

else:

    CONTROL_KEY = Keys.CONTROL


# ==========================================
# WAIT FOR WHATSAPP
# ==========================================

def wait_for_whatsapp(driver):

    print("\nOpening WhatsApp Web...")

    driver.get(
        "https://web.whatsapp.com"
    )

    for _ in range(120):

        try:

            driver.find_element(
                By.ID,
                "pane-side"
            )

            print(
                "✅ WhatsApp Loaded"
            )

            return True

        except:

            time.sleep(1)

    return False


# ==========================================
# CLEAR SEARCH
# ==========================================

def clear_search(search_box):

    search_box.click()

    time.sleep(1)

    search_box.send_keys(
        CONTROL_KEY + "a"
    )

    time.sleep(1)

    search_box.send_keys(
        Keys.DELETE
    )

    time.sleep(1)


# ==========================================
# OPEN GROUP
# ==========================================

def open_group_chat(
    driver,
    recipient
):

    try:

        search_box = driver.find_element(
            By.XPATH,
            '//input[@aria-label="Search or start a new chat"]'
        )

        clear_search(search_box)

        search_box.send_keys(
            recipient
        )

        time.sleep(3)

        chat = driver.find_element(
            By.XPATH,
            f'//span[contains(@title,"{recipient}")]'
        )

        chat.click()

        time.sleep(2)

        return True

    except Exception as e:

        print(
            f"❌ Group Open Error: {e}"
        )

        return False


# ==========================================
# OPEN NUMBER
# ==========================================

def open_number_chat(
    driver,
    number
):

    try:

        formatted_number = (
            format_indian_number(
                number
            )
        )

        if not formatted_number:

            return False

        url = (
            "https://web.whatsapp.com/send"
            f"?phone={formatted_number}"
        )

        driver.get(url)

        print(
            f"📱 Opening: {formatted_number}"
        )

        for _ in range(30):

            try:

                driver.find_element(
                    By.XPATH,
                    '//footer//div[@contenteditable="true"]'
                )

                print(
                    "✅ Number Chat Opened"
                )

                return True

            except:

                time.sleep(1)

        return False

    except Exception as e:

        print(
            f"❌ Number Open Error: {e}"
        )

        return False


# ==========================================
# PASTE MESSAGE
# ==========================================

def paste_message(
    driver,
    message
):

    try:

        editor = driver.find_element(
            By.XPATH,
            '//footer//div[@contenteditable="true"]'
        )

        editor.click()

        time.sleep(1)

        # ==================================
        # CLEAR OLD MESSAGE
        # ==================================

        actions = ActionChains(driver)

        actions.key_down(
            CONTROL_KEY
        ).send_keys(
            "a"
        ).key_up(
            CONTROL_KEY
        ).perform()

        time.sleep(1)

        editor.send_keys(
            Keys.DELETE
        )

        time.sleep(1)

        # ==================================
        # CLEAN FORMATTING
        # ==================================

        message = (
            str(message)
            .replace("\r\n", "\n")
            .replace("\r", "\n")
        )

        # ==================================
        # CLIPBOARD COPY
        # ==================================

        driver.execute_script(
            """
            navigator.clipboard.writeText(
                arguments[0]
            );
            """,
            message
        )

        time.sleep(1)

        # ==================================
        # REAL PASTE
        # ==================================

        actions = ActionChains(driver)

        actions.key_down(
            CONTROL_KEY
        ).send_keys(
            "v"
        ).key_up(
            CONTROL_KEY
        ).perform()

        time.sleep(2)

        inserted_text = (
            editor.text.strip()
        )

        if not inserted_text:

            return False

        return True

    except Exception as e:

        print(
            f"❌ Paste Error: {e}"
        )

        return False


# ==========================================
# VERIFY SENT
# ==========================================

def verify_sent(driver):

    try:

        editor = driver.find_element(
            By.XPATH,
            '//footer//div[@contenteditable="true"]'
        )

        time.sleep(2)

        remaining_text = (
            editor.text.strip()
        )

        # ==================================
        # IF BOX EMPTY = SENT
        # ==================================

        if remaining_text == "":

            return True

        return False

    except:

        return False


# ==========================================
# SEND MESSAGE
# ==========================================

def send_message(
    driver,
    recipient,
    message
):

    try:

        print(
            f"\n📤 Sending To: {recipient}"
        )

        # ==================================
        # DETECT TYPE
        # ==================================

        recipient_type = (
            detect_recipient_type(
                recipient
            )
        )

        # ==================================
        # OPEN CHAT
        # ==================================

        if recipient_type == "number":

            opened = open_number_chat(
                driver,
                recipient
            )

        else:

            opened = open_group_chat(
                driver,
                recipient
            )

        if not opened:

            print(
                "❌ Chat Open Failed"
            )

            return False

        # ==================================
        # PASTE MESSAGE
        # ==================================

        pasted = paste_message(
            driver,
            message
        )

        if not pasted:

            print(
                "❌ Paste Failed"
            )

            return False

        # ==================================
        # SEND MESSAGE
        # ==================================

        editor = driver.find_element(
            By.XPATH,
            '//footer//div[@contenteditable="true"]'
        )

        editor.send_keys(
            Keys.ENTER
        )

        time.sleep(3)

        # ==================================
        # VERIFY
        # ==================================

        verified = verify_sent(
            driver
        )

        if verified:

            print(
                f"✅ SENT: {recipient}"
            )

            return True

        print(
            f"❌ VERIFY FAILED: {recipient}"
        )

        return False

    except Exception as e:

        print(
            f"❌ SEND ERROR: {e}"
        )

        return False