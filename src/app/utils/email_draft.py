from src.app.utils.issue_summarizer import IssueSummarizer

class EmailDraftUtil:
    def __init__(self, summarizer=None) -> None:
        # If no summarizer is provided, instantiate one directly
        if summarizer is None:
            summarizer = IssueSummarizer()
        self.summarizer = summarizer.summarize_issue
        
    def generate_email_content(self, complaint):
        summarized_issue = self.summarizer(complaint.issue)
        
        subject = "Urgent: Buyer Complaint Regarding Product Issue"
        body = f"""
        Hello Admin,

        A Buyer (User ID: {complaint.user_id}) has reported an issue with their order.

        Order ID: {complaint.order_id}
        Product ID: {complaint.product_id}
        
        **Issue Summary:** {summarized_issue}
        Uploaded Image (if any): {complaint.image_url}

        Please review the complaint and take necessary action.

        Best Regards,
        Customer Support Team
        """
        return subject, body
