import smtplib
import ssl
from email.message import EmailMessage
import os


class EmailSender:
    """
    A class to send emails securely using SSL/TLS.

    Attributes:
        smtp_server (str): The SMTP server address (e.g., 'smtp.gmail.com').
        port (int): The port for SSL connection (usually 465 for implicit SSL).
        sender_email (str): The email address of the sender.
        password (str): The password for the sender's email account.
        context (ssl.SSLContext): The SSL context for secure connection.
    """

    def __init__(self, smtp_server: str, port: int, sender_email: str, password: str):
        """
        Initializes the EmailSender with server details and sender credentials.

        Args:
            smtp_server (str): The SMTP server address.
            port (int): The port for SSL connection.
            sender_email (str): The email address of the sender.
            password (str): The password for the sender's email account.
        """
        self.smtp_server = smtp_server
        self.port = port
        self.sender_email = sender_email
        self.password = password

        self.context = ssl.create_default_context()

    def send_email(
        self, receiver_email: str, subject: str, body: str, html_content: str = None
    ):
        """
        Sends an email to a specified receiver.

        Args:
            receiver_email (str): The email address of the recipient.
            subject (str): The subject of the email.
            body (str): The plain text content of the email.
            html_content (str, optional): The HTML content of the email. If provided,
                                        the email will be sent as a multipart message
                                        with both plain text and HTML. Defaults to None.

        Returns:
            bool: True if the email was sent successfully, False otherwise.
        """
        msg = EmailMessage()
        msg["From"] = self.sender_email
        msg["To"] = receiver_email
        msg["Subject"] = subject

        # Set plain text content
        msg.set_content(body)

        if html_content:
            msg.add_alternative(html_content, subtype="html")
            print("Adding HTML content to the email.")

        try:
            with smtplib.SMTP_SSL(self.smtp_server, self.port) as server:
                print(f"Attempting to log in as {self.sender_email}...")

                server.login(self.sender_email, self.password)
                print("Login successful.")

                server.send_message(msg)
                print(f"Email sent successfully to {receiver_email}!")
            return True
        except smtplib.SMTPAuthenticationError as e:
            print(
                f"SMTP Authentication Error: Could not log in. Check your email and password. Details: {e}"
            )
            print(
                "Ensure that 'Less secure app access' or 'App passwords' are enabled for your email provider if you are using services like Gmail."
            )
            return False
        except smtplib.SMTPConnectError as e:
            print(
                f"SMTP Connection Error: Could not connect to the SMTP server. Details: {e}"
            )
            print(
                "Ensure the server address and port are correct, and there are no firewall issues."
            )
            return False
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return False


emailer = EmailSender(
    smtp_server=os.getenv("SMTP_SERVER"),
    port=int(os.getenv("SMTP_PORT", 465)),
    sender_email=os.getenv("SENDER_EMAIL"),
    password=os.getenv("SENDER_PASSWORD"),
)
