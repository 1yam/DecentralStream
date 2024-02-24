from flask import Flask, request, jsonify
from datetime import datetime

from flask_cors import cross_origin

app = Flask(__name__)
cid_storage = {}


@app.route("/store_cid/<owner>", methods=["POST"])
def store_cid(owner):
    key = request.args.get("key")
    if not key:
        return jsonify({"error": "Missing 'key' query parameter"}), 400

    timestamp = datetime.now().timestamp()  # Get current Unix timestamp
    full_key = f"{timestamp}-{owner}"
    cid_storage[full_key] = key
    return jsonify({"message": "CID stored successfully", "full_key": full_key, "cid": key}), 200


@app.route("/get_cid/<owner>")
@cross_origin()
def get_cids(owner):
    #owner_cids = [f"{int(key.split('-')[0])}:{cid}" for key, cid in cid_storage.items() if key.endswith(f"-{owner}")]
    owner_cids = [f"{float(key.split('-')[0])}:{cid}" for key, cid in cid_storage.items() if key.endswith(f"-{owner}")]
    if owner_cids:
        return jsonify({"owner": owner, "cids": owner_cids}), 200
    else:
        return jsonify({"message": f"No CID found for owner '{owner}'"}), 404


if __name__ == "__main__":
    app.run()