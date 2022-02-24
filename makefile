run:
	sudo apt-get update
	sudo apt-get install python3
	echo Y

	sudo apt-get install python3-pip
	echo Y
	sudo pip install setuptools
	echo Y
	sudo pip install pyinstaller
	echo Y

	sudo pyinstaller --onefile --noupx while.py
	sudo cp -r ./dist/while while

	sudo rm -rfv build
	sudo rm -rfv dist
	sudo rm -rfv while.spec 

	sudo chmod -R 777 ~/Documents/
	sudo cd /home/snzi/Documents/hw2-shknight/
	