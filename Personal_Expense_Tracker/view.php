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
    </tr>
    <?php 
    $total = 0;
    foreach ($tracking as $row): 
        $total += $row['amount'];
    ?>
    <tr>
        <td><?php echo htmlspecialchars($row['tracking_id']); ?></td>
        <td><?php echo htmlspecialchars($row['date']); ?></td>
        <td><?php echo htmlspecialchars($row['category']); ?></td>
        <td><?php echo htmlspecialchars($row['description']); ?></td>
        <td><?php echo htmlspecialchars($row['amount']); ?></td>
    </tr>
    <?php endforeach; ?>
    <tr>
        <td colspan="4" style="text-align: right; font-weight: bold;">Total:</td>
        <td style="font-weight: bold;"><?php echo htmlspecialchars($total); ?></td>
    </tr>
</table>
</body>
</html>
