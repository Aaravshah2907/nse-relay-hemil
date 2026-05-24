from flask import Flask, jsonify, request
from bse import BSE
import os

app = Flask(__name__)

@app.route("/")
def index():
    return jsonify({"status": "ok", "message": "BSE relay is running"})

@app.route("/actions")
def actions():
    symbol = request.args.get("symbol", "").upper().strip()
    if not symbol:
        return jsonify({"error": "symbol parameter required"}), 400

    try:
        with BSE(download_folder="/tmp") as bse:
            # Step 1: resolve NSE symbol → BSE scrip code
            scrip_code = bse.getScripCode(symbol)
            if not scrip_code:
                return jsonify({"error": "Symbol not found: " + symbol}), 404

            # Step 2: fetch full corporate action history
            data = bse.actions(scripcode=scrip_code)

        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)