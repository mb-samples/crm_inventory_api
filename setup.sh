#!/bin/bash
# Setup script for CRM & Inventory API with Python 3.11

echo "🚀 Setting up CRM & Inventory API..."

# Check if Python 3.11 is installed
if ! command -v python3.11 &> /dev/null; then
    echo "❌ Python 3.11 not found. Installing via Homebrew..."
    brew install python@3.11
fi

echo "✅ Python 3.11 found: $(python3.11 --version)"

# Create virtual environment with Python 3.11
echo "📦 Creating virtual environment with Python 3.11..."
python3.11 -m venv venv311

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv311/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Copy environment file
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env with your database credentials"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To activate the environment, run:"
echo "  source venv311/bin/activate"
echo ""
echo "To start the API server:"
echo "  python app.py"
echo ""
echo "To use mock database (no real database needed):"
echo "  export USE_MOCK_DB=true"
echo "  python app.py"
echo "  python app.py"
echo ""
