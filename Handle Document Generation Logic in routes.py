backend/
├── routes.py
├── services/
│   ├── document_generator.py
│   └── ai_service.py
├── models/
│   └── document.py
├── schemas/
│   └── document.py
└── tests/
    └── test_document_generation.py

routes.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from services.document_generator import generate_legal_document

router = APIRouter(prefix="/documents", tags=["Documents"])


class DocumentGenerationRequest(BaseModel):
    document_type: str = Field(..., min_length=2)
    jurisdiction: str = Field(..., min_length=2)
    parties: list[str] = Field(default_factory=list)
    requirements: str = Field(..., min_length=10)


class DocumentGenerationResponse(BaseModel):
    document_type: str
    jurisdiction: str
    content: str


@router.post(
    "/generate",
    response_model=DocumentGenerationResponse
)
async def generate_document(request: DocumentGenerationRequest):
    """
    Generate an AI-powered legal document from user requirements.
    """

    try:
        content = await generate_legal_document(
            document_type=request.document_type,
            jurisdiction=request.jurisdiction,
            parties=request.parties,
            requirements=request.requirements,
        )

        if not content:
            raise HTTPException(
                status_code=500,
                detail="Document generation returned empty content."
            )

        return DocumentGenerationResponse(
            document_type=request.document_type,
            jurisdiction=request.jurisdiction,
            content=content,
        )

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Document generation failed: {str(exc)}",
        )

services/document_generator.py
Keep the AI logic out of routes.py:

async def generate_legal_document(
    document_type: str,
    jurisdiction: str,
    parties: list[str],
    requirements: str,
) -> str:

    prompt = f"""
Generate a legal document based on the following information.

Document Type:
{document_type}

Jurisdiction:
{jurisdiction}

Parties:
{", ".join(parties)}

Requirements:
{requirements}

Instructions:
- Use clear and professional legal language.
- Structure the document with appropriate headings and clauses.
- Do not invent facts that were not provided.
- Clearly identify placeholders for missing information.
- Return only the document content.
"""

    # Connect this to your configured LLM provider.
    response = await call_ai_model(prompt)

    return response

Example API request
POST /documents/generate
Content-Type: application/json

{
  "document_type": "Rental Agreement",
  "jurisdiction": "Tamil Nadu, India",
  "parties": [
    "Landlord: John Doe",
    "Tenant: Jane Doe"
  ],
  "requirements": "One-year residential rental agreement with monthly rent of ₹20,000 and a two-month security deposit."
}

Expected response
{
  "document_type": "Rental Agreement",
  "jurisdiction": "Tamil Nadu, India",
  "content": "RESIDENTIAL RENTAL AGREEMENT\n\n..."
}

For EPIC 3, I would structure the implementation around this flow:

Frontend
   ↓
POST /documents/generate
   ↓
routes.py
   ↓
Validate request
   ↓
document_generator service
   ↓
AI model
   ↓
Generated legal document
   ↓
routes.py
   ↓
JSON response
