<?php

function redirect($url) {
    ob_start();
    header('Location: '.$url);
    ob_end_flush();
    die();
}

session_start();
session_destroy();

redirect("../pages/login.php");

?>
