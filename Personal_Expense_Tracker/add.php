<?php
require_once 'session_helper.php';
require_once 'db.php';
require_login();

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $date = $_POST['date'] ?? '';
    $category = trim($_POST['category'] ?? '');
    $amount = $_POST['amount'] ?? '';
    $description = trim($_POST['description'] ?? '');

    if ($date !== '' && $category !== '' && $description !== '' && is_numeric($amount) && $amount > 0) {
        $stmt = $pdo->prepare("INSERT INTO tracking (date, category, description, amount, id) VALUES (?, ?, ?, ?, ?)");
        $stmt->execute([$date, $category, $description, $amount, $_SESSION['user_id']]);
        header("Location: index.php?msg=" . urlencode("<center><strong style='color: white;'>✅ Expense added successfully.</strong></center>") . "&type=success");
        exit;
    }
}

header("Location: index.php?msg=" . urlencode("<center><strong style='color: red;'>Please fill all fields correctly.</strong></center>") . "&type=error");
exit;
