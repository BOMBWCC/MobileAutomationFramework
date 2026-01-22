import requests
import json
from typing import Dict, Any
from utils.logger import logger
from config.global_config import GlobalConfig

class NotifyHelper:
    """
    Message Notification Center.
    Supports Lark (Feishu) and DingTalk.
    """

    @staticmethod
    def _post_webhook(url: str, payload: Dict[str, Any]) -> bool:
        """[Low-level Sender]"""
        headers = {"Content-Type": "application/json"}
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()
            return True
        except Exception as e:
            logger.error(f"Failed to send webhook notification: {e}")
            return False

    @staticmethod
    def _format_lark_card(summary: Dict[str, Any]) -> Dict[str, Any]:
        """[Feishu/Lark Card]"""
        failed_count = summary.get('failed', 0)
        color = "red" if failed_count > 0 else "green"
        title = "UI Automation Report"
        
        elements = [
            {"tag": "div", "text": {"tag": "lark_md", "content": f"**Environment:** {GlobalConfig.PLATFORM_NAME}"}},
            {"tag": "div", "text": {"tag": "lark_md", "content": f"**Total:** {summary.get('total', 0)}"}},
            {"tag": "div", "text": {"tag": "lark_md", "content": f"**Passed:** {summary.get('passed', 0)}"}},
            {"tag": "div", "text": {"tag": "lark_md", "content": f"**Failed:** {failed_count}"}},
        ]

        card = {
            "msg_type": "interactive",
            "card": {
                "config": {"wide_screen_mode": True},
                "header": {
                    "title": {"tag": "plain_text", "content": title},
                    "template": color
                },
                "elements": elements
            }
        }
        return card

    @staticmethod
    def _format_dingtalk_md(summary: Dict[str, Any]) -> Dict[str, Any]:
        """[DingTalk Markdown]"""
        title = "UI Automation Report"
        text = f"### {title}\n"
        text += f"- **Environment**: {GlobalConfig.PLATFORM_NAME}\n"
        text += f"- **Total**: {summary.get('total', 0)}\n"
        text += f"- **Passed**: {summary.get('passed', 0)}\n"
        text += f"- **Failed**: {summary.get('failed', 0)}\n"
        
        if summary.get('report_url'):
            text += f"\n[View Report]({summary['report_url']})"

        return {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": text
            }
        }

    @staticmethod
    def send_test_report(summary_data: Dict[str, Any], webhook_url: str = None):
        """
        [Main Entry Point]
        Sends test report to the configured webhook.
        """
        # Ideally, getting URL from config if not provided
        # For now, we assume it's passed in or we check config
        target_url = webhook_url
        
        # NOTE: Since GlobalConfig doesn't have WEBHOOK_URL defined in our skeleton yet, 
        # we would typically fetch it here.
        # target_url = target_url or GlobalConfig.WEBHOOK_URL
        
        if not target_url:
            logger.warning("No Webhook URL provided. Skipping notification.")
            return

        # Determine type based on URL (simple heuristic)
        if "feishu" in target_url or "lark" in target_url:
            payload = NotifyHelper._format_lark_card(summary_data)
        else:
            payload = NotifyHelper._format_dingtalk_md(summary_data)
            
        success = NotifyHelper._post_webhook(target_url, payload)
        if success:
            logger.info("Test report pushed to group chat.")
