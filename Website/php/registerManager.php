<?php
$servername = "localhost";
$username = "root";
$password = "internet12";

if(md5($_POST['password']) == md5($_POST['repeatPassword']) && strlen($_POST['password']) >= 8 )
{
  try {
      $conn = new PDO("mysql:host=$servername;dbname=test_create_DB", $username, $password);
      $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
      $sql = "INSERT INTO web_members (FirstName, LastName, Email, Password)
      VALUES ('".$_POST['firstName']."', '".$_POST['lastName']."', '".$_POST['email']."', '".md5($_POST['password'])."')";
      $conn->exec($sql);
      echo "Connected successfully";
      }
  catch(PDOException $e)
      {
      echo "Connection failed: " . $e->getMessage();
      }
  header("Location:../pages/login.php");
}
else
{
  header("Location:../pages/login.php");
}
?>
