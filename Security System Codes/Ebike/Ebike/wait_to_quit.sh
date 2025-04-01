#wait until q is entered or program ends through gui
#run using "bash wait_to_quit.sh"
echo 1 > "Program_Files/run_prog.txt" 
sleep 10
echo "Press 'q' to end programs!"

while [ `cat "Program_Files/run_prog.txt"` = '1' ]
do
	#quit program if q is entered
	read -t 0.1 -N 1 usr_input
	if [ $usr_input ]
	then
		echo "" #new line
		if [ $usr_input = 'q' ]
		then
			echo 0 > "Program_Files/run_prog.txt"
			echo "Ending programs..."
		else
			echo "Press 'q' to end programs!"
		fi
	fi
done

sleep 2
echo "Programs Ended!"

#give an option to keep the window open
echo "Window will close in 10 seconds."
echo "Press 'h' to keep the window on; press any other button to quit now."
read -t 10 -N 1 usr_input
if [ $usr_input -a $usr_input = 'h' ]
then
	while [ $usr_input != 'c' ]
	do
		echo ""
		echo "Press 'c' to close the window."
		read -N 1 usr_input
	done
fi
echo""
