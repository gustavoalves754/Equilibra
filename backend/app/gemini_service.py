"""Integração isolada com o SDK Python do Gemini."""

from typing import NamedTuple

from google import genai

from .prompts import build_wellbeing_prompt


class GeminiServiceError(RuntimeError):
    """Erro controlado da integração com o serviço externo."""


class GeminiGuidance(NamedTuple):
    """Texto gerado e modelo que respondeu à solicitação."""

    text: str
    model: str


def generate_wellbeing_guidance(
    profile: dict,
    *,
    api_key: str,
    models: list[str] | tuple[str, ...],
) -> GeminiGuidance:
    """Tenta os modelos configurados, em ordem, até obter uma orientação."""
    if not api_key:
        raise GeminiServiceError("GEMINI_API_KEY não configurada.")
    if not models:
        raise GeminiServiceError("Nenhum modelo Gemini foi configurado.")

    try:
        client = genai.Client(api_key=api_key)
    except Exception as error:
        raise GeminiServiceError("Falha ao iniciar o cliente Gemini.") from error

    prompt = build_wellbeing_prompt(profile)
    last_error: Exception | None = None

    for model in models:
        try:
            response = client.models.generate_content(model=model, contents=prompt)
            text = response.text
            if not isinstance(text, str) or not text.strip():
                raise GeminiServiceError(
                    f"O modelo {model} retornou uma resposta vazia ou inválida."
                )
            return GeminiGuidance(text=text.strip(), model=model)
        except Exception as error:
            last_error = error

    raise GeminiServiceError(
        "Não foi possível consultar nenhum dos modelos Gemini configurados."
    ) from last_error
