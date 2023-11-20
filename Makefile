APP_NAME = "drone"
ROS_IMAGE = ""


.PHONY: rosdev/start rosdev/stop rosdev/logs rosdev/exec  construction/pcb  rosdev2/start rosdev2/stop rosdev2/logs rosdev2/exec 

rosdev/start:
	cd ./ros && docker-compose up -d

rosdev/logs:
	docker logs rosnoetic --follow

rosdev/stop:
	cd ./ros && docker-compose down

rosdev/exec:
	docker exec -ti rosnoetic bash


rosdev2/start:
	cd ./ros2 && docker-compose up -d

rosdev2/logs:
	docker logs ros2 --follow

rosdev2/stop:
	cd ./ros2 && docker-compose down

rosdev2/exec:
	docker exec -ti ros2 bash


construction/pcb:
	docker run -ti --rm -e DISPLAY=${DISPLAY} -v /tmp/.X11-unix:/tmp/.X11-unix -v `pwd`/construction/pcb:/home/fritzing/docs jerivas/fritzing