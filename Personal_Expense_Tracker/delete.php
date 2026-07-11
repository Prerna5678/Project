<?php
require_once 'session_helper.php';
require_once 'db.php';
require_login();

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $id = $_POST['id'] ?? null;

    if ($id) {
        $stmt = $pdo->prepare("DELETE FROM tracking WHERE tracking_id = ? AND id = ?");
        $stmt->execute([$id, $_SESSION['user_id']]);
    }
}

header("Location: report.php");
exit;
