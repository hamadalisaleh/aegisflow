from app.services.llm.gemini_provider import GeminiProvider

class RepositoryAnalyzerAgent:
    def __init__(self, provider: GeminiProvider | None = None):
        self.provider = provider or GeminiProvider()
        self.system_prompt = (
            "You are AegisFlow Code Reviewer and Security Specialist. "
            "Analyze the given repository details or source code. "
            "Provide: 1) Architecture overview, 2) Security concerns, 3) Recommended improvements."
        )

    def analyze(self, repo_url_or_code: str) -> dict:
        prompt = f"Please inspect and analyze this repository / code input:\n\n{repo_url_or_code}"
        llm_response = self.provider.generate(prompt=prompt, system_prompt=self.system_prompt)
        
        return {
            "summary": llm_response.content,
            "metrics": {
                "prompt_tokens": llm_response.prompt_tokens,
                "completion_tokens": llm_response.completion_tokens,
                "total_tokens": llm_response.total_tokens,
                "latency_ms": round(llm_response.latency_ms, 2)
            }
        }