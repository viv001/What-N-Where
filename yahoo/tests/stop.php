<?php
if (isset($_POST['pid']))
{
        //echo $_POST['pid'];
        posix_kill($_POST['pid'], SIGINT);
}
$cmd1 = "/usr/bin/python /home/pallav/Documents/Yahoo/What-N-Where/Tag_Cloud.py"; 
$output = shell_exec($cmd1);
echo $output;
//$output = shell_exec('/usr/bin/python /home/pallav/Documents/Yahoo/What-N-Where/1.py > /home/pallav/Documents/Yahoo/What-N-Where/1.json');
?>

