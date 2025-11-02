"""Email service tools for sending notifications and confirmations."""

import os
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import List, Optional, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class EmailService:
    """Service for sending travel-related emails and notifications."""
    
    def __init__(self):
        """Initialize email service with configuration."""
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.email_address = os.getenv("EMAIL_ADDRESS")
        self.email_password = os.getenv("EMAIL_PASSWORD")
        self.use_tls = os.getenv("EMAIL_USE_TLS", "true").lower() == "true"
        
        if not self.email_address or not self.email_password:
            logger.warning("Email credentials not configured. Email functionality will be simulated.")
            self.enabled = False
        else:
            self.enabled = True
    
    def send_email(
        self,
        to_addresses: List[str],
        subject: str,
        body: str,
        html_body: Optional[str] = None,
        cc_addresses: Optional[List[str]] = None,
        bcc_addresses: Optional[List[str]] = None,
        attachments: Optional[List[Dict[str, Any]]] = None
    ) -> bool:
        """
        Send an email with optional HTML content and attachments.
        
        Args:
            to_addresses: List of recipient email addresses
            subject: Email subject line
            body: Plain text email body
            html_body: Optional HTML email body
            cc_addresses: Optional CC recipients
            bcc_addresses: Optional BCC recipients
            attachments: Optional list of attachments with 'filename' and 'content' keys
            
        Returns:
            True if email sent successfully, False otherwise
        """
        if not self.enabled:
            logger.info(f"Email simulation: Would send email to {to_addresses}")
            logger.info(f"Subject: {subject}")
            logger.info(f"Body: {body[:100]}...")
            return True
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = self.email_address
            msg['To'] = ', '.join(to_addresses)
            msg['Subject'] = subject
            
            if cc_addresses:
                msg['Cc'] = ', '.join(cc_addresses)
            
            # Add plain text part
            text_part = MIMEText(body, 'plain')
            msg.attach(text_part)
            
            # Add HTML part if provided
            if html_body:
                html_part = MIMEText(html_body, 'html')
                msg.attach(html_part)
            
            # Add attachments if provided
            if attachments:
                for attachment in attachments:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment['content'])
                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename= {attachment["filename"]}'
                    )
                    msg.attach(part)
            
            # Combine all recipients
            all_recipients = to_addresses.copy()
            if cc_addresses:
                all_recipients.extend(cc_addresses)
            if bcc_addresses:
                all_recipients.extend(bcc_addresses)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                if self.use_tls:
                    server.starttls()
                server.login(self.email_address, self.email_password)
                server.send_message(msg, to_addrs=all_recipients)
            
            logger.info(f"Email sent successfully to {to_addresses}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False


def send_booking_confirmation_email(
    user_email: str,
    user_name: str,
    booking_details: Dict[str, Any],
    accessibility_info: Dict[str, Any]
) -> bool:
    """
    Send booking confirmation email with accessibility details.
    
    Args:
        user_email: User's email address
        user_name: User's name
        booking_details: Dictionary containing booking information
        accessibility_info: Dictionary containing accessibility arrangements
        
    Returns:
        True if email sent successfully
    """
    email_service = EmailService()
    
    subject = f"Booking Confirmation - {booking_details.get('destination', 'Your Trip')}"
    
    # Create plain text body
    body = f"""Dear {user_name},

Your booking has been confirmed! Here are your travel details:

BOOKING INFORMATION:
- Destination: {booking_details.get('destination', 'N/A')}
- Dates: {booking_details.get('start_date', 'N/A')} to {booking_details.get('end_date', 'N/A')}
- Booking Reference: {booking_details.get('reference', 'N/A')}

ACCESSIBILITY ARRANGEMENTS:
"""
    
    # Add accessibility information
    if accessibility_info.get('mobility_needs'):
        body += f"- Mobility Needs: {', '.join(accessibility_info['mobility_needs'])}\n"
    
    if accessibility_info.get('assistance_preferences'):
        body += "- Assistance Arrangements:\n"
        for service, preference in accessibility_info['assistance_preferences'].items():
            body += f"  • {service}: {preference}\n"
    
    if accessibility_info.get('special_requests'):
        body += f"- Special Requests: {accessibility_info['special_requests']}\n"
    
    body += f"""
IMPORTANT REMINDERS:
- All accessibility services have been requested and are being confirmed
- You will receive separate confirmations from hotels and airlines
- Contact us immediately if you need to modify any accessibility arrangements

We're here to ensure your trip is comfortable and accessible!

Best regards,
Inclusive Travel Agent Team

Contact: support@inclusivetravel.com
Phone: 1-800-ACCESSIBLE
"""
    
    return email_service.send_email(
        to_addresses=[user_email],
        subject=subject,
        body=body
    )


def send_accessibility_notification_email(
    provider_email: str,
    provider_name: str,
    guest_name: str,
    booking_reference: str,
    accessibility_requirements: Dict[str, Any],
    arrival_date: str,
    departure_date: Optional[str] = None
) -> bool:
    """
    Send accessibility requirements notification to service provider.
    
    Args:
        provider_email: Service provider's email address
        provider_name: Service provider's name
        guest_name: Guest's name
        booking_reference: Booking reference number
        accessibility_requirements: Dictionary of accessibility needs
        arrival_date: Arrival date
        departure_date: Optional departure date
        
    Returns:
        True if email sent successfully
    """
    email_service = EmailService()
    
    subject = f"Accessibility Requirements - {guest_name} - Booking {booking_reference}"
    
    body = f"""Dear {provider_name} Team,

I am writing to confirm accessibility requirements for an upcoming reservation:

BOOKING DETAILS:
- Guest Name: {guest_name}
- Booking Reference: {booking_reference}
- Arrival Date: {arrival_date}
"""
    
    if departure_date:
        body += f"- Departure Date: {departure_date}\n"
    
    body += "\nACCESSIBILITY REQUIREMENTS:\n"
    
    # Add mobility requirements
    if accessibility_requirements.get('mobility_needs'):
        body += "\nMobility Needs:\n"
        for need in accessibility_requirements['mobility_needs']:
            body += f"• {need}\n"
    
    # Add sensory requirements
    if accessibility_requirements.get('sensory_needs'):
        body += "\nSensory Needs:\n"
        for need in accessibility_requirements['sensory_needs']:
            body += f"• {need}\n"
    
    # Add assistance preferences
    if accessibility_requirements.get('assistance_preferences'):
        body += "\nAssistance Preferences:\n"
        for service, preference in accessibility_requirements['assistance_preferences'].items():
            body += f"• {service}: {preference}\n"
    
    # Add equipment needs
    if accessibility_requirements.get('equipment_needs'):
        body += "\nEquipment Requirements:\n"
        for equipment in accessibility_requirements['equipment_needs']:
            body += f"• {equipment}\n"
    
    # Add dietary restrictions
    if accessibility_requirements.get('dietary_restrictions'):
        body += "\nDietary Restrictions:\n"
        for restriction in accessibility_requirements['dietary_restrictions']:
            body += f"• {restriction}\n"
    
    body += f"""
CONFIRMATION REQUEST:
Please confirm that these accessibility arrangements can be accommodated and provide:
1. Written confirmation of all accessibility services
2. Contact information for your accessibility coordinator
3. Any additional information or documentation needed
4. Emergency contact procedures for accessibility issues

We appreciate your commitment to providing excellent accessible service.

Please reply to this email with confirmation details.

Best regards,
Inclusive Travel Agent
Accessibility Coordination Team

Contact: accessibility@inclusivetravel.com
Phone: 1-800-ACCESSIBLE
"""
    
    return email_service.send_email(
        to_addresses=[provider_email],
        subject=subject,
        body=body
    )


def send_checkin_reminder_email(
    user_email: str,
    user_name: str,
    flight_details: Dict[str, Any],
    accessibility_services: Dict[str, Any]
) -> bool:
    """
    Send check-in reminder email with accessibility service information.
    
    Args:
        user_email: User's email address
        user_name: User's name
        flight_details: Dictionary containing flight information
        accessibility_services: Dictionary containing accessibility service details
        
    Returns:
        True if email sent successfully
    """
    email_service = EmailService()
    
    subject = f"Check-in Reminder - Flight {flight_details.get('flight_number', 'N/A')}"
    
    body = f"""Dear {user_name},

Your flight check-in is now available! Here are your details:

FLIGHT INFORMATION:
- Flight: {flight_details.get('flight_number', 'N/A')}
- Date: {flight_details.get('departure_date', 'N/A')}
- Departure: {flight_details.get('departure_time', 'N/A')} from {flight_details.get('departure_airport', 'N/A')}
- Arrival: {flight_details.get('arrival_time', 'N/A')} at {flight_details.get('arrival_airport', 'N/A')}

CHECK-IN STATUS:
✓ Online check-in completed automatically
✓ Accessible seating confirmed: {flight_details.get('seat_number', 'N/A')}
✓ Mobile boarding pass ready

ACCESSIBILITY SERVICES CONFIRMED:
"""
    
    if accessibility_services.get('wheelchair_assistance'):
        body += f"✓ Wheelchair assistance: {accessibility_services['wheelchair_assistance']}\n"
    
    if accessibility_services.get('priority_boarding'):
        body += "✓ Priority boarding confirmed\n"
    
    if accessibility_services.get('special_meals'):
        body += f"✓ Special meal: {accessibility_services['special_meals']}\n"
    
    if accessibility_services.get('assistance_contact'):
        body += f"✓ Assistance contact: {accessibility_services['assistance_contact']}\n"
    
    body += f"""
IMPORTANT REMINDERS:
- Arrive at airport 2 hours early for domestic flights, 3 hours for international
- Proceed to special assistance desk upon arrival
- Have your boarding pass and ID ready
- Contact airline immediately if you need to modify accessibility services

Your boarding pass is attached to this email.

Have a safe and comfortable flight!

Best regards,
Inclusive Travel Agent Team

Emergency Contact: 1-800-ACCESSIBLE
"""
    
    return email_service.send_email(
        to_addresses=[user_email],
        subject=subject,
        body=body
    )


# Tool functions for ADK integration
def send_notification_email(
    recipient_email: str,
    subject: str,
    message: str,
    email_type: str = "notification"
) -> str:
    """
    Send a notification email.
    
    Args:
        recipient_email: Email address to send to
        subject: Email subject
        message: Email message content
        email_type: Type of email (notification, confirmation, reminder)
        
    Returns:
        Success message or error description
    """
    try:
        email_service = EmailService()
        success = email_service.send_email(
            to_addresses=[recipient_email],
            subject=subject,
            body=message
        )
        
        if success:
            return f"Email sent successfully to {recipient_email}"
        else:
            return f"Failed to send email to {recipient_email}"
            
    except Exception as e:
        return f"Error sending email: {str(e)}"


def send_accessibility_provider_notification(
    provider_email: str,
    provider_name: str,
    booking_details: Dict[str, Any],
    accessibility_needs: Dict[str, Any]
) -> str:
    """
    Send accessibility requirements notification to service provider.
    
    Args:
        provider_email: Provider's email address
        provider_name: Provider's name
        booking_details: Booking information
        accessibility_needs: Accessibility requirements
        
    Returns:
        Success message or error description
    """
    try:
        success = send_accessibility_notification_email(
            provider_email=provider_email,
            provider_name=provider_name,
            guest_name=booking_details.get('guest_name', 'Guest'),
            booking_reference=booking_details.get('reference', 'N/A'),
            accessibility_requirements=accessibility_needs,
            arrival_date=booking_details.get('arrival_date', 'N/A'),
            departure_date=booking_details.get('departure_date')
        )
        
        if success:
            return f"Accessibility notification sent to {provider_name} at {provider_email}"
        else:
            return f"Failed to send accessibility notification to {provider_name}"
            
    except Exception as e:
        return f"Error sending accessibility notification: {str(e)}"