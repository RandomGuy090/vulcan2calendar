FROM python:latest

ARG pin
ARG token
ARG symbol

WORKDIR /app

COPY requirements.txt . 
 
RUN pip3 install -r requirements.txt

COPY . .

ENV PIN=${pin} 
ENV TOKEN=${token} 
ENV SYMBOL=${symbol} 

RUN python3 register.py

CMD ["python3", "vulcan2calendar.py"]

