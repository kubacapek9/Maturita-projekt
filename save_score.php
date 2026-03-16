<?php
$servername = "dbs.spskladno.cz";
$username   = "student3";
$password   = "spsnet";
$database   = "vyuka3";

$conn = new mysqli($servername, $username, $password, $database);
if ($conn->connect_error) die("Chyba připojení: " . $conn->connect_error);

$data = json_decode(file_get_contents("php://input"), true);
if(isset($data['player_name']) && isset($data['score'])) {
    $stmt = $conn->prepare("INSERT INTO scores (player_name, score) VALUES (?, ?)");
    $stmt->bind_param("si", $data['player_name'], $data['score']);
    $stmt->execute();
    $stmt->close();
    echo json_encode(["status"=>"ok"]);
} else {
    echo json_encode(["status"=>"error","message"=>"Chybí data"]);
}

$conn->close();
?>