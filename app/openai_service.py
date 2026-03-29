import os
from openai import OpenAI


def get_client():
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OPENAI_API_KEY não encontrada no .env")

    return OpenAI(api_key=api_key)


def get_model():
    return os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


def classify_message(text: str) -> str:
    client = get_client()
    model = get_model()

    prompt = f"""
Classifique a intenção da mensagem do usuário em apenas uma destas categorias:

- lead = quando a pessoa quer comprar, contratar, saber preço, orçamento, plano, proposta ou demonstra interesse comercial
- suporte = quando relata problema, erro, falha, bug, acesso ou login
- duvida = pergunta geral sem intenção clara de compra ou suporte

Responda APENAS com uma palavra:
lead
suporte
duvida

Mensagem:
{text}
""".strip()

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Você classifica intenções de clientes com precisão."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    content = response.choices[0].message.content.strip().lower()

    if "lead" in content:
        return "lead"
    if "suporte" in content:
        return "suporte"
    return "duvida"


def generate_reply(text: str, intent: str, has_lead_data: bool = False) -> str:
    client = get_client()
    model = get_model()

    extra = ""
    if intent == "lead" and not has_lead_data:
        extra = """
Peça educadamente nome, email e empresa do interessado para seguir com o atendimento comercial.
"""
    elif intent == "lead" and has_lead_data:
        extra = """
Agradeça o envio dos dados e diga que o contato foi registrado com sucesso no CRM.
"""

    prompt = f"""
Você é um assistente comercial educado.
Responda em português, de forma curta e profissional.

Intenção detectada: {intent}
Mensagem do usuário: {text}

Regras adicionais:
{extra}
""".strip()

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Você responde clientes de forma breve, profissional e clara."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )

    return response.choices[0].message.content.strip()