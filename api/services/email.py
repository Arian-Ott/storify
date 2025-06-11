from api.db import get_db
from uuid import uuid4, UUID
from api.utils.email import emailer
from api.models.email import EmailToken
from datetime import datetime, timedelta
from api.services.user_service import get_user

import os
from jinja2 import Template
import json

ISSUED_REASONS = ("password_reset", "email_verification", "account_activation")


def clean_invalid_tokens(user_id: UUID):
    """
    Marks all expired, unused tokens for the given user as used.
    """
    profile = get_user(user_id=user_id)
    if not profile:
        raise ValueError("User not found")

    # Acquire a DB session
    with next(get_db()) as db:
        # Mark expired tokens as used
        newest_token = (
            db.query(EmailToken)
            .filter(
                EmailToken.profile_id == profile.id,
                EmailToken.is_used.is_(False),
            )
            .order_by(EmailToken.expires_at.desc())
            .first()
        )
        db.query(EmailToken).filter(
            EmailToken.profile_id == profile.id,
            EmailToken.is_used.is_(False),
            EmailToken.expires_at < datetime.now(),
        ).update(
            {EmailToken.is_used: True},
        )
        if newest_token:
            # If there is a valid token, do not delete it
            db.query(EmailToken).filter(
                EmailToken.profile_id == profile.id,
                EmailToken.token != newest_token.token,
            ).update(
                {EmailToken.is_used: True},
            )
        db.commit()
        db.flush()


def generate_verification_token(
    profile_id: UUID, issued_because: str, time_delta: timedelta = timedelta(days=1)
) -> EmailToken:
    """
    Generates and stores a unique email token for the specified reason.
    """
    if issued_because not in ISSUED_REASONS:
        raise ValueError(
            f"Invalid issued_because value. Must be one of {ISSUED_REASONS}"
        )
    profile = get_user(user_id=profile_id)
    if not profile:
        raise ValueError("User not found")

    # Cleanup any old, expired tokens first
    clean_invalid_tokens(profile_id)

    with next(get_db()) as db:
        token_str = uuid4().hex
        expires = datetime.now() + time_delta
        new_token = EmailToken(
            token=token_str,
            expires_at=expires,
            profile_id=profile.id,
            is_used=False,
            issued_because=issued_because,
        )
        db.add(new_token)
        db.commit()
        db.refresh(new_token)

        print("From hell")

    return new_token


def send_account_verification_email(email: str, username: str):
    """
    Generates a verification token, renders the email template, and sends the verification email.
    """
    profile = get_user(username=username)
    print(f"Sending verification email to {email} for user {username}")
    print(f"Profile found: {profile}")
    if not profile:
        raise ValueError("User not found")

    # Create a fresh verification token
    token_obj = generate_verification_token(profile.id, "email_verification")

    # Build the verification URL
    frontend = os.getenv("HOSTNAME", "https://example.com")

    link = f"{frontend}/auth/verify-email?token={token_obj.token}"
    print(f"Verification link: {link}")
    # Load the template data from JSON
    with open("api/utils/email_texts/account_verification.json", "r") as f:
        template_data = dict(dict(json.load(f)).get("default"))
        print(f"Template data loaded: {template_data}")

    # Render the email content
    template = Template(
        """
                        {{ greeting }} {{ username }},\n{{ body }}\n{{ link }}\n{{ verification_link }}\n{{ closing }},
                        {{ signature }}
                        """,
        trim_blocks=True,
        lstrip_blocks=True,
    )

    rendered_body = str(
        template.render(
            greeting=template_data.get("greeting", "Hello"),
            username=profile.username,
            body=template_data.get(
                "body", "Please verify your email by clicking the link below."
            ),
            verification_link=template_data.get(
                "verification_link_text", "Verify your email"
            ),
            link=link,
            closing=template_data.get("closing", "Thank you"),
            signature=template_data.get("signature", "The Team"),
        )
    )
    rendered_body = f"""
    Hello {profile.username},\n
    Please verify your email by clicking the link below:\n
    {link}\n
    If you did not request this, please ignore this email.\n
    Thank you,\n
    Storify Team
    """
    print(f"Rendered email body: {rendered_body}")
    # Send the email
    emailer.send_email(
        receiver_email=email,
        subject=template_data.get("subject", "Please verify your email"),
        body=rendered_body,
    )


def verify_email_token(token: str) -> EmailToken:
    """
    Verifies the provided email token and marks it as used if valid.
    """
    with next(get_db()) as db:
        # Fetch the token from the database
        user = db.query(EmailToken).filter(EmailToken.token == token).first()

    
    with next(get_db()) as db:
        email_token = (
            db.query(EmailToken)
            .filter(
                EmailToken.token == token,
                EmailToken.is_used.is_(False),
                EmailToken.expires_at > datetime.now(),
            )
            .first()
        )

        if not email_token:
            
            return

        # Mark the token as used
        email_token.is_used = True
        db.commit()
        db.refresh(email_token)
        username = get_user(user_id=email_token.profile_id)
        
    return email_token
