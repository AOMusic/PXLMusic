from telethon import TelegramClient, events
from telethon.tl.functions.account import ReportPeerRequest
from telethon.tl.types import (
    InputReportReasonSpam,
    InputReportReasonFake,
    InputReportReasonViolence,
    InputReportReasonPornography,
    InputReportReasonChildAbuse,
    InputReportReasonCopyright,
    InputReportReasonIllegalDrugs,
    InputReportReasonPersonalDetails,
    InputReportReasonOther,
)

import time
import sys
from termcolor import colored

api_id = 1234567
api_hash = "your_api_hash"
phone_number = "+918887275626"

report_reasons = {
    1: ("I don't like it", InputReportReasonOther()),
    2: ("Child abuse", InputReportReasonChildAbuse()),
    3: ("Violence", InputReportReasonViolence()),
    4: ("Illegal goods", InputReportReasonIllegalDrugs()),
    5: ("Illegal adult content", InputReportReasonPornography()),
    6: ("Personal data", InputReportReasonPersonalDetails()),
    7: ("Terrorism", InputReportReasonViolence()),
    8: ("Scam or spam", InputReportReasonSpam()),
    9: ("Copyright", InputReportReasonCopyright()),
    10: ("Other", InputReportReasonOther()),
}

def check_exit(input_value):
    if input_value.lower() == "exit":
        print(colored("Exiting the script.", "red"))
        sys.exit()

def check_home(input_value):
    return input_value.lower() == "home"

def get_valid_input(prompt, valid_options=None):
    while True:
        user_input = input(colored(prompt, "red"))
        check_exit(user_input)
        if check_home(user_input):
            return "home"
        if valid_options:
            try:
                user_input = int(user_input)
                if user_input in valid_options:
                    return user_input
                else:
                    print(colored(f"Please select a valid option from {valid_options}.", "red"))
            except ValueError:
                print(colored("Invalid input. Please enter a number.", "red"))
        else:
            return user_input

def get_valid_integer_input(prompt):
    while True:
        user_input = input(colored(prompt, "red"))
        check_exit(user_input)
        if check_home(user_input):
            return "home"
        try:
            return int(user_input)
        except ValueError:
            print(colored("Invalid input. Please enter a valid integer.", "red"))

async def report_entity(client):
    while True:
        print(colored("1: Account\n2: Channel\n3: Group\n4: Bot\n5: Post Link (Channel/Group Only)", "green"))
        report_type = get_valid_input("What do you want to report: ", valid_options=[1, 2, 3, 4, 5])
        if report_type == "home":
            continue
        print()

        if report_type == 5:
            while True:
                post_link = input(colored("Enter the full post link (e.g., (link unavailable)): ", "red"))
                check_exit(post_link)
                if check_home(post_link):
                    break
                print()
                if not post_link.startswith("(link unavailable)"):
                    print(colored("You can only report a post link. Please provide a valid link.\n", "red"))
                    continue
                try:
                    parts = post_link.replace("(link unavailable)", "").split("/")
                    if len(parts) != 2 or not parts[1].isdigit():
                        print(colored("Invalid post link format. Please provide a valid link.\n", "red"))
                        continue
                    channel_username = parts[0]
                    message_id = int(parts[1])
                    channel = await client.get_entity(channel_username)
                    print(colored("\nReasons:", "green"))
                    for number, (reason_name, _) in report_reasons.items():
                        print(f"{number}: {reason_name}")
                    print()
                    reason_choice = get_valid_input(colored("Enter the number for the reason: ", "red"), valid_options=report_reasons.keys())
                    if reason_choice == "home":
                        break
                    print()
                    num_reports = get_valid_integer_input(colored("How many reports to submit? ", "red"))
                    if num_reports == "home":
                        break
                    print()
                    for i in range(num_reports):
                        await client(
                            ReportPeerRequest(
                                peer=channel,
                                reason=report_reasons[reason_choice][1],
                                message=f"Reported post ID {message_id} for {report_reasons[reason_choice][0]}",
                            )
                        )
                        print(colored(f"Report {i + 1} submitted.", "green"))
                    await client.send_message(channel, f"Your post ID {message_id} has been reported for {report_reasons[reason_choice][0]}")
                    await client.delete_messages(channel, message_id)
                    print(colored(f"Post ID {message_id} deleted.", "green"))
                    print(colored("\nAll reports sent successfully.", "green"))
                except Exception as e:
                    print(colored(f"Error reporting post: {e}", "red"))
            continue

        else:
            entity_username = input(colored("Enter the username or ID (e.g., @username): ", "red"))
            check_exit(entity_username)
            if check_home(entity_username):
                break
            print()
            if not entity_username.startswith("@"):
                entity_username = "@" + entity_username
            try:
                entity = await client.get_entity(entity_username)
                print(colored("\nReasons:", "green"))
                for number, (reason_name, _) in report_reasons.items():
                    print(f"{number}: {reason_name}")
                print()
                reason_choice = get_valid_input(colored("Enter the number for the reason: ", "red"), valid_options=report_reasons.keys())
                if reason_choice == "home":
                    break
                print()
                num_reports = get_valid_integer_input(colored("How many reports to submit? ", "red"))
                if num_reports == "home":
                    break
                print()
                for i in range(num_reports):
                    await client(
                        ReportPeerRequest(
                            peer=entity,
                            reason=report_reasons[reason_choice][1],
                            message=f"Reported for {report_reasons[reason_choice][0]}",
                        )
                    )
                    print(colored(f"Report {i + 1} submitted.", "green"))
            except Exception as e:
                print(colored(f"Error reporting entity: {e}", "red"))

async def main():
    client = TelegramClient("report_session", api_id, api_hash)
    await client.start()
    await report_entity(client)

if __name__ == "__main__":
    import asyncio
    asyncio.get_event_loop().run_until_complete(main())
