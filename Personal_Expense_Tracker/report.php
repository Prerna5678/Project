<?php
require_once 'session_helper.php';
require_once 'db.php';
require_login();

$stmt = $pdo->prepare("SELECT tracking_id, date, category, description, amount FROM tracking WHERE id = ? ORDER BY date DESC");
$stmt->execute([$_SESSION['user_id']]);
$tracking = $stmt->fetchAll();
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
<table>
    <tr>
        <th>Id</th>
        <th>Date</th>
        <th>Category</th>
        <th>Description</th>
        <th>(₹) Amount</th>
        <th>Update</th>
        <th>Delete</th>
    </tr>
    <?php foreach ($tracking as $row): ?>
    <tr>
        <td><?php echo htmlspecialchars($row['tracking_id']); ?></td>
        <td><?php echo htmlspecialchars($row['date']); ?></td>
        <td><?php echo htmlspecialchars($row['category']); ?></td>
        <td><?php echo htmlspecialchars($row['description']); ?></td>
        <td><?php echo htmlspecialchars($row['amount']); ?></td>
        <td>
            <a href="update.php?id=<?php echo urlencode($row['tracking_id']); ?>">✏️ Edit</a>
        </td>
        <td>
            <form action="delete.php" method="POST" onsubmit="return confirm('Delete this expense?');" style="display:inline;">
                <input type="hidden" name="id" value="<?php echo htmlspecialchars($row['tracking_id']); ?>">
                <button type="submit">🗑️ Delete</button>
            </form>
        </td>
    </tr>
    <?php endforeach; ?>
</table>
</body>
</html>
