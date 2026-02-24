import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

def build_llm(provider: str, model: str | None, temperature: float = 0.0):
    if provider.lower() == "gemini":
        api_key = os.getenv("GEMINI_API")
        return ChatGoogleGenerativeAI(
            model=model or "gemini-1.5-pro", 
            temperature=temperature, 
            google_api_key=api_key,
            max_output_tokens=8192
        )
    elif provider.lower() == "groq":
        api_key = os.getenv("GROQ_API")
        return ChatGroq(
            model_name=model or "llama-3.3-70b-versatile", 
            temperature=temperature, 
            groq_api_key=api_key
        )
    elif provider.lower() == "anthropic":
        from langchain_anthropic import ChatAnthropic
        api_key = os.getenv("ANTHROPIC_API_KEY") or os.getenv("CLAUDE_API")
        return ChatAnthropic(
            model=model or "claude-3-5-sonnet-20240620",
            temperature=temperature,
            anthropic_api_key=api_key,
            max_tokens=8000
        )
    else:
        raise ValueError(f"Unsupported provider: {provider}")
