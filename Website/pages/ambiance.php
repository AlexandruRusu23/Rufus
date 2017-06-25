<?php

$servername = "localhost";
$username = "root";
$password = "internet12";

$temperatureValue = 0;
$humidityValue = 0;
$gasValue = 0;
$lightValue = 0;
$motionValue = 0;

try
{
    $conn = new PDO("mysql:host=$servername;dbname=test_create_DB", $username, $password);
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    $stmt = $conn->prepare("SELECT value FROM HOME_SCANNER_DATABASE_TEMPERATURE WHERE time_collected in (select max(time_collected) from HOME_SCANNER_DATABASE_TEMPERATURE)");
    $stmt->execute();

    $result = $stmt->setFetchMode(PDO::FETCH_ASSOC);
    foreach($stmt->fetchAll() as $k=>$v) {
        $temperatureValue = $v['value'];
    }

    $stmt = $conn->prepare("SELECT value FROM HOME_SCANNER_DATABASE_HUMIDITY WHERE time_collected in (select max(time_collected) from HOME_SCANNER_DATABASE_HUMIDITY)");
    $stmt->execute();

    $result = $stmt->setFetchMode(PDO::FETCH_ASSOC);
    foreach($stmt->fetchAll() as $k=>$v) {
        $humidityValue = $v['value'];
    }

    $stmt = $conn->prepare("SELECT value FROM HOME_SCANNER_DATABASE_GAS_RECORD WHERE time_collected in (select max(time_collected) from HOME_SCANNER_DATABASE_GAS_RECORD)");
    $stmt->execute();

    $result = $stmt->setFetchMode(PDO::FETCH_ASSOC);
    foreach($stmt->fetchAll() as $k=>$v) {
        $gasValue = $v['value'];
    }

    $stmt = $conn->prepare("SELECT value FROM HOME_SCANNER_DATABASE_LIGHT WHERE time_collected in (select max(time_collected) from HOME_SCANNER_DATABASE_LIGHT)");
    $stmt->execute();

    $result = $stmt->setFetchMode(PDO::FETCH_ASSOC);
    foreach($stmt->fetchAll() as $k=>$v) {
        $lightValue = $v['value'];
    }

    $stmt = $conn->prepare("SELECT value FROM HOME_SCANNER_DATABASE_MOTION WHERE time_collected in (select max(time_collected) from HOME_SCANNER_DATABASE_MOTION)");
    $stmt->execute();

    $result = $stmt->setFetchMode(PDO::FETCH_ASSOC);
    foreach($stmt->fetchAll() as $k=>$v) {
        $motionValue = $v['value'];
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
            <!-- <i class="fa fa-television" aria-hidden="true"></i> -->
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
                  <li><a href="../pages/cloud.php"><i class="fa fa-cloud fa-fw" aria-hidden="true"></i> Cloud</a>
                  </li>
                  <li role="separator" class="divider"></li>
                  <li><a href="../pages/settings.php"><i class="fa fa-wrench fa-fw" aria-hidden="true"></i> Configuration Board</a>
                  </li>
                </ul>
              </li>
            </ul>

          <ul class="nav navbar-nav navbar-right">
              <li class="dropdown">
                <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false"><i class="fa fa-user-circle-o fa-fw" aria-hidden="true"></i>User Name <i class="fa fa-caret-down" aria-hidden="true"></i></a>
                <ul class="dropdown-menu">
                  <li>
                    <a href="../pages/account.php"><i class="fa fa-user fa-fw" aria-hidden="true"></i> Account</a>
                  </li>
                  <li role="separator" class="divider"></li>
                  <li><a href="../pages/settings.php"><i class="fa fa-cogs fa-fw" aria-hidden="true"></i> Rufus Settings</a>
                  </li>
                  <li role="separator" class="divider"></li>
                  <li>
                    <form>
                      <button type="submit" class="btn btn-link btn-logout"><i class="fa fa-sign-out" aria-hidden="true"></i> Logout</button>
                    </form>
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
                <div class="col-lg-3 col-md-6">
                    <div class="panel panel-success">
                        <div class="panel-heading">
                            <div class="row">
                                <div class="col-xs-3">
                                    <i class="fa fa-thermometer-half fa-5x" aria-hidden="true"></i>
                                </div>
                                <div class="col-xs-9 text-right">
                                    <div class="h3">
                                      <strong>
                                      <?php
                                        print "$temperatureValue";
                                      ?>
                                        &#8451;
                                      </strong>
                                    </div>
                                    <div>Temperature</div>
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
                <div class="col-lg-3 col-md-6">
                    <div class="panel panel-primary">
                        <div class="panel-heading">
                            <div class="row">
                                <div class="col-xs-3">
                                    <i class="fa fa-tint fa-5x" aria-hidden="true"></i>
                                </div>
                                <div class="col-xs-9 text-right">
                                    <div class="h3">
                                      <strong>
                                      <?php
                                        print "$humidityValue";
                                      ?>
                                      %
                                      </strong>
                                    </div>
                                    <div>Humidity</div>
                                </div>
                            </div>
                        </div>
                        <a href="../pages/ambiance.php">
                            <div class="panel-footer panel-primary">
                                <span class="pull-left text-primary">View Details</span>
                                <span class="pull-right text-primary"><i class="fa fa-arrow-circle-right fa-2x"></i></span>
                                <div class="clearfix"></div>
                            </div>
                        </a>
                    </div>
                </div>
                <div class="col-lg-3 col-md-6">
                    <div class="panel panel-danger">
                        <div class="panel-heading">
                            <div class="row">
                                <div class="col-xs-3">
                                    <i class="fa fa-fire fa-5x" aria-hidden="true"></i>
                                </div>
                                <div class="col-xs-9 text-right">
                                    <div class="h3">
                                      <strong>
                                      <?php
                                        print number_format($gasValue / 1024 * 100, 2);
                                      ?>
                                      %
                                      </strong>
                                    </div>
                                    <div>Smoke and Gas</div>
                                </div>
                            </div>
                        </div>
                        <a href="../pages/ambiance.php">
                            <div class="panel-footer panel-danger">
                                <span class="pull-left text-danger">View Details</span>
                                <span class="pull-right text-danger"><i class="fa fa-arrow-circle-right fa-2x"></i></span>
                                <div class="clearfix"></div>
                            </div>
                        </a>
                    </div>
                </div>
                <div class="col-lg-3 col-md-6">
                    <div class="panel panel-warning">
                        <div class="panel-heading">
                            <div class="row">
                                <div class="col-xs-3">
                                    <i class="fa fa-lightbulb-o fa-5x" aria-hidden="true"></i>
                                </div>
                                <div class="col-xs-9 text-right">
                                    <div class="h3">
                                      <strong>
                                      <?php
                                        print number_format($lightValue / 1024 * 100, 2);
                                      ?>
                                      %
                                      </strong>
                                    </div>
                                    <div>Light</div>
                                </div>
                            </div>
                        </div>
                        <a href="../pages/ambiance.php">
                            <div class="panel-footer panel-warning">
                                <span class="pull-left text-warning">View Details</span>
                                <span class="pull-right text-warning"><i class="fa fa-arrow-circle-right fa-2x"></i></span>
                                <div class="clearfix"></div>
                            </div>
                        </a>
                    </div>
                </div>
                <div class="col-lg-3 col-md-6">
                    <div class="panel panel-info">
                        <div class="panel-heading">
                            <div class="row">
                                <div class="col-xs-3">
                                    <i class="fa fa-eye fa-5x" aria-hidden="true"></i>
                                </div>
                                <div class="col-xs-9 text-right">
                                    <div class="h3">
                                      <strong>
                                      <?php
                                        if ($motionValue > 0)
                                        {
                                          print 'Suspicious';
                                        }
                                        else {
                                          print 'Stable';
                                        }
                                      ?>
                                      </strong>
                                    </div>
                                    <div>Motion</div>
                                </div>
                            </div>
                        </div>
                        <a href="../pages/ambiance.php">
                            <div class="panel-footer panel-info">
                                <span class="pull-left text-info">View Details</span>
                                <span class="pull-right text-info"><i class="fa fa-arrow-circle-right fa-2x"></i></span>
                                <div class="clearfix"></div>
                            </div>
                        </a>
                    </div>
                </div>
            </div>
            <!-- /.row -->
        </div>

    </div>

  </body>

  </html>
