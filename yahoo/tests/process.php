<?php
$latitude = 1;
$longitude = 2;
if (isset($_POST['latitude']))
{
        $longitude = $_POST['longitude'];
        $latitude = $_POST['latitude'];
        $cmd = "/usr/bin/python /home/pallav/Documents/Yahoo/What-N-Where/copy_tweet.py " . $latitude . " " . $longitude . "";
        $output = shell_exec("nohup $cmd 1>/dev/null 2> /dev/null & echo $!");
        echo $output;
}
//$output = shell_exec('/usr/bin/python /home/pallav/Documents/Yahoo/What-N-Where/1.py > /home/pallav/Documents/Yahoo/What-N-Where/1.json');
?>

