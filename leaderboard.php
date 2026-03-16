<?php
// ----------------------- PHP: Připojení k databázi -----------------------
$servername = "dbs.spskladno.cz";
$username   = "student3";      // tvé DB uživatelské jméno
$password   = "spsnet";        // tvé DB heslo
$database   = "vyuka3";        // tvá DB

$conn = new mysqli($servername, $username, $password, $database);
if ($conn->connect_error) die("Chyba připojení: " . $conn->connect_error);

// Pokud chceme načíst TOP 5 hráčů (využijeme, když zobrazíme leaderboard)
$sql = "SELECT player_name, score FROM scores ORDER BY score DESC LIMIT 5";
$result = $conn->query($sql);
?>

<!DOCTYPE html>
<html lang="cs">
<head>
<meta charset="UTF-8">
<title>Catch the Ball - Prezentace</title>
<style>
/* ----------------------- Základní nastavení ----------------------- */
body { font-family: Arial, sans-serif; margin:0; padding:0; background:#1e1e2f; color:#fff; }
h1,h2 { text-align:center; }
a { color:#ffd700; text-decoration:none; }
a:hover { text-decoration:underline; }
header { background-color:#282c44; padding:20px 0; box-shadow:0 4px 6px rgba(0,0,0,0.3); }
nav { text-align:center; margin-top:10px; }
nav a { margin:0 15px; font-weight:bold; font-size:18px; }
.section { display:none; padding:40px 20px; }
.section.active { display:block; }
.section h2 { color:#ffd700; margin-bottom:20px; }
#loginForm input, #gameScoreSection input { padding:10px; font-size:16px; width:250px; margin-right:10px; border:none; border-radius:5px; }
#loginForm button, #gameScoreSection button, #adminPanel button { padding:10px 15px; font-size:16px; background-color:#ffd700; border:none; border-radius:5px; cursor:pointer; font-weight:bold; }
#loginForm button:hover, #gameScoreSection button:hover, #adminPanel button:hover { background-color:#e6c200; }
table { width:60%; margin:20px auto; border-collapse:collapse; background-color:#282c44; box-shadow:0 4px 6px rgba(0,0,0,0.3); }
th, td { padding:12px; border-bottom:1px solid #444; text-align:center; }
th { background-color:#1e1e2f; color:#ffd700; font-size:18px; }
tr:hover { background-color:#3a3f5c; }
p { max-width:800px; margin:10px auto; line-height:1.5; text-align:center; }
.hidden { display:none; }
</style>
</head>
<body>

<header>
    <h1>Catch the Ball 🎯</h1>
    <nav>
        <a href="#" onclick="showSection('home')">Domů</a>
        <a href="#" onclick="showSection('about')">O projektu</a>
        <a href="#" onclick="showSection('contact')">Kontakt</a>
        <a href="#" onclick="showSection('popis')">Popis hry</a>
        <a href="#" onclick="showSection('leaderboard')">TOP 5 hráčů</a>
    </nav>
</header>

<!-- ----------------------- DOMŮ ----------------------- -->
<section id="home" class="section active">
    <h2>Přihlášení</h2>
    <div id="loginForm">
        <input type="text" id="username" placeholder="Zadejte své jméno">
        <button onclick="login()">Přihlásit</button>
        <p id="loginError" style="color:red;"></p>
    </div>
    <div id="welcome" class="hidden">
        <p id="welcomeText"></p>
        <button onclick="logout()">Odhlásit</button>
    </div>

    <!-- Sekce pro přidání skóre -->
    <section id="gameScoreSection" class="hidden">
        <h2>Přidej své skóre</h2>
        <input type="number" id="userScore" placeholder="Zadejte své skóre">
        <button onclick="addScore()">Uložit skóre</button>
    </section>
</section>

<!-- ----------------------- LEADERBOARD ----------------------- -->
<section id="leaderboard" class="section">
    <h2>TOP 5 hráčů</h2>
    <table>
        <tr><th>Pořadí</th><th>Hráč</th><th>Skóre</th></tr>
        <?php
        $rank = 1;
        while($row = $result->fetch_assoc()){
            echo "<tr>";
            echo "<td>".$rank."</td>";
            echo "<td>".$row["player_name"]."</td>";
            echo "<td>".$row["score"]."</td>";
            echo "</tr>";
            $rank++;
        }
        ?>
    </table>
</section>

<!-- ----------------------- ABOUT ----------------------- -->
<section id="about" class="section">
    <h2>O projektu</h2>
    <p>Tento projekt představuje jednoduchou hru Catch the Ball, kde hráči chytají padající míčky a získávají body. Webová prezentace umožňuje přihlášení a zobrazení žebříčku.</p>
</section>

<!-- ----------------------- CONTACT ----------------------- -->
<section id="contact" class="section">
    <h2>Kontakt</h2>
    <p>Autor projektu: Jakub Čapek</p>
    <p>Email: capekj@gmail.com</p>
    <p>github.com/kubacapek9</p>
</section>

<!-- ----------------------- POPIS ----------------------- -->
<section id="popis" class="section">
    <h2>Popis hry</h2>
    <p>Hráč ovládá košík, chytá míčky. Červený míček: +1 bod, Zlatý míček: +3 body, Černý (bomba): -1 život. Hra zvyšuje obtížnost se skóre.</p>
</section>

<script>
// Přepínání sekcí
function showSection(id){
    document.querySelectorAll(".section").forEach(sec=>sec.classList.remove("active"));
    document.getElementById(id).classList.add("active");
}

// Přihlášení
let currentUser = null;
function login() {
    const username = document.getElementById("username").value.trim();
    if(username===""){ 
        document.getElementById("loginError").innerText="Zadejte své jméno!"; 
        return; 
    }
    currentUser=username;
    document.getElementById("loginForm").classList.add("hidden");
    document.getElementById("welcome").classList.remove("hidden");
    document.getElementById("welcomeText").innerText=`Vítej, ${currentUser}!`;
    document.getElementById("gameScoreSection").classList.remove("hidden");
    document.getElementById("loginError").innerText="";
}

// Odhlášení
function logout(){
    currentUser=null;
    document.getElementById("loginForm").classList.remove("hidden");
    document.getElementById("welcome").classList.add("hidden");
    document.getElementById("gameScoreSection").classList.add("hidden");
    document.getElementById("username").value="";
}

// Přidání skóre
function addScore() {
    const scoreInput = document.getElementById("userScore");
    let scoreVal = parseInt(scoreInput.value);
    if(isNaN(scoreVal)) { alert("Zadejte číslo!"); return; }
    alert("Skóre "+scoreVal+" pro hráče "+currentUser+" bude uloženo do DB přes backend (nutné doprogramovat).");
    scoreInput.value="";
}
</script>

</body>
</html>