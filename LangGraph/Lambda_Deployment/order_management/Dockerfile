# Use AWS Lambda Python 3.11 base image
FROM public.ecr.aws/lambda/python:3.11

# Copy and install dependencies
COPY requirements.txt ${LAMBDA_TASK_ROOT}/
RUN  pip install -r requirements.txt

# Copy application code
COPY graph.py ${LAMBDA_TASK_ROOT}/

# Set the Lambda handler - filename.function_name
CMD ["graph.lambda_handler"]
