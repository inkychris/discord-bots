FROM python:3.9

ADD groovy_context_manager.py requirements.txt /
RUN pip install -r requirements.txt

CMD python groovy_context_manager.py
