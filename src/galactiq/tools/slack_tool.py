from crewai.tools import BaseTool
from typing import Type, Dict, Any
from pydantic import BaseModel, Field, ConfigDict
import slack_sdk
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
import os

load_dotenv()
slack_token =  os.getenv("SLACK_BOT_TOKEN")


class SlackMessageSchema(BaseModel):
    channel: str = Field(..., description="Channel or user ID to send the message to")
    message: str = Field(..., description="Content of the message to send")
    thread_ts: str = Field(None, description="Thread timestamp to reply to (optional)")

class SlackTool(BaseTool):
    """Tool to send messages via Slack API"""
    name: str = "SendSlack"
    description: str = "Send a message using Slack API."
    args_schema: Type[BaseModel] = SlackMessageSchema
    model_config = ConfigDict(arbitrary_types_allowed=True)
    client: slack_sdk.WebClient = None
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client = slack_sdk.WebClient(token=slack_token)

    def _run(self, channel: str, message: str, thread_ts: str = None) -> str:
        """
        Sends a message using Slack API.

        Parameters:
            channel (str): Channel or user ID to send the message to
            message (str): Content of the message
            thread_ts (str, optional): Thread timestamp to reply to

        Returns:
            str: Success or failure message
        """
        try:
            # Prepare message payload
            message_payload = {
                "channel": channel,
                "text": message
            }
            
            # Add thread_ts if provided
            if thread_ts:
                message_payload["thread_ts"] = thread_ts

            # Send the message
            response = self.client.chat_postMessage(**message_payload)

            return {
                "status": "success",
                "message": "Slack message sent successfully",
                "timestamp": response["ts"],
                "channel": response["channel"]
            }

        except SlackApiError as e:
            return f"Error sending Slack message: {str(e.response['error'])}"
        except Exception as e:
            return f"Error sending Slack message: {str(e)}"