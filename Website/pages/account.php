<?php
function redirect($url) {
    ob_start();
    header('Location: '.$url);
    ob_end_flush();
    die();
}

session_start();
if (!isset($_SESSION['user_email'])) { redirect("../pages/login.php"); }
$account_name = $_SESSION['user_first_name'] .' '. $_SESSION['user_last_name'];
$user_first_name = $_SESSION['user_first_name'];
$user_last_name = $_SESSION['user_last_name'];
$user_email = $_SESSION['user_email'];
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
          <div class="navbar-header">
            <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1" aria-expanded="false">
              <span class="sr-only">Toggle navigation</span>
              <span class="icon-bar"></span>
              <span class="icon-bar"></span>
              <span class="icon-bar"></span>
            </button>
            <a class="navbar-brand" href="../pages/index.php"><i class="fa fa-user fa-fw fa-3x" aria-hidden="true"></i></a>
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
        </div>
      </nav>
      <div class="row">
        <div class="col-md-4 col-md-offset-4">
          <div id="registerBlock" class="login-panel panel panel-default">
              <div class="panel-heading">
                  <h3 class="panel-title">Update your account details.</h3>
              </div>
              <div class="panel-body">
                  <form role="form" method="post" action="../php/accountManager.php">
                      <fieldset>
                          <div class="form-group">
                              <input class="form-control" placeholder="First Name" name="firstName" type="text" value="<?php echo $user_first_name ?>" autofocus>
                          </div>
                          <div class="form-group">
                              <input class="form-control" placeholder="Last Name" name="lastName" value="<?php echo $user_last_name ?>" type="text">
                          </div>
                          <div class="form-group">
                              <input class="form-control" placeholder="E-mail" name="email" value="<?php echo $user_email ?>" type="email">
                          </div>
                          <div class="form-group">
                              <input class="form-control" placeholder="Password" name="password" type="password" value="">
                          </div>
                          <div class="form-group">
                              <input class="form-control" placeholder="Repeat Password" name="repeatPassword" type="password" value="">
                          </div>
                          <button type="submit" class="btn btn-lg btn-success btn-block">Update</button>
                      </fieldset>
                  </form>
              </div>
            </div>
          </div>
        </div>
    </div>
  </body>
  </html>
