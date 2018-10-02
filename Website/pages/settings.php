<?php

function redirect($url) {
    ob_start();
    header('Location: '.$url);
    ob_end_flush();
    die();
}

$servername = "localhost";
$username = "root";
$password = "internet12";

session_start();
if (!isset($_SESSION['user_email'])) { redirect("../pages/login.php"); }
$account_name = $_SESSION['user_first_name'] .' '. $_SESSION['user_last_name'];

$temperatureThresh = 0;
$humidityThresh = 0;
$gasThresh = 0;
$surveillanceVideo = 0;
$faceDetection = 0;
$motionDetection = 0;
$humanDetection = 0;

try
{
    $conn = new PDO("mysql:host=$servername;dbname=test_create_DB", $username, $password);
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    $stmt = $conn->prepare("SELECT `TEMPERATURE_THRESHOLD`, `HUMIDITY_THRESHOLD`, `GAS_THRESHOLD`, `VIDEO_ENABLED`, `FACE_DETECTION`, `MOTION_DETECTION`, `HUMAN_DETECTION` FROM `HOME_SCANNER_USER_SETTINGS`");
    $stmt->execute();

    $result = $stmt->setFetchMode(PDO::FETCH_ASSOC);
    foreach($stmt->fetchAll() as $k=>$v)
    {
        $temperatureThresh = $v['TEMPERATURE_THRESHOLD'];
        $humidityThresh = $v['HUMIDITY_THRESHOLD'];
        $gasThresh = $v['GAS_THRESHOLD'];
        $surveillanceVideo = $v['VIDEO_ENABLED'];
        $faceDetection = $v['FACE_DETECTION'];
        $motionDetection = $v['MOTION_DETECTION'];
        $humanDetection = $v['HUMAN_DETECTION'];
    }
}
catch(PDOException $e)
{
    die($e->getMessage());
    echo "Connection failed: " . $e->getMessage();
}
?>

<html>
<head>
  <title>Rufus - Home Smart Assistant</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
  <link rel="stylesheet" href="../css/style.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
  <script src="js/script.js"></script>
  <script type="text/javascript">

  function updateCheck(checker)
  {
    if (checker.id == 'surveillance_module')
    {
      if (checker.checked == true)
      {
        document.getElementById("face_detection").disabled = false;
        document.getElementById("motion_detection").disabled = false;
        document.getElementById("human_detection").disabled = false;
      }
      else {
        document.getElementById("face_detection").disabled = true;
        document.getElementById("motion_detection").disabled = true;
        document.getElementById("human_detection").disabled = true;
      }
    }
  }
  </script>

