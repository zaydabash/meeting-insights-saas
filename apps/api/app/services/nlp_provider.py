from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from app.core.config import settings
import time
import json
import asyncio


class LLMProvider(ABC):
    @abstractmethod
    async def extract_insights(
        self, text: str, context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_cost_estimate(self, tokens_in: int, tokens_out: int) -> float:
        pass


class MockProvider(LLMProvider):
    """Deterministic mock provider for local dev and testing"""

    async def extract_insights(
        self, text: str, context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        # Simulate processing time
        await asyncio.sleep(0.1)
        
        # Simple deterministic extraction
        action_items = []
        decisions = []
        sentiment = 0.0
        
        text_lower = text.lower()
        
        # Extract action items (look for "need to", "should", "will")
        if "need to" in text_lower or "should" in text_lower:
            action_items.append({
                "text": "Follow up on discussed items",
                "owner_candidate": None,
                "due_date_candidate": None,
                "confidence": 0.7
            })
        
        # Extract decisions (look for "decided", "agreed", "approved")
        if "decided" in text_lower or "agreed" in text_lower:
            decisions.append({
                "text": "Decision made during meeting",
                "confidence": 0.8
            })
        
        # Simple sentiment (very basic)
        positive_words = ["good", "great", "excellent", "yes", "agree"]
        negative_words = ["bad", "no", "disagree", "problem", "issue"]
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)
        if pos_count + neg_count > 0:
            sentiment = (pos_count - neg_count) / (pos_count + neg_count)
        
        summary = f"Meeting discussed: {text[:200]}..." if len(text) > 200 else text
        
        return {
            "action_items": action_items,
            "decisions": decisions,
            "sentiment": sentiment,
            "summary": summary,
            "topics": ["General Discussion"],
            "tokens_in": len(text.split()) * 1.3,  # Rough estimate
            "tokens_out": 500,
        }

    def get_cost_estimate(self, tokens_in: int, tokens_out: int) -> float:
        return 0.0  # Free for mock


class OpenAIProvider(LLMProvider):
    def __init__(self, api_key: str):
        try:
            import openai
            self.client = openai.AsyncOpenAI(api_key=api_key)
        except ImportError:
            raise ImportError("openai package not installed")

    async def extract_insights(
        self, text: str, context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        prompt = f"""Extract insights from this meeting transcript. Return JSON with:
- action_items: list of {{text, owner_candidate, due_date_candidate, confidence}}
- decisions: list of {{text, confidence}}
- sentiment: float between -1 and 1
- summary: string (max 6 sentences)
- topics: list of strings

Transcript:
{text}
"""
        
        response = await self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
        )
        
        result = json.loads(response.choices[0].message.content)
        
        return {
            **result,
            "tokens_in": response.usage.prompt_tokens,
            "tokens_out": response.usage.completion_tokens,
        }

    def get_cost_estimate(self, tokens_in: int, tokens_out: int) -> float:
        # GPT-4 Turbo pricing (approximate)
        input_cost = (tokens_in / 1000) * 0.01
        output_cost = (tokens_out / 1000) * 0.03
        return input_cost + output_cost


class AnthropicProvider(LLMProvider):
    def __init__(self, api_key: str):
        try:
            import anthropic
            self.client = anthropic.AsyncAnthropic(api_key=api_key)
        except ImportError:
            raise ImportError("anthropic package not installed")

    async def extract_insights(
        self, text: str, context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        prompt = f"""Extract insights from this meeting transcript. Return JSON with:
- action_items: list of {{text, owner_candidate, due_date_candidate, confidence}}
- decisions: list of {{text, confidence}}
- sentiment: float between -1 and 1
- summary: string (max 6 sentences)
- topics: list of strings

Transcript:
{text}
"""
        
        message = await self.client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}],
        )
        
        content = message.content[0].text
        result = json.loads(content)
        
        return {
            **result,
            "tokens_in": message.usage.input_tokens,
            "tokens_out": message.usage.output_tokens,
        }

    def get_cost_estimate(self, tokens_in: int, tokens_out: int) -> float:
        # Claude 3 Opus pricing (approximate)
        input_cost = (tokens_in / 1000) * 0.015
        output_cost = (tokens_out / 1000) * 0.075
        return input_cost + output_cost


def get_provider() -> LLMProvider:
    provider_name = settings.llm_provider.lower()
    
    if provider_name == "mock":
        return MockProvider()
    elif provider_name == "openai":
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY not set")
        return OpenAIProvider(settings.openai_api_key)
    elif provider_name == "anthropic":
        if not settings.anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY not set")
        return AnthropicProvider(settings.anthropic_api_key)
    else:
        raise ValueError(f"Unknown provider: {provider_name}")

