from pydantic import BaseModel

class TemplateResponse(BaseModel):
    id: int
    name: str
    email_subject: str
    email_body: str
    edu_page_content: str

    class Config:
        from_attributes = True