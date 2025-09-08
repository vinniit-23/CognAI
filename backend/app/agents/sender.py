"""
Email Sender Agent
Specialized agent for sending emails via Gmail API
"""

import requests
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any, List, Optional
import json


class EmailSender:
    """
    Specialized agent for sending emails through Gmail API
    Handles various email sending scenarios with proper formatting
    """
    
    def __init__(self, user_id: str, get_token_func: callable):
        """
        Initialize Email Sender
        
        Args:
            user_id: Descope user ID
            get_token_func: Function to get Gmail access token
        """
        self.user_id = user_id
        self.get_token_func = get_token_func
        self.base_url = "https://gmail.googleapis.com/gmail/v1/users/me"
    
    def _get_access_token(self) -> str:
        """Get fresh Gmail access token"""
        token_data = self.get_token_func(self.user_id)
        return token_data["token"]["accessToken"]
    
    def _create_message(
        self, 
        to: str, 
        subject: str, 
        body: str,
        from_email: Optional[str] = None,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None,
        reply_to: Optional[str] = None
    ) -> str:
        """
        Create a MIME message for Gmail API
        
        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body (can be HTML or plain text)
            from_email: Sender email (optional)
            cc: CC recipients (optional)
            bcc: BCC recipients (optional)
            reply_to: Reply-to address (optional)
            
        Returns:
            Base64 encoded message string
        """
        # Create message
        message = MIMEMultipart('alternative')
        
        # Set headers
        message['To'] = to
        message['Subject'] = subject
        
        if from_email:
            message['From'] = from_email
        
        if cc:
            message['Cc'] = ', '.join(cc)
        
        if bcc:
            message['Bcc'] = ', '.join(bcc)
        
        if reply_to:
            message['Reply-To'] = reply_to
        
        # Detect if body is HTML or plain text
        if '<html>' in body.lower() or '<p>' in body.lower() or '<div>' in body.lower():
            # HTML body
            html_part = MIMEText(body, 'html')
            message.attach(html_part)
        else:
            # Plain text body
            text_part = MIMEText(body, 'plain')
            message.attach(text_part)
        
        # Encode message
        raw_message = base64.urlsafe_b64encode(
            message.as_bytes()
        ).decode('utf-8')
        
        return raw_message
    
    def send_email(
        self,
        to: str,
        subject: str,
        body: str,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None,
        thread_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Send an email
        
        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body
            cc: CC recipients
            bcc: BCC recipients
            thread_id: Thread ID for replies
            
        Returns:
            Result dictionary with success status and message info
        """
        try:
            access_token = self._get_access_token()
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            # Create the message
            raw_message = self._create_message(
                to=to,
                subject=subject,
                body=body,
                cc=cc,
                bcc=bcc
            )
            
            # Prepare API payload
            api_message = {
                "raw": raw_message
            }
            
            # Add thread ID for replies
            if thread_id:
                api_message["threadId"] = thread_id
            
            # Send the email
            response = requests.post(
                f"{self.base_url}/messages/send",
                headers=headers,
                data=json.dumps(api_message),
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "message_id": result.get("id"),
                    "thread_id": result.get("threadId"),
                    "recipient": to,
                    "subject": subject
                }
            else:
                return {
                    "success": False,
                    "error": f"Failed to send email: {response.status_code} - {response.text}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Error sending email: {str(e)}"
            }
    
    def reply_to_email(
        self,
        original_message_id: str,
        reply_body: str,
        thread_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Reply to an existing email
        
        Args:
            original_message_id: ID of the original message
            reply_body: Body of the reply
            thread_id: Thread ID (optional, will be fetched if not provided)
            
        Returns:
            Result dictionary with success status
        """
        try:
            # First, get the original message details
            access_token = self._get_access_token()
            headers = {"Authorization": f"Bearer {access_token}"}
            
            # Fetch original message
            response = requests.get(
                f"{self.base_url}/messages/{original_message_id}",
                headers=headers,
                params={"format": "metadata"},
                timeout=15
            )
            
            if response.status_code != 200:
                return {
                    "success": False,
                    "error": "Could not fetch original message"
                }
            
            original_message = response.json()
            
            # Extract original email details
            headers_data = original_message['payload']['headers']
            original_subject = ""
            original_from = ""
            original_to = ""
            
            for header in headers_data:
                if header['name'].lower() == 'subject':
                    original_subject = header['value']
                elif header['name'].lower() == 'from':
                    original_from = header['value']
                elif header['name'].lower() == 'to':
                    original_to = header['value']
            
            # Create reply subject
            reply_subject = original_subject
            if not reply_subject.lower().startswith('re:'):
                reply_subject = f"Re: {original_subject}"
            
            # Send reply
            return self.send_email(
                to=original_from,
                subject=reply_subject,
                body=reply_body,
                thread_id=thread_id or original_message.get('threadId')
            )
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error replying to email: {str(e)}"
            }
    
    def send_draft_email(self, draft: Dict[str, str], to: str) -> Dict[str, Any]:
        """
        Send a drafted email
        
        Args:
            draft: Email draft with 'subject' and 'body' keys
            to: Recipient email address
            
        Returns:
            Result dictionary with success status
        """
        return self.send_email(
            to=to,
            subject=draft.get('subject', 'No Subject'),
            body=draft.get('body', 'No content')
        )
    
    def forward_email(
        self,
        original_message_id: str,
        to: str,
        forward_message: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Forward an existing email
        
        Args:
            original_message_id: ID of the original message to forward
            to: Recipient for the forwarded email
            forward_message: Optional message to add before forwarded content
            
        Returns:
            Result dictionary with success status
        """
        try:
            # Get the original message
            access_token = self._get_access_token()
            headers = {"Authorization": f"Bearer {access_token}"}
            
            response = requests.get(
                f"{self.base_url}/messages/{original_message_id}",
                headers=headers,
                params={"format": "full"},
                timeout=15
            )
            
            if response.status_code != 200:
                return {
                    "success": False,
                    "error": "Could not fetch original message for forwarding"
                }
            
            original_message = response.json()
            
            # Extract original details
            headers_data = original_message['payload']['headers']
            original_subject = ""
            original_from = ""
            original_date = ""
            
            for header in headers_data:
                name = header['name'].lower()
                if name == 'subject':
                    original_subject = header['value']
                elif name == 'from':
                    original_from = header['value']
                elif name == 'date':
                    original_date = header['value']
            
            # Get original body (simplified)
            original_body = "Original message content"  # You'd implement body extraction here
            
            # Create forward subject
            forward_subject = original_subject
            if not forward_subject.lower().startswith('fwd:'):
                forward_subject = f"Fwd: {original_subject}"
            
            # Create forward body
            forward_body = ""
            if forward_message:
                forward_body += f"{forward_message}\n\n"
            
            forward_body += f"""
---------- Forwarded message ---------
From: {original_from}
Date: {original_date}
Subject: {original_subject}

{original_body}
"""
            
            # Send forwarded email
            return self.send_email(
                to=to,
                subject=forward_subject,
                body=forward_body
            )
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error forwarding email: {str(e)}"
            }
    
    def send_bulk_emails(
        self,
        recipients: List[str],
        subject: str,
        body: str,
        personalize: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Send emails to multiple recipients
        
        Args:
            recipients: List of recipient email addresses
            subject: Email subject
            body: Email body
            personalize: Whether to personalize each email
            
        Returns:
            List of result dictionaries for each sent email
        """
        results = []
        
        for recipient in recipients:
            try:
                # Personalize if requested
                personalized_body = body
                personalized_subject = subject
                
                if personalize:
                    # Extract name from email for personalization
                    name = recipient.split('@')[0].replace('.', ' ').title()
                    personalized_body = body.replace('[NAME]', name)
                    personalized_subject = subject.replace('[NAME]', name)
                
                # Send individual email
                result = self.send_email(
                    to=recipient,
                    subject=personalized_subject,
                    body=personalized_body
                )
                
                result['recipient'] = recipient
                results.append(result)
                
            except Exception as e:
                results.append({
                    "success": False,
                    "recipient": recipient,
                    "error": f"Failed to send to {recipient}: {str(e)}"
                })
        
        return results
    
    def schedule_email(
        self,
        to: str,
        subject: str,
        body: str,
        send_time: str
    ) -> Dict[str, Any]:
        """
        Schedule an email to be sent later (Note: Gmail API doesn't support scheduling directly)
        This is a placeholder for future implementation with external scheduling
        
        Args:
            to: Recipient email
            subject: Email subject  
            body: Email body
            send_time: When to send (ISO format)
            
        Returns:
            Result indicating scheduling status
        """
        return {
            "success": False,
            "error": "Email scheduling not yet implemented. Gmail API doesn't support native scheduling."
        }
    
    def save_draft(
        self,
        to: str,
        subject: str,
        body: str,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Save email as draft
        
        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body
            cc: CC recipients
            bcc: BCC recipients
            
        Returns:
            Result dictionary with draft info
        """
        try:
            access_token = self._get_access_token()
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            # Create the message
            raw_message = self._create_message(
                to=to,
                subject=subject,
                body=body,
                cc=cc,
                bcc=bcc
            )
            
            # Prepare draft payload
            draft_data = {
                "message": {
                    "raw": raw_message
                }
            }
            
            # Save as draft
            response = requests.post(
                f"{self.base_url}/drafts",
                headers=headers,
                data=json.dumps(draft_data),
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "draft_id": result.get("id"),
                    "message_id": result.get("message", {}).get("id"),
                    "recipient": to,
                    "subject": subject
                }
            else:
                return {
                    "success": False,
                    "error": f"Failed to save draft: {response.status_code} - {response.text}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Error saving draft: {str(e)}"
            }
    
    def send_draft_by_id(self, draft_id: str) -> Dict[str, Any]:
        """
        Send a previously saved draft
        
        Args:
            draft_id: ID of the draft to send
            
        Returns:
            Result dictionary with success status
        """
        try:
            access_token = self._get_access_token()
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            # Send the draft
            response = requests.post(
                f"{self.base_url}/drafts/{draft_id}/send",
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "message_id": result.get("id"),
                    "thread_id": result.get("threadId")
                }
            else:
                return {
                    "success": False,
                    "error": f"Failed to send draft: {response.status_code} - {response.text}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Error sending draft: {str(e)}"
            }
    
    def get_sent_emails(self, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        Get recently sent emails for confirmation
        
        Args:
            max_results: Maximum number of sent emails to retrieve
            
        Returns:
            List of sent email information
        """
        try:
            access_token = self._get_access_token()
            headers = {"Authorization": f"Bearer {access_token}"}
            
            # Query for sent emails
            params = {
                "q": "in:sent",
                "maxResults": max_results
            }
            
            response = requests.get(
                f"{self.base_url}/messages",
                headers=headers,
                params=params,
                timeout=15
            )
            
            if response.status_code == 200:
                message_list = response.json()
                sent_emails = []
                
                for message in message_list.get('messages', []):
                    # Get message details
                    detail_response = requests.get(
                        f"{self.base_url}/messages/{message['id']}",
                        headers=headers,
                        params={"format": "metadata"},
                        timeout=10
                    )
                    
                    if detail_response.status_code == 200:
                        message_data = detail_response.json()
                        headers_data = message_data['payload']['headers']
                        
                        email_info = {"id": message['id']}
                        for header in headers_data:
                            name = header['name'].lower()
                            if name in ['to', 'subject', 'date']:
                                email_info[name] = header['value']
                        
                        sent_emails.append(email_info)
                
                return sent_emails
            
            return []
            
        except Exception as e:
            print(f"Error fetching sent emails: {e}")
            return []
    
    def validate_email_address(self, email: str) -> bool:
        """
        Basic email address validation
        
        Args:
            email: Email address to validate
            
        Returns:
            True if email appears valid
        """
        import re
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        return re.match(pattern, email) is not None
    
    def get_sending_statistics(self) -> Dict[str, Any]:
        """
        Get basic sending statistics
        
        Returns:
            Dictionary with sending stats
        """
        try:
            sent_emails = self.get_sent_emails(50)  # Get more for better stats
            
            if not sent_emails:
                return {"total_sent": 0, "error": "No sent emails found"}
            
            # Basic statistics
            total_sent = len(sent_emails)
            recipients = set()
            
            for email in sent_emails:
                if 'to' in email:
                    recipients.add(email['to'])
            
            return {
                "total_sent_recently": total_sent,
                "unique_recipients": len(recipients),
                "average_per_recipient": total_sent / max(len(recipients), 1)
            }
            
        except Exception as e:
            return {"error": f"Could not fetch statistics: {str(e)}"}