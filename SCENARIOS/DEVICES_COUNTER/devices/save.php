<?php 

    $arr_data[] = array(); // create empty array

    $myFile = "devices.json";
    $string = file_get_contents($myFile);
    $json_a = json_decode($string, true);

    $known_devices = $json_a['known'];
    $unknown_devices = $json_a['unknown'];
    $connected_devices = $json_a['connected'];

    try
    {
        //Get form data
        $formdata = array(
            'mac'=> $_GET['mac'],
            'owner'=> $_GET['owner'],
            'description'=> $_GET['description']
        );

        $known_devices[$formdata['mac']] = $formdata;

        foreach($unknown_devices as $key => $device)
        {
            if($_GET['mac'] == $device)
            {
                array_splice($unknown_devices, $key, 1);
            }
        }

        $json_a['known'] = $known_devices;
        $json_a['unknown'] = $unknown_devices;
        $json_a['connected'] = $connected_devices;

        $jsondata = json_encode($json_a, JSON_PRETTY_PRINT);

        //write json data into data.json file
        if(file_put_contents('devices.json', $jsondata)) 
        {
            echo 'Data successfully saved';
            header("Location: /devices");
            
        }
        else 
            echo "error";
    }
    catch (Exception $e) {
        echo 'Caught exception: ',  $e->getMessage(), "\n";
    }

?>
