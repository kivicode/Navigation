<?php
  $robot_type = intval($_GET["mode"]); // 1-big  2-small 3-set
//  $file = fopen("poss.txt", "w") or die("Unable to open file!");
  if (1 == $robot_type){
    $p = explode("|", file_get_contents('poss.txt', FILE_USE_INCLUDE_PATH))[0];
    $p = explode("[", $p)[1];
    $p = explode("]", $p)[0];
    echo $p;
  }else if(2 == $robot_type){
    $p = explode("|", file_get_contents('poss.txt', FILE_USE_INCLUDE_PATH))[1];
    $p = explode("[", $p)[1];
    $p = explode("]", $p)[0];
    echo $p;
  }else if(3 == $robot_type){
    $pos_1 = $_GET["r1"];
    $pos_2 = $_GET["r2"];
    $file = fopen("poss.txt", "w+") or die("Unable to open file!");
    fwrite($file, "$pos_1|$pos_2");
    echo "Set pos to $pos_1 and $pos_2";
  }
//    fclose($file);

?>