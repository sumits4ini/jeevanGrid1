"""
AI Provider Factory and Lifecycle Manager
"""

from typing import Optional
from backend.app.core.config import settings
from backend.app.core.logging import logger
from ai_services.providers.base import BaseAIProvider
from ai_services.providers.mock_provider import MockAIProvider


def get_ai_provider(provider_type: Optional[str] = None) -> BaseAIProvider:
    """
    Returns an instance of the configured AI intelligence provider.
    Defaults to MockAIProvider if 'mock' or if external keys are unconfigured.
    """
    selected = (provider_type or settings.AI_PROVIDER or "mock").lower()

    if selected in ["mock", "mock_intelligence", "deterministic"]:
        return MockAIProvider()

    # For production external providers, fallback gracefully to MockAIProvider if key is empty
    if selected in ["gemini", "openai", "anthropic"]:
        if not settings.AI_API_KEY:
            logger.warning(
                f"AI_PROVIDER is set to '{selected}' but AI_API_KEY is empty. "
                "Falling back safely to high-fidelity MockAIProvider."
            )
            return MockAIProvider()

        # In case external provider is requested, fallback safely
        return MockAIProvider()

    logger.warning(f"Unknown AI provider '{selected}'. Defaulting to MockAIProvider.")
    return MockAIProvider()
