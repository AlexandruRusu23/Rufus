<?php

function redirect($url) {
    ob_start();
    header('Location: '.$url);
    ob_end_flush();
    die();
}

session_start();
if (!isset($_SESSION['user_email']))
{
  redirect("../pages/login.php");
}
$account_name = $_SESSION['user_first_name'] .' '. $_SESSION['user_last_name'];

$servername = "localhost";
$username = "root";
$password = "internet12";

$ambianceRecords = 0;
$videosRecords = 0;
$notificationsList = array();
$timelineList = array();

try
{
    $conn = new PDO("mysql:host=$servername;dbname=test_create_DB", $username, $password);
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    # ambiance records
    $stmt = $conn->prepare("SELECT count(value) as 'value' FROM HOME_SCANNER_DATABASE_TEMPERATURE");
    $stmt->execute();
    $result = $stmt->setFetchMode(PDO::FETCH_ASSOC);
    foreach($stmt->fetchAll() as $k=>$v) {
      $ambianceRecords = $ambianceRecords + $v['value'];
    }
    $stmt = $conn->prepare("SELECT count(value) as 'value' FROM HOME_SCANNER_DATABASE_HUMIDITY");
    $stmt->execute();
    $result = $stmt->setFetchMode(PDO::FETCH_ASSOC);
    foreach($stmt->fetchAll() as $k=>$v) {
      $ambianceRecords = $ambianceRecords + $v['value'];
    }
    $stmt = $conn->prepare("SELECT count(value) as 'value' FROM HOME_SCANNER_DATABASE_LIGHT");
    $stmt->execute();
    $result = $stmt->setFetchMode(PDO::FETCH_ASSOC);
    foreach($stmt->fetchAll() as $k=>$v) {
      $ambianceRecords = $ambianceRecords + $v['value'];
    }
    $stmt = $conn->prepare("SELECT count(value) as 'value' FROM HOME_SCANNER_DATABASE_GAS_RECORD");
    $stmt->execute();
    $result = $stmt->setFetchMode(PDO::FETCH_ASSOC);
    foreach($stmt->fetchAll() as $k=>$v) {
      $ambianceRecords = $ambianceRecords + $v['value'];
    }
    $stmt = $conn->prepare("SELECT count(value) as 'value' FROM HOME_SCANNER_DATABASE_MOTION");
    $stmt->execute();
    $result = $stmt->setFetchMode(PDO::FETCH_ASSOC);
    foreach($stmt->fetchAll() as $k=>$v) {
      $ambianceRecords = $ambianceRecords + $v['value'];
    }

    # video numbers
    $stmt = $conn->prepare("SELECT count(value) as 'value' FROM HOME_SCANNER_VIDEO_FILES");
    $stmt->execute();
    $result = $stmt->setFetchMode(PDO::FETCH_ASSOC);
    foreach($stmt->fetchAll() as $k=>$v) {
      $videosRecords = $v['value'];
    }

    # notifications
    $stmt = $conn->prepare("SELECT value, time_collected FROM HOME_SCANNER_NOTIFICATIONS ORDER BY TIME_COLLECTED DESC LIMIT 13");
    $stmt->execute();
    $result = $stmt->setFetchMode(PDO::FETCH_ASSOC);
    foreach($stmt->fetchAll() as $k=>$v) {
        $notificationsList[(string)$v['time_collected']] = (string)$v['value'];
    }

    # timeline
    $stmt = $conn->prepare("SELECT value, time_collected FROM HOME_SCANNER_NOTIFICATIONS WHERE value LIKE '%GAS%' ORDER BY TIME_COLLECTED DESC LIMIT 5");
    $stmt->execute();
    $result = $stmt->setFetchMode(PDO::FETCH_ASSOC);
    foreach($stmt->fetchAll() as $k=>$v) {
        $timelineList[(string)$v['time_collected']] = (string)$v['value'];
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
</head>

<body>
  <div id="wrapper">

      <nav class="navbar navbar-default">
        <div class="container">
          <!-- Brand and toggle get grouped for better mobile display -->
          <div class="navbar-header">
            <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1" aria-expanded="false">
              <span class="sr-only">Toggle navigation</span>
              <span class="icon-bar"></span>
              <span class="icon-bar"></span>
              <span class="icon-bar"></span>
            </button>
            <a class="navbar-brand" href="../pages/index.php"><img alt="Brand" src="../images/logo/logo4.png" class="img-responsive"/></a>
          </div>

        <!-- Collect the nav links, forms, and other content for toggling -->
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
                  <?php
                  echo $account_name;
                  ?>
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
                    <a href="../php/logoutManager.php">
                      <i class="fa fa-sign-out" aria-hidden="true"></i>
                      Logout
                    </a>
                  </li>
                </ul>
              </li>
            </ul>
          </div>
          <!-- /.navbar-collapse -->
        </div>
        <!-- /.container-fluid -->
      </nav>
      <!-- /.navbar -->

        <div class="container">
            <!-- /.row -->
            <div class="row">
                <div class="col-lg-4 col-md-5">
                    <div class="panel panel-success">
                        <div class="panel-heading">
                            <div class="row">
                                <div class="col-xs-3">
                                    <i class="fa fa-leaf fa-5x"></i>
                                </div>
                                <div class="col-xs-9 text-right">
                                    <div class="h3">
                                      <strong>
                                        <?php
                                          print $ambianceRecords;
                                        ?>
                                        records
                                      </strong>
                                    </div>
                                    <div>Ambiance Watcher</div>
                                </div>
                            </div>
                        </div>
                        <a href="../pages/ambiance.php">
                            <div class="panel-footer panel-success">
                                <span class="pull-left text-success">View Details</span>
                                <span class="pull-right text-success"><i class="fa fa-arrow-circle-right fa-2x"></i></span>
                                <div class="clearfix"></div>
                            </div>
                        </a>
                    </div>
                </div>
                <div class="col-lg-4 col-md-5">
                    <div class="panel panel-danger">
                        <div class="panel-heading">
                            <div class="row">
                                <div class="col-xs-3">
                                    <i class="fa fa-eye fa-5x"></i>
                                </div>
                                <div class="col-xs-9 text-right">
                                    <div class="h3">
                                      <strong>
                                        <?php
                                          print $videosRecords;
                                        ?>
                                      </strong>
                                    </div>
                                    <div>Surveillance</div>
                                </div>
                            </div>
                        </div>
                        <a href="../pages/surveillance.php">
                            <div class="panel-footer panel-danger">
                                <span class="pull-left text-danger">View Details</span>
                                <span class="pull-right text-danger"><i class="fa fa-arrow-circle-right fa-2x"></i></span>
                                <div class="clearfix"></div>
                            </div>
                        </a>
                    </div>
                </div>
                <div class="col-lg-4 col-md-5">
                    <div class="panel panel-warning">
                        <div class="panel-heading">
                            <div class="row">
                                <div class="col-xs-3">
                                    <i class="fa fa-cogs fa-5x"></i>
                                </div>
                                <div class="col-xs-9 text-right">
                                    <div class="h3"><strong>Ready!</strong></div>
                                    <div>Settings</div>
                                </div>
                            </div>
                        </div>
                        <a href="../pages/settings.php">
                            <div class="panel-footer panel-warning">
                                <span class="pull-left text-warning">View Details</span>
                                <span class="pull-right text-warning"><i class="fa fa-arrow-circle-right fa-2x"></i></span>
                                <div class="clearfix"></div>
                            </div>
                        </a>
                    </div>
                </div>
            </div>
            <!-- /.row -->

            <div class="row">
                <div class="col-lg-8">
                    <div class="panel panel-default">
                        <div class="panel-heading">
                            <i class="fa fa-clock-o fa-fw"></i>Timeline
                        </div>
                        <!-- /.panel-heading -->
                        <div class="panel-body">
                          <div class="list-group">
                            <?php
                              foreach ($timelineList as $key => $value)
                              {
                                $postTitle = "";
                                $postContent = "";
                                if (strpos($value, 'ON') !== false)
                                {
                                  $postTitle = "GAS ALARM ENABLED!!!";
                                  $postContent = "The sistem detected that the gas and smoke concentration in the air exceeded the set threshold.";
                                }
                                else {
                                  $postTitle = "Air is clean.";
                                  $postContent = "Following routine checks, the system did not detect any alarm cases.";
                                }
                                echo "<a class=\"list-group-item list-group-item-action flex-column align-items-start\">
                                  <div class=\"d-flex w-100 justify-content-between\">
                                    <h4 class=\"mb-0\"><i class=\"fa fa-cogs fa-fw\"></i> $postTitle </h4>
                                    <span class=\"pull-top text-muted small\"><em> $key </em>
                                  </div>
                                  <p class=\"h5\">
                                    $postContent
                                  </p>
                                </a>";
                              }
                            ?>
                          </div>
                        </div>
                        <!-- /.panel-body -->
                    </div>
                    <!-- /.panel -->
                </div>
                <!-- /.col-lg-8 -->
                <div class="col-lg-4">
                    <div class="panel panel-default">
                        <div class="panel-heading">
                            <i class="fa fa-bell fa-fw"></i> Notifications Panel
                        </div>
                        <!-- /.panel-heading -->
                        <div class="panel-body">
                            <div class="list-group">
                                <?php
                                  foreach ($notificationsList as $key => $value) {
                                    $iconType = "fa-warning";
                                    $notificationMessage = "";
                                    if (strpos($value, 'MOTION') !== false)
                                    {
                                      $iconType = "fa-eye";
                                      $notificationMessage = "Motion detected.";
                                    }
                                    if (strpos($value, 'TEMP') !== false)
                                    {
                                      $iconType = "fa-thermometer-empty";
                                      if (strpos($value, 'HIGHER') !== false)
                                      {
                                        $notificationMessage = "Higher temperature!";
                                      }
                                      else {
                                        $notificationMessage = "Temperature stable.";
                                      }
                                    }
                                    if (strpos($value, 'HUMI') !== false)
                                    {
                                      $iconType = "fa-tint";
                                      if (strpos($value, 'HIGHER') !== false)
                                      {
                                        $notificationMessage = "Higher humidity!";
                                      }
                                      else {
                                        $notificationMessage = "Humidity stable.";
                                      }
                                    }
                                    if (strpos($value, 'GAS') !== false)
                                    {
                                      if (strpos($value, 'ON') !== false)
                                      {
                                        $notificationMessage = "GAS ALARM ENABLED!!!";
                                      }
                                      else {
                                        $notificationMessage = "Air is clean.";
                                      }
                                    }
                                    echo "
                                      <a href=\"#\" class=\"list-group-item\">
                                          <i class=\"fa $iconType fa-fw\"></i> $notificationMessage
                                          <span class=\"pull-right text-muted small\"><em>$key</em>
                                          </span>
                                      </a>
                                    ";
                                  }
                                ?>
                            </div>
                            <!-- /.list-group -->
                            <a href="../pages/notifications.php" class="btn btn-default btn-block">View All Alerts</a>
                        </div>
                        <!-- /.panel-body -->
                    </div>
                    <!-- /.panel -->

                </div>
                <!-- /.col-lg-4 -->
            </div>
            <!-- /.row -->
          </div>

        </div>
</body>
</html>
