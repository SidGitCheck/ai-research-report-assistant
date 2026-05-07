from __future__ import annotations

import json

import requests


class LLMClient:
    def __init__(self, provider: str, model: str, ollama_base_url: str, groq_api_key: str = "") -> None:
        self.provider = provider
        self.model = model
        self.ollama_base_url = ollama_base_url
        self.groq_api_key = groq_api_key

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        if self.provider == "mock":
            return self._generate_mock(prompt=prompt, system_prompt=system_prompt)
        if self.provider == "groq":
            return self._generate_groq(prompt=prompt, system_prompt=system_prompt)
        try:
            return self._generate_ollama(prompt=prompt, system_prompt=system_prompt)
        except requests.RequestException:
            return self._generate_mock(prompt=prompt, system_prompt=system_prompt)

    def _generate_ollama(self, prompt: str, system_prompt: str = "") -> str:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "system": system_prompt,
            "stream": False,
        }
        response = requests.post(f"{self.ollama_base_url}/api/generate", json=payload, timeout=90)
        response.raise_for_status()
        return response.json().get("response", "")

    def _generate_groq(self, prompt: str, system_prompt: str = "") -> str:
        if not self.groq_api_key:
            raise RuntimeError("GROQ_API_KEY not set.")
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt or "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
        }
        headers = {"Authorization": f"Bearer {self.groq_api_key}", "Content-Type": "application/json"}
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            data=json.dumps(payload),
            timeout=90,
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    def _generate_mock(self, prompt: str, system_prompt: str = "") -> str:
        prompt_lower = prompt.lower()
        if "return only valid json" in prompt_lower and "json schema" in prompt_lower:
            return json.dumps(
                {
                    "topic": self._extract_topic(prompt),
                    "sections": [
                        {
                            "title": "BERT Overview",
                            "query_strategy": [
                                "BERT architecture encoder-only transformer",
                                "BERT pretraining masked language model next sentence prediction",
                            ],
                            "required_sources": 2,
                        },
                        {
                            "title": "GPT Overview",
                            "query_strategy": [
                                "GPT architecture decoder-only transformer",
                                "GPT autoregressive language modeling training objective",
                            ],
                            "required_sources": 2,
                        },
                        {
                            "title": "BERT vs GPT Comparison",
                            "query_strategy": [
                                "BERT vs GPT differences encoder decoder bidirectional autoregressive",
                                "when to use BERT vs GPT",
                            ],
                            "required_sources": 2,
                        },
                    ],
                    "retrieval_budget": {"max_sources": 8, "max_chunks_total": 30},
                    "evaluation_rubric": ["coverage", "citation_quality", "clarity", "correctness"],
                }
            )
        if "write a concise markdown section titled" in prompt_lower:
            title = self._extract_title(prompt)
            title_lower = title.lower()
            if "bert overview" in title_lower:
                return (
                    "- BERT is encoder-only and uses bidirectional attention, which makes it strong for contextual understanding [bert_chunk_1].\n"
                    "- Its pretraining objective (masked language modeling) is optimized for representation learning rather than free-form generation [bert_chunk_1].\n"
                    "- Typical use-cases include classification, NER, and extractive QA pipelines [cmp_chunk_1]."
                )
            if "gpt overview" in title_lower:
                return (
                    "- GPT is decoder-only and predicts the next token autoregressively, which naturally supports generation workflows [gpt_chunk_1].\n"
                    "- Instruction tuning and chat alignment make GPT-style models practical for assistants and content generation [gpt_chunk_1].\n"
                    "- GPT models are commonly selected when output fluency and multi-turn generation are priorities [cmp_chunk_1]."
                )
            return (
                "- BERT and GPT differ in transformer directionality: bidirectional encoding vs autoregressive decoding [bert_chunk_1] [gpt_chunk_1].\n"
                "- Choose BERT for understanding-centric tasks and GPT for generation-centric tasks [cmp_chunk_1].\n"
                "- Hybrid systems often use both: BERT-like retrievers and GPT-like generators in RAG pipelines [cmp_chunk_1]."
            )
        if "review this markdown report against rubric" in prompt_lower:
            return "- Coverage is acceptable.\n- Add one clearer sentence on bidirectional vs autoregressive objective.\n- Citations appear present in core sections."
        return "Mock response generated due to unavailable external LLM runtime."

    @staticmethod
    def _extract_topic(prompt: str) -> str:
        marker = "Create a research plan for topic:"
        if marker in prompt:
            return prompt.split(marker, maxsplit=1)[1].splitlines()[0].strip()
        return "Research Topic"

    @staticmethod
    def _extract_title(prompt: str) -> str:
        marker = 'titled "'
        if marker in prompt:
            return prompt.split(marker, maxsplit=1)[1].split('"', maxsplit=1)[0]
        return "Section"
