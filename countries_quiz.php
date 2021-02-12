<?php session_start() ?>

<!DOCTYPE html>
<html lang="en" dir="ltr">
  <head>
    <meta charset="utf-8">
    <title>Countries Quiz</title>
    <script type="text/javascript">
    function sigihtmawnfjft(){
      document.getElementById("result").innerHTML="Try again";
    }
    </script>
  </head>
  <body>
    <p id="result"></p>

    <?php

    if(!isset($_SESSION["noton"])){
      $_SESSION["candc"] = makeOurPairs();
      $_SESSION["noton"] = false;
    }

    $thisRound = array_rand($_SESSION["candc"],5);
    $thisSecretNum = array_rand($thisRound);
    $thisPair = array(
      $_SESSION["candc"][$thisRound[$thisSecretNum]],
      $thisRound[$thisSecretNum]);

    echo "what is the capital of ".$thisPair[0]."<br>";
    echo "<form>";
    foreach ($thisRound as $value) {
      if ($value==$thisPair[1]) {
        echo "<input type='submit' value='$value'>";
      } else {
        echo "<input type='button' value='$value' onclick='sigihtmawnfjft()'>";
      }
    }
    echo "</form>";

    function makeOurPairs(){
      $curl = curl_init();

      curl_setopt_array($curl, [
      	CURLOPT_URL => "https://ajayakv-rest-countries-v1.p.rapidapi.com/rest/v1/all",
      	CURLOPT_RETURNTRANSFER => true,
      	CURLOPT_FOLLOWLOCATION => true,
      	CURLOPT_ENCODING => "",
      	CURLOPT_MAXREDIRS => 10,
      	CURLOPT_TIMEOUT => 30,
      	CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
      	CURLOPT_CUSTOMREQUEST => "GET",
      	CURLOPT_HTTPHEADER => [
      		"x-rapidapi-host: ajayakv-rest-countries-v1.p.rapidapi.com",
      		"x-rapidapi-key: 5d7e6ede50msh4157653a7e11cc3p1f322ajsn0049ba59a514"
      	],
      ]);

      $response = curl_exec($curl);
      $err = curl_error($curl);

      curl_close($curl);

      if ($err) {
      	die("cURL Error #:" . $err);
      }

      $response = json_decode($response, true);

      $ourPairs = array();

      foreach ($response as $item) {
        if (!($item["capital"]=="")) {
          $ourPairs[$item["capital"]]=$item["name"];
        }
      }
      return $ourPairs;
    }

    ?>
  </body>
</html>
