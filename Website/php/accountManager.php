<?php
$servername = "localhost";
$username = "root";
$password = "internet12";
session_start();

if (strlen($_POST['firstName']) < 8 || strlen($_POST['lastName']) < 8)
{
  header("Location:../pages/account.php");
}

if(md5($_POST['password']) == md5($_POST['repeatPassword']) && strlen($_POST['password']) >= 8 )
{
  try
  {
      $conn = new PDO("mysql:host=$servername;dbname=test_create_DB", $username, $password);
      $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
      $sql = "UPDATE `web_members` SET `FirstName` = '".$_POST['firstName']."', `LastName` = '".$_POST['lastName']."', `Email` = '".$_POST['email']."', `Password` = '".md5($_POST['password'])."'
      WHERE `Id` = '".$_SESSION['user_id']."'";
      $conn->exec($sql);
  }
  catch(PDOException $e)
  {
      echo "Connection failed: " . $e->getMessage();
  }

  $_SESSION['user_first_name'] = $_POST['firstName'];
  $_SESSION['user_last_name'] = $_POST['lastName'];
  $_SESSION['user_email'] = $_POST['email'];
  header("Location:../pages/account.php");
}
else
{
  header("Location:../pages/login.php");
}
?>
