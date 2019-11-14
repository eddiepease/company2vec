FROM fnndsc/ubuntu-python3:latest

# Create a working directory
WORKDIR /src

# Copy source code to working directory
COPY . /src

# Install packages from requirements.txt
# RUN apk --update add alpine-sdk libffi-dev python3-dev
RUN pip install --upgrade pip &&\
		pip install -r requirements.txt

# Copy data into directory
RUN aws s3 cp s3://company2vec-data /src/app/data --recursive

# Expose port 5000
EXPOSE 5000

# Run app.py at container launch
ENTRYPOINT ["python"]
CMD ["kleinapp.py"]
