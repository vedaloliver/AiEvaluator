"""
AI Evaluator Service - Python Implementation
FastAPI server for evaluating AI model responses against regulatory scenarios
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from config.settings import settings
from routes.evaluation_routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for startup and shutdown"""
    # Startup
    print("\n🚀 Evaluator Service (Python) starting...")
    print(f"📊 Environment: {settings.environment}")

    if settings.use_mock_data:
        print("🎭 Mode: MOCK DATA (using test fixtures)")
        print("   Set USE_MOCK_DATA=false to use real Azure integration")
    else:
        # Validate Azure configuration
        if not all([
            settings.azure_ai_foundry_endpoint,
            settings.azure_subscription_id,
            settings.azure_tenant_id,
            settings.azure_client_id,
            settings.azure_client_secret
        ]):
            print("❌ Missing required Azure environment variables!")
            print("💡 Tip: Set USE_MOCK_DATA=true in .env to use mock data instead")
            print("Please check your .env file")
            exit(1)

        print("☁️  Mode: Azure AI Foundry")
        print(f"🔗 Azure Endpoint: {settings.azure_ai_foundry_endpoint}")

    print(f"\n📍 Service running on port {settings.port}")
    print(f"   - http://localhost:{settings.port}/")
    print(f"   - http://localhost:{settings.port}/api/v1/health")
    print(f"   - http://localhost:{settings.port}/api/v1/scenarios")
    print(f"   - http://localhost:{settings.port}/api/v1/models")
    print(f"   - http://localhost:{settings.port}/api/v1/evaluate\n")

    yield

    # Shutdown (if needed)
    print("\n👋 Shutting down gracefully...")


# Create FastAPI app
app = FastAPI(
    title="AI Evaluator Service",
    description="Evaluates AI model responses against regulatory scenarios",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint with service information"""
    return {
        "service": "AI Evaluator Service (Python)",
        "version": "1.0.0",
        "status": "running",
        "mode": "mock" if settings.use_mock_data else "azure",
        "endpoints": {
            "health": "/api/v1/health",
            "evaluate": "POST /api/v1/evaluate",
            "scenarios": "GET /api/v1/scenarios",
            "models": "GET /api/v1/models",
        }
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.port,
        reload=settings.environment == "development"
    )
