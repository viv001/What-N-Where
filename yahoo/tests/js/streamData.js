// This script runs callback function and receives data via streams of JSON

var xmlHttpData;//Receive HTTP service response from the URL
var iconGreen = "../images/green.gif";
var tableHTML = "<thead><tr><th>Latitude</th><th>Longitude</th><th>Sentiment</th><th>Message</th></tr></thead>";
var dataText;//Text form of response
var start=0;//Start/Stop streaming
var rows="";
var infowindow = new Array();
var num_marker = 0;
var max_radius = 500000;
var numDeltas = 1000;
var curDeltas = new Array();
var curCircle = 0;
var Circles = new Array(); 
var CircleRadius = new Array(); 
var color = new Array();
var preText = "";

function change_radius(circle)
{
        if(CircleRadius[circle] < max_radius)
        {
                CircleRadius[circle] += 4000;
                Circles[circle].setRadius(CircleRadius[circle]);
                //circle.setMap(mymap);
        }
        if(curDeltas[circle]!=numDeltas)
        {
                curDeltas[circle]++;
                setTimeout(function(){
                change_radius(circle);},10);
        }
        return;
}

// Function called on the load of 
function getData() 
{
        if(start==1)
        {
                xmlHttpData=GetxmlHttpDataObject(); 
                if (xmlHttpData==null) 
                { 
                        alert ("Your browser does not support AJAX!"); 
                        return; 
                }
        
                // Change the url to specify the streaming data input
                var url="http://localhost/yahoo/data/tweets.json";

                //whenever onreadystatechange is triggered, callback function is called
                xmlHttpData.onreadystatechange=stateChanged;

                // Specifying the URL to get the response
                xmlHttpData.open("GET",url,true); 
                xmlHttpData.send(null); 
        }
}

// This is the callback function
function stateChanged() 
{ 
        //xmlHTTPdata.readyState==4: request finished and response is ready
        //xmlHttpData.status=200: "OK"
        if (xmlHttpData.readyState==4 && xmlHttpData.status==200) 
        {
                $(document).ready(function() { 
                        // Note : the data must be an array of JSON objects
                        var dataText = xmlHttpData.responseText;
                        if(dataText!=preText)
                        {

                        //parsing the JSON input
                        dataJSON = JSON.parse(dataText);
                        

                        
                        // Adding the data into the table HTML
                        for (var i = 0; i < dataJSON.length; i++) {
                                //appendString = "<tr><td>"+dataJSON[i].data.latitude+"</td><td>"+dataJSON[i].data.longitude+"</td><td>"+dataJSON[i].data.sentiment+"</td><td>"+dataJSON[i].data.message+"</td></tr>";
                                //rows += appendString;

                                //add markers
                                var myLatlng = new google.maps.LatLng(dataJSON[i].data.latitude,dataJSON[i].data.longitude);
                                /*
                                var marker = new google.maps.Marker({
                                        position: myLatlng,
                                        //icon: iconGreen,
                                        title: dataJSON[i].message,
                                        map: mymap,
                                        animation: google.maps.Animation.DROP
                                });
                                marker.info = new google.maps.InfoWindow({
                                        content: dataJSON[i].message
                                });

                                google.maps.event.addListener(marker, 'click', function() {
                                marker.info.open(mymap, marker);
                                });
                                */
                                //mymap.setCenter(myLatlng);
                                curCircle += 1;
                                color[curCircle] = "#FF0000";
                                if(dataJSON[i].data.sentiment == "positive") {
                                        color[curCircle] = "#008000";
                                }
                                curDeltas[curCircle] = 0;
                                CircleRadius[curCircle] = 100000;
                                var circleOptions = {
                                        strokeColor: color[curCircle],
                                        strokeOpacity: 0.8,
                                        strokeWeight: 2,
                                        fillColor: color[curCircle],
                                        fillOpacity: 0.35,
                                        map: mymap,
                                        center: myLatlng,
                                        radius: CircleRadius[curCircle]
                                };
                                Circles[curCircle] = new google.maps.Circle(circleOptions);
                                //var worker = new Worker(change_radius(curCircle));
                                change_radius(curCircle);
                                //if(curCircle > 1)
                                //        Circles[curCircle-1].setRadius(1);
                                //curCircle.setMap(null);

                                //if( !current_bounds.contains( marker_pos ) ){

                                        //var new_bounds = current_bounds.extend( marker_pos );
                                        //mymap.fitBounds( new_bounds );
                                //}
                        }
                        for( j = 1; j < curCircle - dataJSON.length + 2; j++ )
                        {
                                if(j > 1)
                                        Circles[j-1].setRadius(0);
                        }
                        document.getElementById('status').innerHTML = tableHTML+"<tbody>"+rows+"</tbody>";
                        }
                        preText = dataText;



                        // Display the JSON stream in the view
                         document.getElementById("dataResponse").innerHTML=xmlHttpData.responseText; 

                        //-------------------------------------------------

                });

                // Fire getData function here to continuously receive data, i.e "stream data" at interval of 2 seconds
                setTimeout(getData, 2000);
        } 
} 


// Different browsers have different ways of 
// receiving the xmlHTTPdata
function GetxmlHttpDataObject() 
{ 
        var xmlHttpData=null; 
        try 
        { 
                // Firefox, Opera 8.0+, Safari 
                xmlHttpData=new XMLHttpRequest(); 
        } 
        catch (e) 
        { 
                // Internet Explorer 
                try 
                {        
                        xmlHttpData=new ActiveXObject("Msxml2.XMLHTTP"); 
                } 
                catch (e) 
                { 
                        xmlHttpData=new ActiveXObject("Microsoft.XMLHTTP"); 
                }        
        } 
        return xmlHttpData; 
}

// this is function is basically to stop or start the receiving streaming data.

var PID;

function StartStopStreaming()
{
        if(start==0)
        {
                document.getElementById("latitude").value = mylocation.getPosition().lat();
                document.getElementById("longitude").value = mylocation.getPosition().lng();
                $.ajax({
                        type: "POST",
                        url: "http://localhost/yahoo/tests/process.php",
                        data: { 'latitude': mylocation.getPosition().lat(), 'longitude': mylocation.getPosition().lng()   },
                        cache: false,
                        success: function(data)
                        {
                                PID = data;
                                return false;
                                //mymap.setCenter(mylocation.getPosition());
                                //document.write(data);
                        }
                });
                start=1;
                document.getElementById('startstop').firstChild.data = "Stop Streaming";
                getData();
        }
        else 
        {
                $.ajax({
                        type: "POST",
                        url: "http://localhost/yahoo/tests/stop.php",
                        data: { 'pid': PID   },
                        cache: false,
                        success: function(data)
                        {
                                alert(data);
                                return false;
                                //mymap.setCenter(mylocation.getPosition());
                                //document.write(data);
                        }
                });
                document.getElementById('startstop').firstChild.data = "Start Streaming";
                start=0;
        }
}
