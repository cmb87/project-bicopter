APP_NAME = "drone"
ROS_IMAGE = ""


.PHONY: rosdev/start rosdev/stop

rosdev/start:
	cd ./ros && docker-compose up -d


rosdev/stop:
	cd ./ros && docker-compose down