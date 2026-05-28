import asyncio
import os
from dotenv import load_dotenv
from app.mock_provider.factory.factory import ProviderFactory

load_dotenv()
SECRET = os.getenv("WEBHOOK_SECRET")
if not SECRET:
    raise ValueError("WEBHOOK_SECRET is required. Set it in the .env file or environment.")

async def run():
    while True:
        print("Available providers:", ", ".join(ProviderFactory._providers.keys()))
        provider_type = input("Enter provider (or 'exit'): ").strip()

        if not provider_type:
            print("Please enter a provider name")
            continue

        if provider_type == "exit":
            break

        provider = ProviderFactory.create(
            provider_type=provider_type,
            secret=SECRET,
            webhook_url="http://localhost:8000/webhook"
        )
        
        if provider is None:    # catches NoneType error
            continue

        try:
            payload = await provider.generate_event()
            signature = await provider.sign(payload)
            await provider.send(payload, signature)
        except Exception as e:
            print(f"Error while processing provider {provider_type}: {e}")


if __name__ == "__main__":
    asyncio.run(run())
