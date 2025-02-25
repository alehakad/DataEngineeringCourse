# Use the official AWS Glue image
FROM amazon/aws-glue-libs:glue_libs_4.0.0_image_01

# Set the working directory inside the container
WORKDIR /home/glue_user/workspace

# Copy your local Glue script into the container (assumes you have the script on your host machine)
COPY . /home/glue_user/workspace

# Set environment variables (optional)
ENV PYSPARK_PYTHON=python3
ENV PYSPARK_DRIVER_PYTHON=python3

# Default command to run the PySpark job
CMD ["spark-submit", "/home/glue_user/workspace/glue-pyspark.py"]

# To run:
#sudo docker run -it --rm \
#  -v ~/.aws:/home/glue_user/.aws \
#  -e AWS_ACCESS_KEY_ID=$(aws configure get aws_access_key_id) \
#  -e AWS_SECRET_ACCESS_KEY=$(aws configure get aws_secret_access_key) \
#  -e AWS_SESSION_TOKEN=$(aws configure get aws_session_token) \
#  -e AWS_REGION=$(aws configure get region) \
#  -v $(pwd)/../data:/home/glue_user/data/csv \
#  -v $(pwd):/home/glue_user/workspace \
#  -p 4040:4040 -p 18080:18080 \
#  --name glue_local_dev \
#  glue-local-dev \
#  spark-submit /home/glue_user/workspace/glue-pyspark.py
