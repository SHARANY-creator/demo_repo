from pyngrok import ngrok

# Expose the local port 8000 to the internet
public_url = ngrok.connect(8000)
print(f"Public URL: {public_url}")

# Keep the program running to maintain the tunnel
input("Press Enter to exit...\n")
