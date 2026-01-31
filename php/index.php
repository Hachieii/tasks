<!-- Show current user in session and a form to search for a specific user in table with its created date-->

<?php
require __DIR__ . '/db.php';

if (session_status() === PHP_SESSION_NONE) {
    session_start();
}

$username = $_SESSION['username'] ?? null;

if (isset($_GET['q'])) {
    try {
        $q = $_GET['q'];
        $sql = "SELECT username, created_at FROM users WHERE username = '$q'";
        $stmt = $pdo->prepare($sql);
        $stmt->execute();
        $res = $stmt->fetchAll();
    } catch (PDOException $e) {
        echo "Connection failed: " . $e->getMessage();
    }
}
?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Search user</title>
</head>

<body>
    <?php
    if ($username) {
        echo '<a href="logout.php">Logout</a><br>';
        echo "Hello $username!<br>";
    } else {
        echo '<a href="login.php">Login</a><br>';
        echo '<a href="register.php">Register</a><br>';
    }

    if ($username == 'admin') {
        echo 'Flag: HETRUONG{klqi_h9FElc?si=oVal0wV8AbdAmJOs}<br>';
    }
    echo __DIR__;
    ?>

    <form action="index.php" method="GET">
        <input type="text" name="q" placeholder="Enter user to search">
        <button>Submit</button>
    </form>

    <?php
    if (isset($_GET['q'])) {
        echo "Results for $q:<br>";
        foreach ($res as $row) {
            echo "{$row['username']}: {$row['created_at']}<br>";
        }
    }
    ?>
</body>

</html>