</head>
<body>
  <div id="wrapper">
      <nav class="navbar navbar-default">
        <div class="container">
          <div class="navbar-header">
            <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1" aria-expanded="false">
              <span class="sr-only">Toggle navigation</span>
              <span class="icon-bar"></span>
              <span class="icon-bar"></span>
              <span class="icon-bar"></span>
            </button>
            <a class="navbar-brand" href="../pages/index.php"><img alt="Brand" src="../images/logo/logo1.png" class="img-responsive"/></a>
          </div>
          <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
            <ul class="nav navbar-nav">
              <li><a href="../pages/index.php"><i class="fa fa-home fa-fw" aria-hidden="true"></i>Home</a>
              </li>
              <li class="dropdown">
                <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Menu <i class="fa fa-caret-down" aria-hidden="true"></i></span></a>
                <ul class="dropdown-menu">
                  <li><a href="../pages/ambiance.php"><i class="fa fa-server fa-fw" aria-hidden="true"></i> Ambiance Watcher</a>
                  </li>
                  <li><a href="../pages/surveillance.php"><i class="fa fa-video-camera fa-fw" aria-hidden="true"></i> Surveillance</a>
                  </li>
                  <li role="separator" class="divider"></li>
                  <li><a href="../pages/settings.php"><i class="fa fa-wrench fa-fw" aria-hidden="true"></i> Configuration Board</a>
                  </li>
                </ul>
              </li>
            </ul>

          <ul class="nav navbar-nav navbar-right">
              <li class="dropdown">
                <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">
                  <i class="fa fa-user-circle-o fa-fw" aria-hidden="true"></i>
                  <?php echo $account_name; ?>
                  <i class="fa fa-caret-down" aria-hidden="true"></i>
                </a>
                <ul class="dropdown-menu">
                  <li>
                    <a href="../pages/account.php"><i class="fa fa-user fa-fw" aria-hidden="true"></i> Account</a>
                  </li>
                  <li role="separator" class="divider"></li>
                  <li><a href="../pages/settings.php"><i class="fa fa-cogs fa-fw" aria-hidden="true"></i> Rufus Settings</a>
                  </li>
                  <li role="separator" class="divider"></li>
                  <li>
                    <a href="../php/logoutManager.php"> <i class="fa fa-sign-out" aria-hidden="true"></i> Logout </a>
                  </li>
                </ul>
              </li>
            </ul>
          </div>
        </div>
      </nav>
      <div class="container">
        <div class="row">
          <div class="col-md-4 col-md-offset-4">
            <div id="settingsBlock" class="login-panel panel panel-default">
                <div class="panel-heading">
                    <h3 class="panel-title">Adjust the assistant settings.</h3>
                </div>
                <div class="panel-body">
                    <form role="form" method="post" action="../php/settingsManager.php">
                        <fieldset>
                            <div class="form-group">
                                <label>Temperature Threshold:</label>
                                <input id="tempThreshInput" class="form-control" placeholder="Temperature Threshold" name="temperatureThresh"
                                value= <?php echo (int)$temperatureThresh; ?>
                                type="number" min=-15 max=35 autofocus>
                            </div>
                            <div class="form-group">
                                <label>Humidity Threshold:</label>
                                <input id="humiThreshInput" class="form-control" placeholder="Humidity Threshold" name="humidityThresh"
                                value= <?php echo (int)$humidityThresh; ?>
                                type="number" min=20 max=80>
                            </div>
                            <div class="form-group">
                                <label>Gas Threshold:</label>
                                <input class="form-control" placeholder="Gas Threshold" name="gasThresh"
                                value= <?php echo (int)$gasThresh; ?>
                                type="number" min=200 max=500>
                            </div>

                            <div class="form-group">
                              <label>Video Settings:</label>
                              <div class="form-group">
                                <input type="checkbox" id="surveillance_module" name="videoEnable" class="checkbox" onclick="updateCheck(this)"
                                <?php if ($surveillanceVideo == 1) echo " checked "; ?>
                                />
                                <label for="surveillance_module">Surveillance Module</label>
                              </div>
                                <div class="form-group">
                                  <input type="checkbox" id="face_detection" name="faceDetection" class="checkbox" onclick="updateCheck(this)"
                                  <?php
                                    if ($surveillanceVideo == 0)
                                      echo " disabled ";
                                    if ($faceDetection == 1)
                                      echo " checked ";
                                  ?>
                                  />
                                  <label for="face_detection">Face Detection</label>
                                </div>
                                <div class="form-group">
                                  <input type="checkbox" id="motion_detection" name="motionDetection" class="checkbox" onclick="updateCheck(this)"
                                  <?php
                                    if ($surveillanceVideo == 0)
                                      echo " disabled ";
                                    if ($motionDetection == 1)
                                      echo " checked ";
                                  ?>
                                  />
                                  <label for="motion_detection">Motion Detection</label>
                                </div>
                                <div class="form-group">
                                  <input type="checkbox" id="human_detection" name="humanDetection" class="checkbox" onclick="updateCheck(this)"
                                  <?php
                                    if ($surveillanceVideo == 0)
                                      echo " disabled ";
                                    if ($humanDetection == 1)
                                      echo " checked ";
                                  ?>
                                  />
                                  <label for="human_detection">Human Detection</label>
                                </div>
                            </div>
                            <button type="submit" class="btn btn-lg btn-success btn-block">Save changes</button>
                        </fieldset>
                    </form>
                </div>
              </div>
            </div>
        </div>
      </div>
    </div>
  </body>
  </html>
