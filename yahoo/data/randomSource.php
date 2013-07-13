<?php

// Generates a random string of length specified 
function generateRandomString($length) {
        $characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
        $characters = str_shuffle($characters);
        return substr($characters, 0, $length);
}


//Generates a random date between the start and end date
function randomDate($start_date, $end_date)
{
        // Convert to timetamps
        $min = strtotime($start_date);
        $max = strtotime($end_date);

        // Generate random number using above bounds
        $val = rand($min, $max);

        // Convert back to desired date format
        return date('Y-m-d H:i:s', $val);
}

function randomSentiment()
{
        $x = rand(1,100);
        if($x%2==0) return "Good";
        else return "Bad";
}

//Generates a randon JSON data array of the size specified
function randomJSON($size_of_array) {
        $arrayJSON = "[";

        for($i=1; $i<=$size_of_array; $i++)
        {
                $newdate = randomDate('2009-12-10','2013-12-10');
                $objectJSON = "{ ".'"latitude":"'.rand(-40,40).'"'.',"longitude":"'.rand(-40,40).'","sentiment":"'.randomSentiment().'","message":"'.generateRandomString(6).'" } ';
                if($i!=$size_of_array)
                        $objectJSON = $objectJSON.",";
                $arrayJSON = $arrayJSON . $objectJSON;

        }
        $arrayJSON = $arrayJSON . " ]";
        return $arrayJSON;


}

// Continuously displays random JSON data array
echo randomJSON(rand(1,4));

?>
