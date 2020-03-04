<?php 

    $arr_data[] = array(); // create empty array

    $myFile = "devices.json";
    $string = file_get_contents($myFile);
    $json_a = json_decode($string, true);

    $known_devices = $json_a['known'];
    $unknown_devices = $json_a['unknown'];
    $connected_devices = $json_a['connected'];

    echo  "<h2>Connected devices: </h2>";

    foreach ($connected_devices as $mac) {
        if(array_key_exists($mac, $known_devices))
        {
            echo "<div><span style='font-weight: bold;'>".$known_devices[$mac]['owner']."</span>: ".$mac."</div>";
        }
        else {
            echo "<div><span style='font-weight: bold;'>Unknown device</span>: ".$mac."</div>";
        }
    }

    echo "<hr>";

    echo  "<h2>Known devices: </h2>";


    foreach ($known_devices as $mac => $device) {
        echo "<h2>".$mac."</h2>";
        echo "<div><span style='font-weight: bold;'>Owner</span>: ".$device['owner']."</div>";
        echo "<div><span style='font-weight: bold;'>Description</span>: ".$device['description']."</div>";

        echo '<form action="delete.php?"'.$mac.'>';
        echo '<input type="hidden" name="mac" value="'.$device['mac'].'"><br>';
        echo '<input type="submit" value="Delete">';
        echo '</form>';
    }

    echo "<hr>";

    echo  "<h2>Unknown devices: </h2>";

    foreach ($unknown_devices as $mac) {
        
        echo '<form action="save.php?"'.$mac.'>';
        echo "<h2>".$mac."</h2>";
        echo '<input type="hidden" name="mac" value="'.$mac.'"><br>';
        echo 'Owner:<br>';
        echo '<input type="text" name="owner"><br>';
        echo 'Description:<br>';
        echo '<input type="text" name="description" ><br><br>';
        echo '<input type="submit" value="Submit">';
        echo '</form>';
    
    }

?>
