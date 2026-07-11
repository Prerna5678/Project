<?php
require_once 'session_helper.php';
require_once 'db.php';
require_login();

$id = $_GET['id'] ?? ($_POST['id'] ?? null);

if (!$id) {
    header("Location: report.php");
    exit;
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $date = $_POST['date'] ?? '';
    $category = trim($_POST['category'] ?? '');
    $amount = $_POST['amount'] ?? '';
    $description = trim($_POST['description'] ?? '');

    if ($date !== '' && $category !== '' && $description !== '' && is_numeric($amount) && $amount > 0) {
        $stmt = $pdo->prepare("UPDATE tracking SET date = ?, category = ?, description = ?, amount = ? WHERE tracking_id = ? AND id = ?");
        $stmt->execute([$date, $category, $description, $amount, $id, $_SESSION['user_id']]);
        header("Location: report.php");
        exit;
    }
}

$stmt = $pdo->prepare("SELECT * FROM tracking WHERE tracking_id = ? AND id = ?");
$stmt->execute([$id, $_SESSION['user_id']]);
$expense = $stmt->fetch();

if (!$expense) {
    header("Location: report.php");
    exit;
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
    <div class="container">
        <h2>✏️ Edit Expense</h2>
        <br>

        <div class="form-card">
            <form action="update.php?id=<?php echo urlencode($expense['tracking_id']); ?>" method="POST">
                <input type="hidden" name="id" value="<?php echo htmlspecialchars($expense['tracking_id']); ?>">

                <div class="form-group">
                    <label for="date">Date</label>
                    <input type="date" id="date" name="date" value="<?php echo htmlspecialchars($expense['date']); ?>" required>
                </div>
                <br>

                <div class="form-group">
                    <label for="category">Category</label>
                    <select id="category" name="category" required>
                        <?php
                        $categories = ["Food", "Travel", "Shopping", "Bills", "Entertainment", "Other"];
                        foreach ($categories as $cat) {
                            $selected = ($cat === $expense['category']) ? 'selected' : '';
                            echo "<option $selected>" . htmlspecialchars($cat) . "</option>";
                        }
                        ?>
                    </select>
                </div>
                <br>

                <div class="form-group">
                    <label for="amount">Amount (₹)</label>
                    <input type="number" id="amount" name="amount" value="<?php echo htmlspecialchars($expense['amount']); ?>" required>
                </div>
                <br>

                <div class="form-group">
                    <label for="description">Description</label>
                    <input type="text" id="description" name="description" value="<?php echo htmlspecialchars($expense['description']); ?>" required>
                </div>
                <br>

                <div class="button-group" style="display: flex; gap: 10px;">
                    <button type="submit">💾 Save Changes</button>
                    <button type="button" onclick="location.href='report.php'">Cancel</button>
                </div>
            </form>
        </div>
    </div>
</body>
</html>
