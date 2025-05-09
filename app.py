import os

# Simulate usage of a secret key
API_KEY = "sk-proj-Wxoa39g03zhk1cZgsMUc1IJFPBDeHU7k-tub1k3JUY_Rs7B37_4ZnBO6wnm3GQyViBdK15Ii1bT3BlbkFJxYWF3AT-tJAl8iQKsNIc4ET6NGvqc4"  # Hardcoded secret

def main():
    print("Starting application...")
    print(f"API Key: {API_KEY}")  # Exposing secret in logs

if __name__ == "__main__":
    main()
