from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, TIMESTAMP, ForeignKey, CHAR
from sqlalchemy.orm import relationship
from app.core.database import Base

class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    campaigns = relationship("Campaign", back_populates="admin")


class TargetUser(Base):
    __tablename__ = "target_users"

    id = Column(Integer, primary_key=True, index=True)
    user_hash = Column(String(64), unique=True, nullable=False, index=True)
    department = Column(String(100), nullable=False, index=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    trackings = relationship("CampaignTracking", back_populates="target_user")


class Template(Base):
    __tablename__ = "templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email_subject = Column(String(200), nullable=False)
    email_body = Column(Text, nullable=False)
    edu_page_content = Column(Text, nullable=False)

    campaigns = relationship("Campaign", back_populates="template")
    quiz_questions = relationship("QuizQuestion", back_populates="template")


class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    admin_id = Column(Integer, ForeignKey("admins.id", ondelete="SET NULL"), nullable=True)
    template_id = Column(Integer, ForeignKey("templates.id", ondelete="CASCADE"), nullable=False)
    target_department = Column(String(100), nullable=False)
    status = Column(String(20), default="DRAFT")  # DRAFT, ACTIVE, FINISHED
    scheduled_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    admin = relationship("Admin", back_populates="campaigns")
    template = relationship("Template", back_populates="campaigns")
    trackings = relationship("CampaignTracking", back_populates="campaign", cascade="all, delete-orphan")


class CampaignTracking(Base):
    __tablename__ = "campaign_tracking"

    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("target_users.id", ondelete="CASCADE"), nullable=False)
    tracking_token = Column(String(64), unique=True, nullable=False, index=True)
    is_opened = Column(Boolean, default=False)
    is_clicked = Column(Boolean, default=False)
    reaction_time_sec = Column(Integer, nullable=True)
    quiz_score = Column(Integer, nullable=True)

    campaign = relationship("Campaign", back_populates="trackings")
    target_user = relationship("TargetUser", back_populates="trackings")


class QuizQuestion(Base):
    __tablename__ = "quiz_questions"

    id = Column(Integer, primary_key=True, index=True)
    template_id = Column(Integer, ForeignKey("templates.id", ondelete="CASCADE"), nullable=False)
    question = Column(String(255), nullable=False)
    option_a = Column(String(150), nullable=False)
    option_b = Column(String(150), nullable=False)
    option_c = Column(String(150), nullable=False)
    correct_answer = Column(CHAR(1), nullable=False)  # 'A', 'B' lub 'C'

    template = relationship("Template", back_populates="quiz_questions")

