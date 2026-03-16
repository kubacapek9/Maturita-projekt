<?php
header('Content-Type: application/json');

$servername = "dbs.spskladno.cz";
$username   = "student3";
$password   = "spsnet";
$database   = "vyuka3";

$conn = new mysqli($servername, $username, $password, $database);
if ($conn->connect_error) {
    echo json_encode([]);
    exit;
}

$conn->set_charset("utf8");
$sql = "SELECT player_name, score FROM scores ORDER BY score DESC LIMIT 5";
$result = $conn->query($sql);

$top = [];
while($row = $result->fetch_assoc()){
    $top[] = $row;
}

$conn->close();
echo json_encode($top);
?>