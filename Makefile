APP_NAME = "drone"
ROS_IMAGE = ""


.PHONY: rosdev/start rosdev/stop rosdev/logs construction/pcb rosdev/exec

rosdev/start:
	cd ./ros && docker-compose up -d

rosdev/logs:
	docker logs rosnoetic --follow

rosdev/stop:
	cd ./ros && docker-compose down

rosdev/exec:
	docker exec -ti rosnoetic bash

construction/pcb:
	docker run -ti --rm -e DISPLAY=${DISPLAY} -v /tmp/.X11-unix:/tmp/.X11-unix -v `pwd`/construction/pcb:/home/fritzing/docs jerivas/fritzing