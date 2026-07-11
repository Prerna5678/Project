<?php
require_once 'session_helper.php';
require_once 'db.php';

$errors = [];

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $name = trim($_POST['name'] ?? '');
    $contact_no = trim($_POST['contact_no'] ?? '');
    $email = trim($_POST['email'] ?? '');
    $password = $_POST['password'] ?? '';
    $c_password = $_POST['c_password'] ?? '';

    if ($name === '') $errors[] = "Full name is required.";
    if (!preg_match('/^\d{10}$/', $contact_no)) $errors[] = "Enter a valid 10 digit phone number.";
    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) $errors[] = "Enter a valid email address.";
    if (strlen($password) < 6) $errors[] = "Password must be at least 6 characters.";
    if ($password !== $c_password) $errors[] = "Passwords do not match.";

    if (empty($errors)) {
        $stmt = $pdo->prepare("SELECT id FROM reg WHERE email = ?");
        $stmt->execute([$email]);

        if ($stmt->fetch()) {
            $errors[] = "An account with this email already exists.";
        } else {
            $hashed = password_hash($password, PASSWORD_DEFAULT);
            $stmt = $pdo->prepare("INSERT INTO reg (name, contact_no, email, password) VALUES (?, ?, ?, ?)");
            $stmt->execute([$name, $contact_no, $email, $hashed]);

            header("Location: login.php?msg=" . urlencode("Account created successfully. Please sign in.") . "&type=success");
            exit;
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

        <?php if (!empty($errors)): ?>
            <ul class="flash-messages">
                <?php foreach ($errors as $err): ?>
                    <li class="flash error"><?php echo htmlspecialchars($err); ?></li>
                <?php endforeach; ?>
            </ul>
        <?php endif; ?>

        <form action="register.php" method="POST" onsubmit="return validateRegister()" novalidate>
            <h3>Create a New Account</h3><br>

            <div class="form-group">
                <label for="name">Full Name</label>
                <input type="text" id="name" name="name" placeholder="Enter Full Name" required>
                <small class="error-text" id="name-error"></small>
            </div><br>

            <div class="form-group">
                <label for="contact_no">Phone No.</label>
                <input type="tel" id="contact_no" name="contact_no" placeholder="Enter Phone No. 10 digit only" pattern="\d{10}" maxlength="10" required>
                <small class="error-text" id="contact-error"></small>
            </div><br>

            <div class="form-group">
                <label for="email">Email Id</label>
                <input type="email" id="email" name="email" placeholder="Enter Valid Email Id" required>
                <small class="error-text" id="email-error"></small>
            </div><br>

            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" placeholder="Enter Password" minlength="6" required>
                <small class="error-text" id="password-error"></small>
            </div><br>

            <div class="form-group">
                <label for="c_password">Confirm Password</label>
                <input type="password" id="c_password" name="c_password" placeholder="Enter Confirm Password" required>
                <small class="error-text" id="c_password-error"></small>
            </div><br>

            <div class="button-group" style="display: flex; gap: 10px;">
                <button type="submit">Register</button>
                <button type="button" onclick="window.location.href='login.php'">
                    Already have an account? Sign In
                </button>
            </div>
        </form>
    </div>

    <script>
        function validateRegister() {
            let valid = true;

            const name = document.getElementById("name");
            const contact_no = document.getElementById("contact_no");
            const email = document.getElementById("email");
            const password = document.getElementById("password");
            const cPassword = document.getElementById("c_password");

            const nameError = document.getElementById("name-error");
            const contactError = document.getElementById("contact-error");
            const emailError = document.getElementById("email-error");
            const passwordError = document.getElementById("password-error");
            const cPasswordError = document.getElementById("c_password-error");

            [nameError, contactError, emailError, passwordError, cPasswordError].forEach(el => el.textContent = "");

            const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            const phonePattern = /^\d{10}$/;

            if (name.value.trim() === "") {
                nameError.textContent = "Full name is required.";
                valid = false;
            }

            if (!phonePattern.test(contact_no.value.trim())) {
                contactError.textContent = "Enter a valid 10 digit phone number.";
                valid = false;
            }

            if (!emailPattern.test(email.value.trim())) {
                emailError.textContent = "Enter a valid email address.";
                valid = false;
            }

            if (password.value.length < 6) {
                passwordError.textContent = "Password must be at least 6 characters.";
                valid = false;
            }

            if (cPassword.value !== password.value) {
                cPasswordError.textContent = "Passwords do not match.";
                valid = false;
            }

            return valid;
        }
    </script>
</body>
</html>
