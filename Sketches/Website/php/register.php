<?php

$servername = "localhost";
$username = "root";
$password = "internet12";

if(md5($_POST['password']) == md5($_POST['repeatPassword']))
{
  try {
      $conn = new PDO("mysql:host=$servername;dbname=test_create_DB", $username, $password);
      // set the PDO error mode to exception
      $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
      $sql = "INSERT INTO web_members (FirstName, LastName, Email, Password)
      VALUES ('".$_POST['firstName']."', '".$_POST['lastName']."', '".$_POST['email']."', '".md5($_POST['password'])."')";
      // use exec() because no results are returned
      $conn->exec($sql);
      echo "Connected successfully";
      }
  catch(PDOException $e)
      {
      echo "Connection failed: " . $e->getMessage();
      }

  header("Location:../pages/dashboard.html");
}
else
{
  header("Location:../pages/index.html");
}

?>
