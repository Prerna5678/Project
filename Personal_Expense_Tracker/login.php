<?php
require_once 'session_helper.php';
require_once 'db.php';

$error = '';
$success = $_GET['msg'] ?? '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $name = trim($_POST['name'] ?? '');       // used as email/username field
    $password = $_POST['password'] ?? '';

    if ($name === '' || $password === '') {
        $error = "Username and password are required.";
    } else {
        $stmt = $pdo->prepare("SELECT * FROM reg WHERE email = ?");
        $stmt->execute([$name]);
        $user = $stmt->fetch();

        if ($user && password_verify($password, $user['password'])) {
            $_SESSION['user_id'] = $user['id'];
            $_SESSION['user_name'] = $user['name'];
            header("Location: index.php");
            exit;
        } else {
            $error = "Invalid username or password.";
        }
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
    <br><br><br>

    <div class="form-card">

        <?php if ($error): ?>
            <p class="flash error"><?php echo htmlspecialchars($error); ?></p>
        <?php endif; ?>

        <?php if ($success): ?>
            <p class="flash success"><?php echo htmlspecialchars($success); ?></p>
        <?php endif; ?>

        <form action="login.php" method="POST" onsubmit="return validateLogin()" novalidate>
            <h3>Login</h3><br>

            <div class="form-group">
                <label for="name">Email Id</label>
                <input type="text" id="name" name="name" placeholder="Enter email id" required>
                <small class="error-text" id="name-error"></small>
            </div><br>

            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" placeholder="Enter password" required>
                <small class="error-text" id="password-error"></small>
            </div><br><br>

            <div class="button-group" style="display: flex; gap: 10px;">
                <button type="submit">
                    Sign In
                </button>
                <button type="button" onclick="window.location.href='register.php'">
                    Sign Up
                </button>
            </div>
        </form>
    </div>

    <script>
        function validateLogin() {
            let valid = true;

            const name = document.getElementById("name");
            const password = document.getElementById("password");
            const nameError = document.getElementById("name-error");
            const passwordError = document.getElementById("password-error");

            nameError.textContent = "";
            passwordError.textContent = "";

            if (name.value.trim() === "") {
                nameError.textContent = "Username is required.";
                valid = false;
            }

            if (password.value.trim() === "") {
                passwordError.textContent = "Password is required.";
                valid = false;
            }

            return valid;
        }
    </script>
</body>
</html>
