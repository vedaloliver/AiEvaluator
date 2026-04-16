#!/bin/bash

echo "🚀 Setting up Python Evaluator Service..."
echo ""

# Check Python version
echo "📌 Checking Python version..."
python3 --version

# Check if pip is available
if ! command -v pip &> /dev/null && ! python3 -m pip --version &> /dev/null
then
    echo "❌ pip is not installed!"
    echo "💡 Install pip with: sudo apt-get install python3-pip (Ubuntu/Debian)"
    echo "   Or: brew install python3 (macOS)"
    exit 1
fi

echo "✅ pip is available"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
python3 -m pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "🎯 Next steps:"
echo "   1. Copy .env.example to .env: cp .env.example .env"
echo "   2. Run the service: python3 main.py"
echo "   3. Test: curl http://localhost:3002/api/v1/health"
echo ""
