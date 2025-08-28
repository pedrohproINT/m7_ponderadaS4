import os
from decimal import Decimal
from flask import Flask, render_template, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String, DateTime, DECIMAL, ForeignKey, func
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# Use variáveis de ambiente (NÃO commitar credenciais)
DB_HOST = os.getenv("DB_HOST", "CHANGE_ME_RDS_ENDPOINT")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_USER = os.getenv("DB_USER", "admin")
DB_PASS = os.getenv("DB_PASS", "CHANGE_ME_PASSWORD")
DB_NAME = os.getenv("DB_NAME", "simpledb")

engine = create_engine(
    f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4",
    pool_pre_ping=True,
)

Base = declarative_base()

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(120), nullable=False)
    email = Column(String(180), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    orders = relationship("Order", back_populates="customer", cascade="all, delete-orphan")

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False, index=True)
    amount = Column(DECIMAL(10, 2), nullable=False)
    status = Column(String(20), nullable=False)  # pending | paid | canceled
    created_at = Column(DateTime, server_default=func.now())
    customer = relationship("Customer", back_populates="orders")

# cria tabelas se não existirem
Base.metadata.cr
