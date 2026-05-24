from flask import Flask, jsonify, request
from nse import NSE
import os

app = Flask(__name__)

@app.route("/")
def index():
    return jsonify({"status": "ok", "message": "NSE relay is running"})

@app.route("/actions")
def actions():
    symbol = request.args.get("symbol", "").upper().strip()
    if not symbol:
        return jsonify({"error": "symbol parameter required"}), 400

    try:
        # NSE() needs a writable folder for cookie storage.
        # On Render the /tmp directory is always writable.
        with NSE(download_folder="/tmp", server=True) as nse:
            data = nse.actions(segment="equities", symbol=symbol)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)