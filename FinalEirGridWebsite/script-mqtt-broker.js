//Using Hive broker - dashboard available at http://www.hivemq.com/demos/websocket-client/
//Uses the Paho MQTT JS client library - http://www.eclipse.org/paho/files/jsdoc/index.html to send and receive messages using a web browser
//Example code available at https://www.hivemq.com/blog/mqtt-client-library-encyclopedia-paho-js
 
 
client = new Paho.Client("broker.mqttdashboard.com", 8000, "web_" + parseInt(Math.random() * 100, 10));
client.onConnectionLost = onConnectionLostHandler;
 
var connectOptions = {
    onSuccess: onConnectCallback //other options available to set
};
 
function connectToBroker(){
    client.connect(connectOptions);
}
 
// called when the client connect request is successful
function onConnectCallback() {
  // Once a connection has been made, make a subscription and send a message.
  console.log("connected to MQTT broker");
}

function publishMessage() {
    var messageInput = document.getElementById('message');
    var messageValue = messageInput.value;

    var areaInput = document.getElementById('area');
    var areaValue = areaInput.value;

    console.log("Publish function executing");
    client.publish(areaValue, messageValue, 0, false);
    // client.publish("TUDublin_IoT", messageValue, 0, false);

    areaInput.value = '';
    messageInput.value = '';
  }
 
function disconnectFromBroker(){
    client.disconnect();
    console.log("disconnected");
}
 
function onConnectionLostHandler(responseObject) {
  if (responseObject.errorCode !== 0) {
    console.log("onConnectionLost:"+responseObject.errorMessage);
  }
}


// code for subscribing
var subscribeOptions = {
  qos: 0,  // QoS
  onSuccess: onSubscribeCallback, //other options available to set
timeout : 30,
onFailure : onFailureCallback
};

client.onMessageArrived = onMessageArrivedHandler;
client.onConnectionLost = onConnectionLostHandler;

function subscribeToMessages() {
  // Once a connection has been made, make a subscription and send a message.
  console.log("subscribed to messages from topic TUDublin_IoT ");
  client.subscribe("TUDublin_IoT", subscribeOptions);
}
 
// called when a message arrives
function onMessageArrivedHandler(message) {
  var messageFromBroker = document.getElementById("mqtt-messages");
  var container = document.getElementById("mqtt-message-container");
  var brokerMessage = message.payloadString;
  messageFromBroker.innerHTML += brokerMessage + "<br>";

  // container.style.height = messageFromBroker.clientHeight + "px";
  container.style.height = messageFromBroker.scrollHeight + "px";

  console.log("message from broker: " + message.payloadString + " with QoS: " +message.qos);
}
 
// called when client subscribe request is successful
function onSubscribeCallback() {
  console.log("subscribed");   
}
 
function onFailureCallback() {
  console.log("failed");   
}