# Google Maps API
With the help of the Googlemaps API and Python Flask, I created an interface that would prompt the user to enter the origin and destination of their commute, and output the directions from the origin to the destination as well as the top rated restaurants in the proximity of the destination. 

First, a flask application is opened where the user sees a webpage and is prompted to enter their current location and their destination. Once the user clicks on 
the submit button, the HTML webpage redirects the user to a different URL which outputs an HTML table of the directions to the destination. The current setup 
assumes that the user is walking from the origin to the destination. Under this table, the user also sees a table which provides them with the ten top-rated 
restaurants in a 100 metre radius. The configuration of the API that I have selected outputs all the restaurants that have a rating greater than 3.5 on Google. 
However, the API provides us with the flexibility to tinker with these details. Finally, the user is able to download a CSV file with the tables mentioned above in 
order to allow offline access to the directions and restaurants. 
