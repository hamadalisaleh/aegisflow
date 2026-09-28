import os
import time
from google import genai
from app.services.llm.base import BaseLLMProvider, LLMResponse

class GeminiProvider(BaseLLMProvider):
    def __init__(self, api_key: str | None = None, model_name: str = "gemini-2.5-flash"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "")
        self.model_name = model_name
        self.client = genai.Client(api_key=self.api_key) if self.api_key else None

    def generate(self, prompt: str, system_prompt: str | None = None) -> LLMResponse:
        start_time = time.time()
        
        # محاكاة في حالة عدم وجود مفتاح API أثناء التطوير أو الاختبار
        if not self.client:
            return LLMResponse(
                content="[Mock Analysis] No GEMINI_API_KEY provided. Repository analyzed: Structure is valid, no critical security flaws found.",
                prompt_tokens=10,
                completion_tokens=20,
                total_tokens=30,
                latency_ms=(time.time() - start_time) * 1000
            )

        config = {}
        if system_prompt:
            config["system_instruction"] = system_prompt

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=config if config else None
        )
        latency = (time.time() - start_time) * 1000

        # استخراج عدد التوكنات إن توفرت
        usage = getattr(response, "usage_metadata", None)
        prompt_tokens = getattr(usage, "prompt_token_count", 0) if usage else 0
        candidates_tokens = getattr(usage, "candidates_token_count", 0) if usage else 0

        return LLMResponse(
            content=response.text or "",
            prompt_tokens=prompt_tokens,
            completion_tokens=candidates_tokens,
            total_tokens=prompt_tokens + candidates_tokens,
            latency_ms=latency
        )