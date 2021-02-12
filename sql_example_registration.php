<!DOCTYPE html>
<!DOCTYPE html>
<html lang="en" dir="ltr">
  <head>
    <meta charset="utf-8">
    <title>Register</title>
    <style>
      #myForm
      {
        font-family: Verdana;
        font-size: 16pt;
        margin-top: 12px;
        background-color: yellow;
        border: solid 2px red;
        padding: 15px;
        height: 260px;
        width: 510px;
      }

      #myForm label
      {
        display: block;
        text-align: right;
        padding-right: 15px;
        margin-bottom: 10px;
        width: 175px;
        float: left;
      }

      #myForm input{
        display: block;
        float: left;
        width: 300px;
        margin-bottom: 10px;
        font-size: 16px;
      }

      #myForm button{
        background-color: blue;
        color: white;
        height: 60px;
        width: 500px;
        font-size: 24pt;
        border: 2px solid red;
      }
    </style>
  </head>
  <body>
    <h1>Register</h1>
    <p>Please complete the form to register.</p>
    <?php
      if (!isset($_POST['fn'])){
        getUserDetails();
      } else {
        processUserDetails();
      }
    ?>
  </body>
</html>
<?php

  function doSQL($conn,$sql,$testMsgs){
    $result = $conn->query($sql);
    if ($testMsgs) {
      echo "<br><code>SQL: $sql</code>";
      if ($result) {
        echo "<code> - OK</code>";
      } else {
        echo "<code> - FAIL! ".$conn->error."</code>";
        $result=$conn->error;
      }
    }
    return $result;
  };

  function getUserDetails()
  {
    $fn = $sn = "";
    if (isset($_POST['fn'])){
      $fn = $_POST['fn'];
      $sn = $_POST['sn'];
    }
    $regForm = "
    <div id='myForm'>
      <form method='POST' action='register.php'>
        <label>Forename:</label>
        <input type='text' name='fn' id='fn' value='$fn' required><br>
         <label>Surname:</label>
        <input type='text' name='sn' id='sn' value='$sn' required><br>
         <label>Email:</label>
        <input type='email' name='email' id='email' required><br>
         <label>Confirm Email:</label>
        <input type='email' name='cemail' id='cemail' required><br>
         <label>Password:</label>
        <input type='password' name='pw' required><br>
         <button>Register</button>
      </form>
    </div>
    ";
    echo $regForm;
  }
  function processUserDetails()
  {
    $testMsgs = true; // true = On, false = Off.

    $servername = "localhost";
    $username = "root";
    $password = "root";
    $database = "test";

    //create connection
    $conn = mysqli_connect($servername,$username,$password,$database);

    //check connection
    if (!$conn){
      die("connection failed".mysqli_connect_erorr());
    }
    echo "connected successfully <br>";

    $frmFN = $_POST['fn'];
    $frmSN = $_POST['sn'];
    $frmEM = $_POST['email'];
    $frmPW = $_POST['pw'];
    $frmConfirmEM = $_POST['cemail'];
    if ($frmConfirmEM!==$frmEM) {
      echo "<br>The email addresses you have entered do not match. Try again";
      getUserDetails();
    } else {
      $password = password_hash($frmPW, PASSWORD_DEFAULT);
      $sql = "INSERT INTO user (forename, surname, email,password) VALUES ('$frmFN','$frmSN','$frmEM','$password')";
      $result=doSQL($conn, $sql, $testMsgs);
      if (strpos($result,"Duplicate entry")!==false) {
        echo "<br>The email address you have entered is already in use. Try again";
        getUserDetails();
      }
    }
  }
?>
