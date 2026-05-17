from flask import Flask, request, jsonify
from instagrapi import Client

app = Flask(__name__)

@app.route('/extract', methods=['POST'])
def extract_images():
    # 1. Get the target account from n8n
    data = request.json
    target_account = data.get('target_account')
    
    if not target_account:
        return jsonify({"error": "No target account provided"}), 400

    try:
        # 2. Log in with Burner Account
        cl = Client()
        cl.login("YOUR_BURNER_USERNAME", "YOUR_BURNER_PASSWORD")
        
        # 3. Fetch the account
        user_id = cl.user_id_from_username(target_account)
        medias = cl.user_medias(user_id, amount=10) # Grabs the last 10 posts
        
        extracted_urls = []
        
        # 4. Extract the URLs
        for media in medias:
            if media.media_type == 1: # Single Photo
                extracted_urls.append(str(media.thumbnail_url))
                
        # 5. Send the URLs back to n8n
        return jsonify({"status": "success", "images": extracted_urls}), 200
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
