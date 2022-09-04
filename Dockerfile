FROM python:latest

ARG pin
ARG token
ARG symbol

WORKDIR /app

COPY requirements.txt . 
ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

COPY . .

ENV PIN=${pin} 
ENV TOKEN=${token} 
ENV SYMBOL=${symbol} 


RUN python3 register.py

CMD ["python3", "vulcan2calendar.py"]

