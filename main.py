
from pyscript import document, when


# Proposed CampusPrint Hub prices
PRICES = {
    "bw": 2,
    "color": 5,
    "copy": 2,
    "scan": 5,
    "format": 10,
    "binding": 25,
}

SERVICE_NAMES = {
    "bw": "Black-and-white printing",
    "color": "Colored printing",
    "copy": "Photocopying",
    "scan": "Document scanning",
    "format": "Document formatting",
    "binding": "Binding",
}

UNIT_NAMES = {
    "bw": "pages",
    "color": "pages",
    "copy": "pages",
    "scan": "files",
    "format": "files",
    "binding": "binding service(s)",
}


def get_element(element_id):
    return document.querySelector(f"#{element_id}")


def calculate_total():
    service = get_element("service").value
    quantity_text = get_element("quantity").value

    try:
        quantity = int(quantity_text)
    except (ValueError, TypeError):
        raise ValueError("Please enter a valid whole number.")

    if quantity < 1 or quantity > 1000:
        raise ValueError("Quantity must be between 1 and 1000.")

    total = PRICES[service] * quantity

    # Rush service adds ₱5 once per order.
    if get_element("rush").checked:
        total += 5

    return service, quantity, total


def show_message(message, success=True):
    box = get_element("order-message")
    box.textContent = message
    box.className = (
        "message visible success"
        if success
        else "message visible error"
    )


def update_estimate():
    try:
        service, quantity, total = calculate_total()

        get_element("total-price").textContent = f"₱{total:.2f}"

        note = (
            f"{quantity} {UNIT_NAMES[service]} × "
            f"₱{PRICES[service]:.2f}"
        )

        if get_element("rush").checked:
            note += " + ₱5.00 rush fee"

        get_element("estimate-note").textContent = (
            note + ". Final price may vary for formatting and binding."
        )

        return True

    except (ValueError, KeyError) as error:
        get_element("total-price").textContent = "—"
        get_element("estimate-note").textContent = str(error)
        return False


def update_quantity_label():
    service = get_element("service").value
    label = get_element("quantity-label")

    if service in ("bw", "color", "copy"):
        label.textContent = "Number of pages"
    elif service == "scan":
        label.textContent = "Number of files"
    elif service == "format":
        label.textContent = "Number of files (₱10 minimum each)"
    else:
        label.textContent = "Number of binding services (₱25 minimum each)"


# EVENT 1: Calculate Price button click
@when("click", "#calculate-btn")
def calculate_button_clicked(event):
    if update_estimate():
        show_message(
            "Price calculated successfully! "
            "Review your estimated total before submitting.",
            True,
        )
    else:
        show_message(
            "Please check your quantity and try again.",
            False,
        )


# EVENT 2: Service selection changes
@when("change", "#service")
def service_changed(event):
    update_quantity_label()
    update_estimate()


# EVENT 3: Quantity input changes
@when("input", "#quantity")
def quantity_changed(event):
    update_estimate()


# EVENT 4: Rush service checkbox changes
@when("change", "#rush")
def rush_changed(event):
    update_estimate()


# EVENT 5: Order form submission
@when("submit", "#order-form")
def submit_order(event):
    event.preventDefault()

    name = get_element("customer-name").value.strip()

    if not name:
        show_message("Please enter your name.", False)
        return

    if not update_estimate():
        show_message(
            "Please correct the quantity before submitting.",
            False,
        )
        return

    service, quantity, total = calculate_total()
    service_name = SERVICE_NAMES[service]
    unit = UNIT_NAMES[service]

    confirmation = (
        f"Thank you, {name}! "
        f"Your demo order has been prepared. "
        f"Service: {service_name}. "
        f"Quantity: {quantity} {unit}. "
        f"Estimated total: ₱{total:.2f}. "
        f"This is a demonstration only. "
        f"No order has been sent or stored."
    )

    show_message(confirmation, True)


# Initial website setup
update_quantity_label()
update_estimate()
