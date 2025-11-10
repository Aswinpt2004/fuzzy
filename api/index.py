"""
Vercel-compatible serverless wrapper for the Fuzzy Logic Toolbox
This file is needed to run Flask on Vercel's serverless platform
"""

from app import app

# Export the Flask app instance for Vercel
# Vercel automatically looks for 'app' in api/index.py or at root level
export_app = app

if __name__ == "__main__":
    # For local development
    app.run(debug=True, port=5000)
