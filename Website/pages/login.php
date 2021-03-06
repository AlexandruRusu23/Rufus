<html>
<head>
  <title>Rufus - Home Smart Assistant</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
  <script src="../js/script.js"></script>
</head>

<body>
  <div class="jumbotron text-center">
    <img src="../images/logo/logo1.png">
    <img src="../images/logo/logo2.png">
    <img src="../images/logo/logo3.png">
    <img src="../images/logo/logo4.png">
    <h1>Rufus - Home Smart Assistant</h1>
    <p>Welcome to your personal home smart assistant interface control.</p>
  </div>
  <br>
  <br>
  <div class="container">
    <div class="row">
      <div class="col-md-4 col-md-offset-4">
        <div id="registerBlock" class="login-panel panel panel-default">
            <div class="panel-heading">
                <h3 class="panel-title">Register a new account</h3>
            </div>
            <div class="panel-body">
                <form role="form" method="post" action="../php/registerManager.php">
                    <fieldset>
                        <div class="form-group">
                            <input class="form-control" placeholder="First Name" name="firstName" type="text" autofocus>
                        </div>
                        <div class="form-group">
                            <input class="form-control" placeholder="Last Name" name="lastName" type="text">
                        </div>
                        <div class="form-group">
                            <input class="form-control" placeholder="E-mail" name="email" type="email">
                        </div>
                        <div class="form-group">
                            <input class="form-control" placeholder="Password" name="password" type="password" value="">
                        </div>
                        <div class="form-group">
                            <input class="form-control" placeholder="Repeat Password" name="repeatPassword" type="password" value="">
                        </div>
                        <div id="registerRecommandation" class="form-group">
                          <p1>Already registered?</p1>
                          <a href=# onclick="showLoginBlock()">Sign In to Rufus now.</a>
                        </div>
                        <button type="submit" class="btn btn-lg btn-success btn-block">Register</button>
                    </fieldset>
                </form>
            </div>
          </div>
        </div>
        <div class="col-md-4 col-md-offset-4">
          <div id="loginBlock" class="login-panel panel panel-default">
              <div class="panel-heading">
                  <h3 class="panel-title">Sign In to Rufus</h3>
              </div>
              <div class="panel-body">
                  <form role="form" method="post" action="../php/loginManager.php">
                      <fieldset>
                          <div class="form-group">
                              <input class="form-control" placeholder="E-mail" name="email" type="email" autofocus>
                          </div>
                          <div class="form-group">
                              <input class="form-control" placeholder="Password" name="password" type="password" value="">
                          </div>
                          <div id="registerRecommandation" class="form-group">
                            <p1>New to Rufus?</p1>
                            <a href=# onclick="showRegisterBlock()">Register an account now.</a>
                          </div>
                          <button type="submit" class="btn btn-lg btn-success btn-block">Login</button>
                      </fieldset>
                  </form>
              </div>
          </div>
        </div>
    </div>
  </div>
</body>
</html>
