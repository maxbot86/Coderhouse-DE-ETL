FROM python:3.11

# Create app directory For MAX and JIRA Propuse
WORKDIR /app

# Install app dependencies For MAX and JIRA Propuse
COPY src/requirements.txt ./

RUN pip install -r requirements.txt

# Bundle app source For MAX and JIRA Propuse
COPY src /app

CMD [ "python", "main.py" ]

612 619