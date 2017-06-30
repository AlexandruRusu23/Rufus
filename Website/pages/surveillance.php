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
if (!isset($_SESSION['user_email']))
{
  redirect("../pages/login.php");
}
$account_name = $_SESSION['user_first_name'] .' '. $_SESSION['user_last_name'];

$videosArray = array();

try {
  $conn = new PDO("mysql:host=$servername;dbname=test_create_DB", $username, $password);
  $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

  $stmt = $conn->prepare("SELECT value, time_collected FROM HOME_SCANNER_VIDEO_FILES ORDER BY time_collected DESC");
  $stmt->execute();
  $result = $stmt->setFetchMode(PDO::FETCH_ASSOC);
  foreach($stmt->fetchAll() as $k=>$v) {
      $videosArray[(string)$v['time_collected']] = (string)$v['value'];
  }
  $videosArray = array_reverse($videosArray);
}
catch (PDOException $e) {
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
    function changeVideo(video_source)
    {
      var video = document.getElementById('surveillance_video');
      video.src = '../videos/' + video_source;
      video.play();
    }
  </script>
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
            <a class="navbar-brand" href="../pages/index.php"><img alt="Brand" src="../images/logo/logo3.png" class="img-responsive"/></a>
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
            <div class="col-md-2 col-md-offset-3">
              <video id="surveillance_video" width="640" height="480" controls>
                <source id="surveillance_video_source" src="../videos/test.mp4">
                Your browser does not support the video tag.
              </video>
            </div>
          </div>
        </br>
          <div class="row">

          <?php
            foreach ($videosArray as $key => $value) {
               echo
                "<div class=\"col-lg-3 col-md-6\">
                    <div class=\"panel panel-danger\">
                        <div class=\"panel-heading\">
                            <div class=\"row\">
                                <div class=\"col-xs-3\">
                                    <i class=\"fa fa-film fa-5x\" aria-hidden=\"true\"></i>
                                </div>
                                <div class=\"col-xs-9 text-right\">
                                    <div class=\"h3\"><strong> $key </strong></div>
                                    <div class=\"h6\"> $value </div>
                                </div>
                            </div>
                        </div>
                        <a href=# onclick=\"changeVideo('$value')\">
                            <div class=\"panel-footer panel-danger\">
                                <span class=\"pull-left text-danger\">Watch Video</span>
                                <span class=\"pull-right text-danger\"><i class=\"fa fa-play-circle fa-2x\" aria-hidden=\"true\"></i></span>
                                <div class=\"clearfix\"></div>
                            </div>
                        </a>
                    </div>
                </div>";
              }
            ?>
          </div>
          <!-- /.row -->
        </div>

    </div>

  </body>

  </html>
