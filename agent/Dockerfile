FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /srv

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ดาวน์โหลด embedding model ตอน build ไม่ใช่ตอน runtime
# ไม่งั้นครั้งแรกที่ reviewer รัน จะค้างเป็นนาทีโดยไม่รู้ว่าเกิดอะไรขึ้น
ARG EMBEDDING_MODEL=BAAI/bge-m3
ENV HF_HOME=/opt/hf
RUN python -c "from sentence_transformers import SentenceTransformer; \
    SentenceTransformer('${EMBEDDING_MODEL}')"

COPY app ./app

EXPOSE 3000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3000"]
