import boto3

def get_openai_key():
    ssm = boto3.client("ssm", region_name="us-east-2")  # Ohio
    response = ssm.get_parameter(
        Name="/openai/api_key",
        WithDecryption=True
    )
    return response["Parameter"]["Value"]

print("Key retrieved successfully")
print("First characters:", get_openai_key()[:6])
