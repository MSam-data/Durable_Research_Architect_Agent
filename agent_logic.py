import time
from google import genai
from google.genai import types
from google.api_core import exceptions
from tools import web_search

class ResearchAgent:
    def __init__(self, api_key: str, model_id: str):
        self.client = genai.Client(api_key=api_key)
        self.model_id = model_id

    def _call_with_retry(self, func, *args, **kwargs):
        """
        Internal helper to handle 503 (Server Busy) errors automatically.
        """
        max_retries = 3
        for i in range(max_retries):
            try:
                # Add a small base delay to respect rate limits
                time.sleep(2) 
                return func(*args, **kwargs)
            except exceptions.ServiceUnavailable:
                print(f"   ⚠️ Server busy (503). Retrying in {5 * (i + 1)}s...")
                time.sleep(5 * (i + 1))
            except Exception as e:
                raise e
        raise Exception("Google servers are currently too busy. Please try again in a few minutes.")

    def plan_task(self, goal: str):
        prompt = f"Break down this goal into 3 specific search queries: {goal}. Return only the queries."
        return self._call_with_retry(
            self.client.models.generate_content,
            model=self.model_id,
            contents=prompt
        ).text

    def execute_research(self, plan: str):
        prompt = f"Using the search tool, research this plan: {plan}. Summarize findings."
        return self._call_with_retry(
            self.client.models.generate_content,
            model=self.model_id,
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=[web_search]
            )
        ).text

    def finalize_report(self, data: str):
        prompt = f"Based on this data: {data}, write a professional executive summary."
        return self._call_with_retry(
            self.client.models.generate_content,
            model=self.model_id,
            contents=prompt
        ).text