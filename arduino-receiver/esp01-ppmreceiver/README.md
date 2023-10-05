# Websocket based drone system



## Demo with FD411 Flightcontroller and ESP8266


## SocketIO Versions

	Python:
		Flask==1.1.2
		Flask-Cors==3.0.9
		gevent==20.6.2
		gevent-websocket==0.10.1
		python-engineio==3.13.2
		python-socketio==4.6.1
		Flask-SocketIO==4.3.1
    
	Arduino:
		SocketIOClient==0.3.0 (Vincent Wyszynski)
		WebSockets==2.3.1 (Markus Sattler)

	Angular:
		npm i --save socket.io-client@2.3.1
	Node:
		socket.io": {"version": "2.3.0"}
		engine.io  "version": "3.4.2",
		engine.io-client  3.4.4

## Connection Flightcontroller - Receiver

### PPM FD411 Flightcontroller Betaflight
		FD411s => ESP01
		3.3V => Pin 8 
		GND => Pin1
		RX2 => Pin2 (GPIO1)



## Connections for SBUS
https://github.com/bolderflight/SBUS
