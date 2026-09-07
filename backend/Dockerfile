FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements_onnx.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY api_onnx.py ./
COPY model/weights/triplet_hard_model_best.onnx ./model/weights/

# Hugging Face Spaces sets PORT=7860 automatically
ENV PORT=7860
EXPOSE 7860

CMD uvicorn api_onnx:app --host 0.0.0.0 --port ${PORT}
