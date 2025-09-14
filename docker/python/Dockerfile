FROM python:3.13.2

WORKDIR /app

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

COPY . .

CMD ["python", "-m", "seed_scripts.seed_all"]
