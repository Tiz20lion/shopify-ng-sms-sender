#!/bin/bash

echo "Activating virtual environment..."
source venv/bin/activate

echo ""
echo "Starting FastAPI server..."
echo ""
python -m app.main

