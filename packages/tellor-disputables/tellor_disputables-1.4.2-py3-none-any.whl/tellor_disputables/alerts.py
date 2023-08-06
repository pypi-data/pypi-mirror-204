"""Send text messages using Twilio."""
import os
from typing import List
from typing import Optional
from typing import Tuple

import click
from twilio.rest import Client

from tellor_disputables import ALWAYS_ALERT_QUERY_TYPES
from tellor_disputables.data import NewReport


def generic_alert(recipients: List[str], from_number: str, msg: str) -> None:
    """Send a text message to the given recipients."""
    send_text_msg(get_twilio_client(), recipients, from_number, msg)


def get_twilio_info() -> Tuple[Optional[str], Optional[List[str]]]:
    """Read the Twilio from number, client and phone numbers from the environment."""
    twilio_from = os.environ.get("TWILIO_FROM")
    phone_numbers = os.environ.get("ALERT_RECIPIENTS")
    return twilio_from, phone_numbers.split(",") if phone_numbers is not None else None


def dispute_alert(msg: str, recipients: List[str], from_number: str) -> None:
    """send an alert that the dispute was successful to the user"""

    twilio_client = get_twilio_client()
    send_text_msg(twilio_client, recipients, from_number, msg)

    return


def alert(all_values: bool, new_report: NewReport, recipients: List[str], from_number: str) -> None:

    twilio_client = get_twilio_client()

    if new_report.query_type in ALWAYS_ALERT_QUERY_TYPES:
        msg = generate_alert_msg(False, new_report.link)
        send_text_msg(twilio_client, recipients, from_number, msg)

        return

    # Account for unsupported queryIDs
    if new_report.disputable is not None:
        if new_report.disputable:
            msg = generate_alert_msg(True, new_report.link)

    # If user wants ALL NewReports
    if all_values:
        msg = generate_alert_msg(False, new_report.link)
        send_text_msg(twilio_client, recipients, from_number, msg)

    else:
        if new_report.disputable:
            send_text_msg(twilio_client, recipients, from_number, msg)


def generate_alert_msg(disputable: bool, link: str) -> str:
    """Generate an alert message string that
    includes a link to a relevant expolorer."""

    if disputable:
        return f"\n❗DISPUTABLE VALUE❗\n{link}"
    else:
        return f"\n❗NEW VALUE❗\n{link}"


def get_twilio_client() -> Client:
    """Get a Twilio client."""
    return Client(os.environ.get("TWILIO_ACCOUNT_SID"), os.environ.get("TWILIO_AUTH_TOKEN"))


def send_text_msg(client: Client, recipients: list[str], from_number: str, msg: str) -> None:
    """Send a text message to the recipients."""
    click.echo("Alert sent!")
    for num in recipients:
        client.messages.create(
            to=num,
            from_=from_number,
            body=msg,
        )
