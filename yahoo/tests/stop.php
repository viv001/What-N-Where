<?php
if (isset($_POST['pid']))
{
        //echo $_POST['pid'];
        posix_kill($_POST['pid'], SIGINT);

}
//$output = shell_exec('/usr/bin/python /home/pallav/Documents/Yahoo/What-N-Where/1.py > /home/pallav/Documents/Yahoo/What-N-Where/1.json');
?>

