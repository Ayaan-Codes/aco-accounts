<?php
session_start();
if(isset($_SESSION["loggedin"]) && $_SESSION["loggedin"] === false){
    header("location: welcome.php");
    exit;
}

?>
<!DOCTYPE html>
<html>
  <body>
  <h1>welcome to app</h1>
    <h2><?php echo $_SESSION["usr"]; ?></h2>
  </body>
</html>
