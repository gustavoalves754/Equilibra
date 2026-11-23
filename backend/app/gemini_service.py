"""Integração isolada com o SDK Python do Gemini."""

from google import genai

from .prompts import build_wellbeing_prompt


class GeminiServiceError(RuntimeError):
    """Erro controlado da integração com o serviço externo."""


def generate_wellbeing_guidance(
    profile: dict,
    *,
    api_key: str,
    model: str,
) -> str:
    """Envia o perfil ao Gemini e devolve o texto da orientação."""
    if not api_key:
        raise GeminiServiceError("GEMINI_API_KEY não configurada.")
    if not model:
        raise GeminiServiceError("Modelo Gemini não configurado.")

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=model,
            contents=build_wellbeing_prompt(profile),
        )
        text = response.text
    except Exception as error:
        raise GeminiServiceError("Falha ao comunicar com o Gemini.") from error

    if not isinstance(text, str) or not text.strip():
        raise GeminiServiceError("O Gemini retornou uma resposta vazia ou inválida.")

    return text.strip()
