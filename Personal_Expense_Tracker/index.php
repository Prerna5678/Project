<?php
require_once 'session_helper.php';
require_once 'db.php';
require_login();

$msg = '';
$type = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $date = $_POST['date'] ?? '';
    $category = trim($_POST['category'] ?? '');
    $amount = $_POST['amount'] ?? '';
    $description = trim($_POST['description'] ?? '');

    if ($date !== '' && $category !== '' && $description !== '' && is_numeric($amount) && $amount > 0) {
        $stmt = $pdo->prepare("INSERT INTO tracking (date, category, description, amount, id) VALUES (?, ?, ?, ?, ?)");
        $stmt->execute([$date, $category, $description, $amount, $_SESSION['user_id']]);
        $msg = "<center><strong style='color: white;'>✅ Expense added successfully.</strong></center><br>";
        $type = 'success';
    } else {
        $msg = "<center><strong style='color: red;'>Please fill all fields correctly.</strong></center>";
        $type = 'error';
    }
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Personal Expense Tracker</title>

    <link rel="stylesheet" href="style.css">
</head>
<body>

    <nav class="navbar">
        <span>Hi, <?php echo htmlspecialchars($_SESSION['user_name'] ?? ''); ?></span>
        <a href="logout.php">Logout</a>
    </nav>

    <div class="container">
        <h2>💰 Personal Expense Tracker</h2>
        <br>

        <?php if ($msg): ?>
            <p class="flash <?php echo htmlspecialchars($type); ?>">
                <?php echo $msg; ?>
            </p>
        <?php endif; ?>

        <div class="form-card">
            <h3>Add New Expense</h3>

            <form action="" method="POST">

                <div class="form-group">
                    <label for="date">Date</label>
                    <input type="date" id="date" name="date" required>
                </div>
                <br>

                <div class="form-group">
                    <label for="category">Category</label>
                    <select id="category" name="category" required>
                        <option value="">Select Category</option>
                        <option>Food</option>
                        <option>Travel</option>
                        <option>Shopping</option>
                        <option>Bills</option>
                        <option>Entertainment</option>
                        <option>Other</option>
                    </select>
                </div>
                <br>

                <div class="form-group">
                    <label for="amount">Amount (₹)</label>
                    <input
                        type="number"
                        id="amount"
                        name="amount"
                        placeholder="Enter amount"
                        required
                    >
                </div>
                <br>

                <div class="form-group">
                    <label for="description">Description</label>
                    <input
                        type="text"
                        id="description"
                        name="description"
                        placeholder="Enter description"
                        required
                    >
                </div>
                <br>

                <!-- Submit Button -->
                <button type="submit">
                    ➕ Add Expense
                </button>

                <br><br>

                <div class="button-group" style="display: flex; gap: 10px;">

                    <button
                        type="button"
                        onclick="location.href='view.php'">
                        📊 View Expenses
                    </button>

                    <button
                        type="button"
                        onclick="location.href='report.php'">
                        ✏️ Edit / 🗑️ Delete
                    </button>

                </div>

            </form>

        </div>
    </div>

</body>
</html>
