<?php
require_once 'session_helper.php';

session_unset();
session_destroy();

header("Location: login.php");
exit;
