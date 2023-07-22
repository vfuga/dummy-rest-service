FROM python:3.10.10
WORKDIR /app
COPY ./requirements.txt ./requirements.txt
RUN apt-get -y update && apt-get -y upgrade && pip install --upgrade pip && pip install -r ./requirements.txt
COPY ./main.py ./main.py

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 80
USER 500
# CMD ["/bin/bash"]
# CMD ["python", "main.py"]
# CMD ["uvicorn", "main:fapp", "--host", "0.0.0.0", "--port", "8181", "--workers", "1"]
CMD ["uvicorn", "main:fapp", "--host", "0.0.0.0", "--port", "80", "--workers", "5"]
