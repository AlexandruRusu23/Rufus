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
            <a class="navbar-brand" href="../pages/index.php"><i class="fa fa-bell fa-fw fa-3x"></i></a>
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
                    <div class="panel panel-default">
                        <div class="panel-heading">
                            <i class="fa fa-bell fa-fw"></i> Notifications Panel
                        </div>
                        <!-- /.panel-heading -->
                        <div class="panel-body">
                            <div class="list-group">
                                <a href="#" class="list-group-item">
                                    <i class="fa fa-comment fa-fw"></i> New Comment
                                    <span class="pull-right text-muted small"><em>4 minutes ago</em>
                                    </span>
                                </a>
                                <a href="#" class="list-group-item">
                                    <i class="fa fa-twitter fa-fw"></i> 3 New Followers
                                    <span class="pull-right text-muted small"><em>12 minutes ago</em>
                                    </span>
                                </a>
                                <a href="#" class="list-group-item">
                                    <i class="fa fa-envelope fa-fw"></i> Message Sent
                                    <span class="pull-right text-muted small"><em>27 minutes ago</em>
                                    </span>
                                </a>
                                <a href="#" class="list-group-item">
                                    <i class="fa fa-tasks fa-fw"></i> New Task
                                    <span class="pull-right text-muted small"><em>43 minutes ago</em>
                                    </span>
                                </a>
                                <a href="#" class="list-group-item">
                                    <i class="fa fa-upload fa-fw"></i> Server Rebooted
                                    <span class="pull-right text-muted small"><em>11:32 AM</em>
                                    </span>
                                </a>
                                <a href="#" class="list-group-item">
                                    <i class="fa fa-bolt fa-fw"></i> Server Crashed!
                                    <span class="pull-right text-muted small"><em>11:13 AM</em>
                                    </span>
                                </a>
                                <a href="#" class="list-group-item">
                                    <i class="fa fa-warning fa-fw"></i> Server Not Responding
                                    <span class="pull-right text-muted small"><em>10:57 AM</em>
                                    </span>
                                </a>
                                <a href="#" class="list-group-item">
                                    <i class="fa fa-shopping-cart fa-fw"></i> New Order Placed
                                    <span class="pull-right text-muted small"><em>9:49 AM</em>
                                    </span>
                                </a>
                                <a href="#" class="list-group-item">
                                    <i class="fa fa-money fa-fw"></i> Payment Received
                                    <span class="pull-right text-muted small"><em>Yesterday</em>
                                    </span>
                                </a>
                            </div>
                            <!-- /.list-group -->
                        </div>
                        <!-- /.panel-body -->
                    </div>
                    <!-- /.panel -->
          </div>

    </div>

  </body>

  </html>