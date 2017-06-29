<?php

$servername = "localhost";
$username = "root";
$password = "internet12";

try
{
    $conn = new PDO("mysql:host=$servername;dbname=test_create_DB", $username, $password);
    // set the PDO error mode to exception
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $videoEnable = 0;
    $faceDetection = 0;
    $motionDetection = 0;
    $humanDetection = 0;
    if (strpos($_POST['videoEnable'], 'on') !== false)
    {
      $videoEnable = 1;
    }
    if (strpos($_POST['faceDetection'], 'on') !== false)
    {
      $faceDetection = 1;
    }
    if (strpos($_POST['motionDetection'], 'on') !== false)
    {
      $motionDetection = 1;
    }
    if (strpos($_POST['humanDetection'], 'on') !== false)
    {
      $humanDetection = 1;
    }

    $sql = "UPDATE `HOME_SCANNER_USER_SETTINGS` SET `TEMPERATURE_THRESHOLD`='".$_POST['temperatureThresh']."', `HUMIDITY_THRESHOLD`='".$_POST['humidityThresh']."', `GAS_THRESHOLD`='".$_POST['gasThresh']."', `VIDEO_ENABLED`='".$videoEnable."', `FACE_DETECTION`='".$faceDetection."', `MOTION_DETECTION`='".$motionDetection."', `HUMAN_DETECTION`='".$humanDetection."' WHERE `ID` = 1";

    // use exec() because no results are returned
    $conn->exec($sql);
}
catch(PDOException $e)
{
    echo "Connection failed: " . $e->getMessage();
    die("");
}

header("Location:../pages/settings.php");

?>
