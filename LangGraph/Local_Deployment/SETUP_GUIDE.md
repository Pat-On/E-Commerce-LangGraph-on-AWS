# Setup Guide — LangGraph E-Commerce Assistant

## Prerequisites
### Step 1: Python and AWS CLI Installation

- Python 3.11.9 or 3.12 installed (https://www.python.org/downloads/)
- During installation, check **"Add Python to PATH"**.
- Verify installation: python --version

- AWS CLI installed (https://aws.amazon.com/cli/)


## Step-by-Step Installation

### Step 2: Create a virtual and Activate environment

python -m venv venv

venv\Scripts\activate

### Step 3: Install dependencies

pip install -r requirements.txt

### Step 4: Configure AWS credentials

aws configure

### Step 5: Run the agent (graph.py)
python graph.py

..........Deployment to AWS Lambda .........
1. Download Docker Desktop - https://www.docker.com/products/docker-desktop/ 
2. Install it.
3. Make changes to graph.py file
4. Update requirements.txt file
5. Create Docker file 

# 6. Build the Docker image
docker build --provenance=false --output type=docker -t order-management .

# 7. Login  and Create Repo in ECR

aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com

aws ecr create-repository --repository-name order-management --region us-east-1

8. Tag and Push to ECR
docker tag order-management:latest <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/order-management:latest

docker push <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/order-management:latest

9. Deploy to Lambda

10. Test Lambda
Sample event - 

{
  "message": "Can you track order_id 1d4d99c4-08c6-4fda-a687-48d1311a947f?"
}

11. Integrate with Streamlit using Lambda Functional URL

12. Streamlit Command to Run - streamlit run ui/streamlit_app.py

[Important Note : Incase of errors, see below (Below steps shown in one of the previous lectures as part of local deployment )
- Check Streamlit is installed in the Virtual env --- > streamlit --version
- If not, 
python -m venv venv
venv\Scripts\activate
pin install streamlit==1.59.1]

13. Sample Questions :
- What type of shoes do you have ?
- Order Running Shoes (product_id: 101, quanity - 2) 
- Order Status - [order id from previous answer]
