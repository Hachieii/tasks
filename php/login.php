<!-- UI to login and add to session -->

<?php
require __DIR__ . '/db.php';

if (session_status() === PHP_SESSION_NONE) {
    session_start();
}

if (isset($_SESSION['username'])) {
    header("location: index.php");
    exit();
}
?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
</head>

<body>
    <h1>Login</h1>
    <form action="auth.php" method="POST">
        <input type="text" name="username">
        <input type="password" name="password">
        <input type="text" name="type" value="login" hidden>
        <button>Submit</button>
    </form>
    <a href="register.php">Register</a>
</body>

</html>