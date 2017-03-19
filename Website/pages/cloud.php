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
            <a class="navbar-brand" href="../pages/index.php"><img alt="Brand" src="../images/logo/logo2.png" class="img-responsive"/></a>
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
              <li><a href="#"><i class="fa fa-mobile fa-fw" aria-hidden="true"></i>Contact</a>
              </li>
              <li class="dropdown">
                <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false"><i class="fa fa-user-circle-o fa-fw" aria-hidden="true"></i>User Name <i class="fa fa-caret-down" aria-hidden="true"></i></a>
                <ul class="dropdown-menu">
                  <li>
                    <a href="#"><i class="fa fa-user fa-fw" aria-hidden="true"></i> Account</a>
                  </li>
                  <li><a href="#"><i class="fa fa-cog fa-fw" aria-hidden="true"></i> Account Settings</a>
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

        <div class="row">
          <div class="col-lg-3 col-md-6">
              <div class="panel panel-primary">
                  <div class="panel-heading">
                      <div class="row">
                          <div class="col-xs-3">
                              <i class="fa fa-folder fa-5x" aria-hidden="true"></i>
                          </div>
                          <div class="col-xs-9 text-right">
                              <div class="h3"><strong>My Folder</strong></div>
                              <div>32 files</div>
                          </div>
                      </div>
                  </div>
                  <a href="../pages/cloud.php">
                      <div class="panel-footer panel-primary">
                          <span class="pull-left text-primary">View Files</span>
                          <span class="pull-right text-primary"><i class="fa fa-arrow-circle-right fa-2x"></i></span>
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
                              <i class="fa fa-file fa-5x" aria-hidden="true"></i>
                          </div>
                          <div class="col-xs-9 text-right">
                              <div class="h3"><strong>1.5 MB</strong></div>
                              <div>Unknown File</div>
                          </div>
                      </div>
                  </div>
                  <a href="../pages/cloud.php">
                      <div class="panel-footer panel-primary">
                          <span class="pull-left text-primary">Download</span>
                          <span class="pull-right text-primary"><i class="fa fa-download fa-2x" aria-hidden="true"></i></i></span>
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
                              <i class="fa fa-file-code-o fa-5x" aria-hidden="true"></i>
                          </div>
                          <div class="col-xs-9 text-right">
                              <div class="h3"><strong>388 KB</strong></div>
                              <div>Code File</div>
                          </div>
                      </div>
                  </div>
                  <a href="../pages/cloud.php">
                      <div class="panel-footer panel-primary">
                          <span class="pull-left text-primary">Download</span>
                          <span class="pull-right text-primary"><i class="fa fa-download fa-2x" aria-hidden="true"></i></i></span>
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
                              <i class="fa fa-file-archive-o fa-5x" aria-hidden="true"></i>
                          </div>
                          <div class="col-xs-9 text-right">
                              <div class="h3"><strong>233 MB</strong></div>
                              <div>Archive</div>
                          </div>
                      </div>
                  </div>
                  <a href="../pages/cloud.php">
                      <div class="panel-footer panel-primary">
                          <span class="pull-left text-primary">Download</span>
                          <span class="pull-right text-primary"><i class="fa fa-download fa-2x" aria-hidden="true"></i></i></span>
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
                              <i class="fa fa-file-word-o fa-5x" aria-hidden="true"></i>
                          </div>
                          <div class="col-xs-9 text-right">
                              <div class="h3"><strong>15 MB</strong></div>
                              <div>Word Document</div>
                          </div>
                      </div>
                  </div>
                  <a href="../pages/cloud.php">
                      <div class="panel-footer panel-primary">
                          <span class="pull-left text-primary">Download</span>
                          <span class="pull-right text-primary"><i class="fa fa-download fa-2x" aria-hidden="true"></i></i></span>
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
                              <i class="fa fa-file-pdf-o fa-5x" aria-hidden="true"></i>
                          </div>
                          <div class="col-xs-9 text-right">
                              <div class="h3"><strong>42 MB</strong></div>
                              <div>PDF Document</div>
                          </div>
                      </div>
                  </div>
                  <a href="../pages/cloud.php">
                      <div class="panel-footer panel-primary">
                          <span class="pull-left text-primary">Download</span>
                          <span class="pull-right text-primary"><i class="fa fa-download fa-2x" aria-hidden="true"></i></i></span>
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
                              <i class="fa fa-file-text-o fa-5x" aria-hidden="true"></i>
                          </div>
                          <div class="col-xs-9 text-right">
                              <div class="h3"><strong>1012 KB </strong></div>
                              <div>Text File</div>
                          </div>
                      </div>
                  </div>
                  <a href="../pages/cloud.php">
                      <div class="panel-footer panel-primary">
                          <span class="pull-left text-primary">Download</span>
                          <span class="pull-right text-primary"><i class="fa fa-download fa-2x" aria-hidden="true"></i></i></span>
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
                              <i class="fa fa-file-powerpoint-o fa-5x" aria-hidden="true"></i>
                          </div>
                          <div class="col-xs-9 text-right">
                              <div class="h3"><strong>77 MB</strong></div>
                              <div>Power Point Document</div>
                          </div>
                      </div>
                  </div>
                  <a href="../pages/cloud.php">
                      <div class="panel-footer panel-primary">
                          <span class="pull-left text-primary">Download</span>
                          <span class="pull-right text-primary"><i class="fa fa-download fa-2x" aria-hidden="true"></i></i></span>
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
                              <i class="fa fa-file-video-o fa-5x" aria-hidden="true"></i>
                          </div>
                          <div class="col-xs-9 text-right">
                              <div class="h3"><strong>2.32 GB</strong></div>
                              <div>Video File</div>
                          </div>
                      </div>
                  </div>
                  <a href="../pages/cloud.php">
                      <div class="panel-footer panel-primary">
                          <span class="pull-left text-primary">Download</span>
                          <span class="pull-right text-primary"><i class="fa fa-download fa-2x" aria-hidden="true"></i></i></span>
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
                            <i class="fa fa-file-audio-o fa-5x" aria-hidden="true"></i>
                          </div>
                          <div class="col-xs-9 text-right">
                              <div class="h3"><strong>15 MB</strong></div>
                              <div>Audio File</div>
                          </div>
                      </div>
                  </div>
                  <a href="../pages/cloud.php">
                      <div class="panel-footer panel-primary">
                          <span class="pull-left text-primary">Download</span>
                          <span class="pull-right text-primary"><i class="fa fa-download fa-2x" aria-hidden="true"></i></i></span>
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
                              <i class="fa fa-file-excel-o fa-5x" aria-hidden="true"></i>
                          </div>
                          <div class="col-xs-9 text-right">
                              <div class="h3"><strong>33 MB</strong></div>
                              <div>Excel Document</div>
                          </div>
                      </div>
                  </div>
                  <a href="../pages/cloud.php">
                      <div class="panel-footer panel-primary">
                          <span class="pull-left text-primary">Download</span>
                          <span class="pull-right text-primary"><i class="fa fa-download fa-2x" aria-hidden="true"></i></i></span>
                          <div class="clearfix"></div>
                      </div>
                  </a>
              </div>
          </div>
        </div>

      </div>

    </div>

  </body>

  </html>
