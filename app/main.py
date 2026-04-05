from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from app.schemas import (
    ChatMessageIn,
    ChatMessageOut,
    LeadScoreRequest,
    LeadScoreResponse,
)
from app.openai_service import classify_message, generate_reply
from app.salesforce_service import create_lead, get_access_token
from app.storage import save_log
from app.lead_ai_service import score_lead_with_ai

app = FastAPI(title="Aurevix Smart CRM Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "API rodando"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/test-salesforce")
def test_salesforce():
    try:
        data = get_access_token()
        return {
            "success": True,
            "instance_url": data.get("instance_url"),
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }


@app.post("/chat", response_model=ChatMessageOut)
def chat(payload: ChatMessageIn):
    text = payload.text.strip()
    intent = classify_message(text)

    salesforce_created = False
    lead_id = None
    has_lead_data = bool(payload.name and payload.email and payload.company)

    if intent == "lead" and has_lead_data:
        try:
            sf_response = create_lead(
                description=text,
                name=payload.name,
                email=payload.email,
                company=payload.company,
            )
            salesforce_created = True
            lead_id = sf_response.get("id")
        except Exception as exc:
            reply = f"Entendi seu interesse. Houve uma falha ao registrar no CRM: {exc}"
            save_log(
                user_text=text,
                intent=intent,
                reply=reply,
                salesforce_created=salesforce_created,
                name=payload.name,
                email=payload.email,
                company=payload.company,
                lead_id=lead_id,
            )
            return ChatMessageOut(
                intent=intent,
                reply=reply,
                salesforce_created=salesforce_created,
                lead_id=lead_id,
            )

    reply = generate_reply(text, intent, has_lead_data=has_lead_data)

    save_log(
        user_text=text,
        intent=intent,
        reply=reply,
        salesforce_created=salesforce_created,
        name=payload.name,
        email=payload.email,
        company=payload.company,
        lead_id=lead_id,
    )

    return ChatMessageOut(
        intent=intent,
        reply=reply,
        salesforce_created=salesforce_created,
        lead_id=lead_id,
    )


@app.post("/salesforce/score-lead", response_model=LeadScoreResponse)
def score_lead(payload: LeadScoreRequest):
    result = score_lead_with_ai(
        description=payload.description or "",
        name=payload.name,
        email=payload.email,
        company=payload.company,
    )

    return LeadScoreResponse(
        lead_id=payload.lead_id,
        score=result["score"],
        intent=result["intent"],
        summary=result["summary"],
        recommended_action=result["recommended_action"],
    )