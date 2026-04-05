import os
import json
from openai import OpenAI


def get_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY não encontrada no .env")
    return OpenAI(api_key=api_key)


def get_model() -> str:
    return os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


def score_lead_with_ai(
    description: str,
    name: str | None = None,
    email: str | None = None,
    company: str | None = None,
) -> dict:
    client = get_client()
    model = get_model()

    prompt = f"""
Você é um analista comercial B2B.

Analise o lead abaixo e devolva APENAS um JSON válido com esta estrutura:
{{
  "score": 0,
  "intent": "alto|medio|baixo",
  "summary": "resumo curto em português",
  "recommended_action": "ação recomendada em português"
}}

Regras:
- score deve ser inteiro de 0 a 100
- intent deve ser apenas: alto, medio ou baixo
- summary deve ter no máximo 200 caracteres
- recommended_action deve ter no máximo 150 caracteres

Dados do lead:
Nome: {name or ""}
Email: {email or ""}
Empresa: {company or ""}
Descrição: {description or ""}
""".strip()

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "Você analisa leads e retorna somente JSON válido.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.2,
    )

    content = response.choices[0].message.content.strip()

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        # fallback seguro
        data = {
            "score": 50,
            "intent": "medio",
            "summary": "Lead analisado com fallback por falha na resposta estruturada.",
            "recommended_action": "Revisar lead manualmente e entrar em contato.",
        }

    return {
        "score": int(data.get("score", 50)),
        "intent": str(data.get("intent", "medio")).lower(),
        "summary": str(data.get("summary", ""))[:200],
        "recommended_action": str(data.get("recommended_action", ""))[:150],
    }