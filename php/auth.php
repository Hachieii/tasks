<!-- verify login credential -->

<?php
require __DIR__ . '/db.php';

if (session_status() === PHP_SESSION_NONE) {
    session_start();
}

if ($_SERVER['REQUEST_METHOD'] != 'POST') {
    header("location: login.php");
    exit();
}

$username = $_POST['username'] ?? '';
$password = $_POST['password'] ?? '';
$type = $_POST['type'] ?? '';

if (!$username || !$password || !$type) {
    die("Missing credential");
}

if ($type != 'login' && $type != 'register') {
    die("Invalid credential");
}

$sql = "SELECT username, password FROM users WHERE username = ?";
$stmt = $pdo->prepare($sql);
$stmt->execute([$username]);
$row = $stmt->fetch();

if ($type == 'login') {
    if (!$row || ($row['username'] != $username || $row['password'] != $password)) {
        die("Invalid credential");
    }

    $_SESSION['username'] = $username;
    header("location: index.php");
    exit();
}

// $type = 'register'

if ($row) {
    die("Username already exist");
}

$sql = "INSERT INTO users VALUES (?, ?, ?)";
$stmt = $pdo->prepare($sql);
$stmt->execute([$username, $password, date("Y-m-d H:i:s")]);
header("location: login.php");
exit();
?>