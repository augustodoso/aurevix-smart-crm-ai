# Aurevix Smart CRM Assistant 🚀

Assistente inteligente que automatiza a criação de leads no Salesforce usando IA.

---

## 💡 O que faz

- Analisa mensagens de clientes com IA  
- Classifica intenção (lead, suporte ou dúvida)  
- Captura dados (nome, email, empresa)  
- Cria automaticamente um Lead no Salesforce  
- Retorna o ID do registro  

---

## 🧠 Arquitetura

Frontend → FastAPI → OpenAI → Salesforce API

---

## 🛠️ Stack

- Python + FastAPI  
- OpenAI API  
- Salesforce REST API  
- HTML / JavaScript  

---

## ⚙️ Como rodar

```bash
git clone https://github.com/seu-usuario/aurevixassistantoauth
cd aurevix-smart-crm-ai
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pip install email-validator
python -m uvicorn app.main:app --reload --port 8001

Acesse:
http://127.0.0.1:8001/docs

{
  "text": "Quero contratar o serviço",
  "name": "Seu Nome",
  "email": "email@email.com",
  "company": "Sua Empresa"
}