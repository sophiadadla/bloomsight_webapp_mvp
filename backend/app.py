# Add this after your standard imports
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Fix CORS for production
CORS(app, supports_credentials=True, origins=["*"])  # Or specify your frontend domain

# Fixed get_beaches function (remove duplicate exception handler)
@app.route('/beaches', methods=['GET'])
def get_beaches():
    try:
        resp = supabase.table("beaches").select("*, pictures(image_url)").execute()
        rows = resp.data or []

        beaches = []
        for beach in rows:
            pics = beach.get("pictures") or []
            beach["preview_picture"] = pics[0]["image_url"] if pics else None
            beach.pop("pictures", None)
            beaches.append(beach)

        return jsonify(beaches), 200

    except Exception as e:
        import traceback, sys
        traceback.print_exc(file=sys.stderr)
        return jsonify({"error": f"/beaches failed: {str(e)}"}), 500

# Fixed update_beach function
@app.route('/beaches/<string:mapbox_id>', methods=['PUT'])
def update_beach(mapbox_id):
    data = request.json
    result = supabase.table("beaches").update(data).eq('mapbox_id', mapbox_id).execute()  # Fixed: was 'id'
    return jsonify(result.data), 200

# Add this at the very end of your file
# For Vercel deployment
def handler(request, context):
    return app(request, context)

# Make sure app is available at module level
if __name__ == '__main__':
    app.run(debug=True)