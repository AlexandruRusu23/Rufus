<?php

$servername = "localhost";
$username = "root";
$password = "internet12";

try
{
    $conn = new PDO("mysql:host=$servername;dbname=test_create_DB", $username, $password);
    // set the PDO error mode to exception
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    $stmt = $conn->prepare("SELECT Password FROM web_members WHERE Email = '".$_POST['email']."'");
    $stmt->execute();

    // set the resulting array to associative
    $result = $stmt->setFetchMode(PDO::FETCH_ASSOC);
    foreach($stmt->fetchAll() as $k=>$v) {
        if(md5($_POST['password']) == $v['Password'])
        {
          header("Location:../pages/index.php");
        }
        else
        {
          header("Location:../pages/login.php");
        }
    }

}
catch(PDOException $e)
{
    die($e->getMessage());
    echo "Connection failed: " . $e->getMessage();
}

header("Location:../pages/login.php");

?>
