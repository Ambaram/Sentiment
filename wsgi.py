from app import app
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/root/customer-account-automation/")

if __name__ == "__main__":
    app.run()
