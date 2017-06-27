<?php

$servername = "localhost";
$username = "root";
$password = "internet12";

function redirect($url) {
    ob_start();
    header('Location: '.$url);
    ob_end_flush();
    die();
}

try
{
  $conn = new PDO("mysql:host=$servername;dbname=test_create_DB", $username, $password);
  $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

  $stmt = $conn->prepare("SELECT Id, FirstName, LastName, Password FROM web_members WHERE Email = '".$_POST['email']."'");
  $stmt->execute();

  $result = $stmt->setFetchMode(PDO::FETCH_ASSOC);
  foreach($stmt->fetchAll() as $k=>$v)
  {
    if(md5($_POST['password']) == $v['Password'])
    {
      session_start();
      $_SESSION['user_id'] = $v['Id'];
      $_SESSION['user_email'] = $_POST['email'];
      $_SESSION['user_first_name'] = $v['FirstName'];
      $_SESSION['user_last_name'] = $v['LastName'];
      redirect("../pages/index.php");
    }
    else
    {
      redirect("../pages/login.php");
    }
  }
}
catch(PDOException $e)
{
    die($e->getMessage());
    echo "Connection failed: " . $e->getMessage();
}

redirect("../pages/login.php");

?>
