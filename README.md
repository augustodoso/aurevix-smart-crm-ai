# 🚀 Aurevix Smart CRM AI

Sistema de **Lead Scoring com Inteligência Artificial integrado ao Salesforce**, capaz de analisar automaticamente novos leads e sugerir ações comerciais.

---

## 💡 Visão geral

Este projeto conecta uma API de IA desenvolvida em **FastAPI + OpenAI** com o **Salesforce**, utilizando **Apex (Trigger + Queueable)** para processamento automático de leads.

👉 Sempre que um novo Lead é criado:

* A IA analisa o conteúdo
* Classifica o nível de interesse (score)
* Gera um resumo
* Sugere a próxima ação

Tudo isso **sem intervenção manual**.

---

## ⚙️ Arquitetura

```text
Salesforce (Lead)
   ↓
Trigger (Apex)
   ↓
Queueable (Async)
   ↓
HTTP Callout
   ↓
FastAPI (Render)
   ↓
OpenAI (análise)
   ↓
Resposta estruturada
   ↓
Atualização do Lead no Salesforce
```

---

## 🧠 Tecnologias utilizadas

* Python (FastAPI)
* OpenAI API
* Salesforce Apex
* Queueable Jobs
* HTTP Callout
* Render (deploy)
* REST API

---

## 🔗 Endpoint principal

```http
POST /salesforce/score-lead
```

### Exemplo de request:

```json
{
  "lead_id": "00QTESTE123",
  "description": "Quero contratar uma solução de IA para atendimento comercial",
  "name": "Augusto",
  "email": "augusto@email.com",
  "company": "Aurevix Tech"
}
```

### Exemplo de response:

```json
{
  "lead_id": "00QTESTE123",
  "score": 85,
  "intent": "alto",
  "summary": "Lead interessado em solução de IA para atendimento comercial.",
  "recommended_action": "Entrar em contato rapidamente para apresentar soluções."
}
```

---

## 🌐 API em produção

👉 https://aurevix-smart-crm-ai.onrender.com/docs

---

## 📊 Resultado

* Leads analisados automaticamente
* Classificação inteligente de interesse
* Sugestão de ação comercial
* Redução de esforço manual no CRM

---

## 🚀 Diferenciais

* Integração real com Salesforce
* Processamento assíncrono (Queueable)
* IA aplicada a fluxo de negócio
* Deploy em produção
* Arquitetura escalável

---

## 📸 Demonstração

👉 (adicione prints do Swagger e do Salesforce aqui)

---

## 👨‍💻 Autor

**Augusto Cezar de Macedo Doso**
AI & Automation Developer
GitHub: https://github.com/augustodoso

---

## 📌 Próximos passos

* Reanálise de leads sob demanda
* Dashboard de score
* Histórico de análises
* Interface com LWC
