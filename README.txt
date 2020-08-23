Voting Application

Prerequisites:
	Python3
	Django3
	XAMPP
	mysqlclient

Contents:
	Django project
	MySQL database (in database folder)

Setup:
	Copy the 'votingapplication' folder given in 'database' folder to the following directory. "C:\xampp\mysql\data". Path may vary if you have installed XAMPP elsewhere.
	Check if the port of MySQL matches the port given in 'settings.py'. If not, then change the port in 'settings.py'.
	Start Apache and MySQL in XAMPP
	Run the Djnago project as usual.

Working:
	Already 3 user IDs are created; 'demo', 'john', 'abdul'. Password of all three are 'root'. 'demo' is an administrator account.
	Users can signup/login to app with email ID and password.
	Users can create poll with maximum of 5 option.
	If users have voted once, they are not allowed to vote again.
	Total number of votes can not be greater than 12. If the limit of 12 votes is reached then "Voting is Ended" message is displayed.
	Only logged in users can perform any actions.
	For reference refer screenshots.