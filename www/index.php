<html>
	<head>
		<meta http-equiv="content-type" content="text/html; charset=UTF-8"/>
		<meta http-equiv="Content-Type" charset="utf-8"/>
		<link rel="stylesheet" href="zarafaadmin.css"/>
		<title>Zarafa Administration</title>
	</head>
	<body>
		<div id="frame-wrapper">
		<div id="frame-header">
  			<div id="header-panel">
    			<div id="header-title1">Zarafa Admin</div>
    			<div id="header-title2">Office of Public Works - Zarafa Administration</b></div>
    			<div id="header-opwlogo"></div>
  			</div>
		</div>
		<table id="frame-table">
			<tr>
 				<td id="table-header">&nbsp;&nbsp;Commands</td>
 				<td id="table-user" align="right">&nbsp;Logged in as <?=strtolower( $_SERVER['PHP_AUTH_USER'] )?>
				&nbsp;<a href="https://logout:logout@<?=$_SERVER['HTTP_HOST']?>/">Logout</a>&nbsp;&nbsp;</td>
			</tr>
			<tr>
				<td id="table-commands">
					<p></p>
					<p>&nbsp;Zarafa Management
					<ul>
						<li><a href="./zarafa-users.php" target="cmdiframe">Zarafa Users</a></li>
						<li><a href="./zarafa-groups.php" target="cmdiframe">Zarafa Groups</a></li>
						<li><a href="./zarafa-mdm.php" target="cmdiframe">Zarafa Devices</a></li>						
						<li><a href="./zarafa-system.php" target="cmdiframe">Zarafa System</a></li>
						<li><a href="./zarafa-session.php" target="cmdiframe">Zarafa Session</a></li>
						<li><a href="./zarafa-license.php" target="cmdiframe">Zarafa License</a></li>
					</ul></p>
					<p>&nbsp;Zarafa Logs
					<ul>
						<li><a href="./zarafa-logins.php" target="cmdiframe">Login Errors</a></li>
						<li><a href="./zarafa-errors.php?log=system" target="cmdiframe">System Log</a></li>
						<li><a href="./zarafa-errors.php?log=mysql" target="cmdiframe">MySQL Log</a></li>
						<li><a href="./zarafa-errors.php?log=z-push" target="cmdiframe">Z-Push Log</a></li>						
						<li><a href="./zarafa-errors.php?log=mail" target="cmdiframe">Mail Log</a></li>						
					</ul></p>					
					<p>&nbsp;Email Addresses
					<ul>
						<li><a href="./zarafa-emails.php" target="cmdiframe">OPW Emails</a></li>					
					</ul></p>
					<p>&nbsp;Mail Stores
					<ul>
						<li><a href="./zarafa-orphans.php" target="cmdiframe">Orphaned Stores</a></li>					
					</ul></p>
				</td>
				<td id="table-results">
					<iframe id="cmdiframe" src="blank.html" name="cmdiframe">Browser not compatible.</iframe>
				</td>
			</tr>
		</table>
		</div>
	</body>
</html>
