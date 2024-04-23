import threading

from django.core.mail import EmailMessage

from core.models import OnlineDonation


from_email = 'gift200161@gmail.com'

class EmailThread(threading.Thread):
    def __init__(self, email):
        super().__init__()
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=True)


def send_thank_you_email(donation: OnlineDonation):
    subject = "Thank You for Your Generous Donation!"
    to_email = [donation.donor_email]
    email_message = f"""
    Dear {donation.donor_name},

    On behalf of {donation.beneficiary.name}, we extend our heartfelt gratitude for your generous donation. Your support enables us to continue our mission. 

    Your donation of {donation.currency}{donation.amount} has a significant impact on the lives of those we serve, and we are sincerely grateful for your kindness and generosity.

    If you have any questions or would like to learn more about how your donation is making a difference, please don't hesitate to contact us.

    With warmest regards,
    {donation.beneficiary.name}
    {donation.beneficiary.email}
    {donation.beneficiary.cell}
    """
    email = EmailMessage(
        subject=subject,
        to=to_email,
        body=email_message,
        from_email=from_email
    )
    # Start the email thread
    EmailThread(email=email).start()


def send_donation_received_email(donation: OnlineDonation):
    subject = "Notification: You Have Received a Donation!"
    to_email = [donation.beneficiary.email, donation.beneficiary.manager.email]
    email_message = f"""
    Dear {donation.beneficiary.name},

    We are thrilled to inform you that you have received a generous donation from {donation.donor_name}.

    The donation amount is {donation.currency}{donation.amount}, and it will contribute significantly to mission.

    We want to express our deepest gratitude to {donation.donor_name} for their kindness and generosity. It is through the support of compassionate individuals like them that we are able to continue our mission.

    If you have any questions or would like to provide a personal message of thanks to the donor, please feel free to contact us.

    With warm regards,
    Online Donors
    """
    email = EmailMessage(
        subject=subject,
        to=to_email,
        body=email_message,
        from_email=from_email
    )
    # Start the email thread
    EmailThread(email=email).start()


def send_anonymous_donation_received_email(donation: OnlineDonation):
    subject = "Notification: You Have Received an Anonymous Donation!"
    to_email = [donation.beneficiary.email, donation.beneficiary.manager.email]
    email_message = f"""
    Dear {donation.beneficiary.name},

    We are thrilled to inform you that you have received a generous anonymous donation.

    The donation amount is {donation.currency}{donation.amount}, and it will contribute significantly to our mission.

    We want to express our deepest gratitude for this anonymous contribution. It is through the support of compassionate individuals like this donor that we are able to continue our mission.

    If you have any questions or would like to provide a message of thanks, please feel free to contact us.

    With warm regards,
    Online Donors
    """
    email = EmailMessage(
        subject=subject,
        to=to_email,
        body=email_message,
        from_email=from_email
    )
    # Start the email thread
    EmailThread(email=email).start()
