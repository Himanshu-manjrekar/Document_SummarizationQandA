# base image
FROM python:3.7
# work dir
WORKDIR /app
# copy
COPY . /app
# run 
RUN pip install -r requirements.txt
# port
EXPOSE 8501
# cmd
CMD ["streamlit", "run", "app.py"]