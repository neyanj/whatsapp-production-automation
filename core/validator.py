import re

# ==========================================
# DETECT RECIPIENT TYPE
# ==========================================

def detect_recipient_type(
    recipient
):

    recipient = (
        str(recipient)
        .strip()
    )

    digits = re.sub(
        r"\\D",
        "",
        recipient
    )

    # ======================================
    # INDIAN MOBILE NUMBER
    # ======================================

    if len(digits) == 10:

        return "number"

    return "group"


# ==========================================
# FORMAT INDIAN NUMBER
# ==========================================

def format_indian_number(
    number
):

    digits = re.sub(
        r"\\D",
        "",
        str(number)
    )

    # already with country code
    if (
        len(digits) == 12
        and
        digits.startswith("91")
    ):

        return digits

    # plain 10 digit
    if len(digits) == 10:

        return f"91{digits}"

    return None


# ==========================================
# VALIDATE RECIPIENT
# ==========================================

def validate_recipient(
    recipient
):

    recipient = (
        str(recipient)
        .strip()
    )

    if not recipient:

        return False

    recipient_type = (
        detect_recipient_type(
            recipient
        )
    )

    # ======================================
    # NUMBER VALIDATION
    # ======================================

    if recipient_type == "number":

        formatted = (
            format_indian_number(
                recipient
            )
        )

        if not formatted:

            return False

    return True


# ==========================================
# VALIDATE MESSAGE
# ==========================================

def validate_message(
    message
):

    if message is None:

        return False

    message = str(message)

    if not message.strip():

        return False

    return True


# ==========================================
# VALIDATE ROW
# ==========================================

def validate_row(row):

    # ======================================
    # RECIPIENT
    # ======================================

    recipient = row.get(
        "recipient",
        ""
    )

    if not validate_recipient(
        recipient
    ):

        return (
            False,
            "Invalid Recipient"
        )

    # ======================================
    # MESSAGE
    # ======================================

    message = row.get(
        "message",
        ""
    )

    if not validate_message(
        message
    ):

        return (
            False,
            "Invalid Message"
        )

    return True, "OK"