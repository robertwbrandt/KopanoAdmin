<?php
/*
 *    Zarafa Out of Office form
 *
 *    Created by: Bob Brandt (http://brandt.ie)
 *    Created on: 2016-04-23
 *
 *                             GNU GENERAL PUBLIC LICENSE
 *                                Version 2, June 1991
 *    -------------------------------------------------------------------------
 *    Copyright (C) 2013 Bob Brandt
 *
 *    This program is free software; you can redistribute it and/or modify it
 *    under the terms of the GNU General Public License as published by the
 *    Free Software Foundation; either version 2 of the License, or (at your
 *    option) any later version.
 *
 *    This program is distributed in the hope that it will be useful, but
 *    WITHOUT ANY WARRANTY; without even the implied warranty of
 *    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 *    General Public License for more details.
 *
 *    You should have received a copy of the GNU General Public License along
 *    with this program; if not, write to the Free Software Foundation, Inc.,
 *    59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
 */

// Turn off all error reporting
//error_reporting(0);
// Report all PHP errors
error_reporting(-1);
header("Expires: Tue, 01 Jan 2000 00:00:00 GMT");
header("Last-Modified: " . gmdate("D, d M Y H:i:s") . " GMT");
header("Cache-Control: no-store, no-cache, must-revalidate, max-age=0");
header("Cache-Control: post-check=0, pre-check=0", false);
header("Pragma: no-cache");
// The following is needed to display loading screen using Progressive Rendering
ob_start(); // not needed if output_buffering is on in php.ini
ob_implicit_flush(); // implicitly calls flush() after every ob_flush()
$buffer = ini_get('output_buffering'); // retrive the buffer size from the php.ini file
if (!is_numeric($buffer)) $buffer = 8192;

$username = "";
if (isset($_GET['username']))    $username = $_GET['username'];
if (isset($_POST['username']))   $username = $_POST['username'];

$fullname = "";
if (isset($_GET['fullname']))    $fullname = $_GET['fullname'];
if (isset($_POST['fullname']))   $fullname = $_POST['fullname'];

$email = "";
if (isset($_GET['email']))    $email = $_GET['email'];
if (isset($_POST['email']))   $email = $_POST['email'];

?>
<html><head>
	<meta http-equiv="content-type" content="text/html; charset=UTF-8">
	<meta http-equiv="Content-Type" charset="utf-8">
	<link rel="stylesheet" href="zarafaadmin.css">

	<!-- https://jqueryui.com/datepicker/ -->
	<link rel="stylesheet" href="jquery-ui.css">
	<script src="jquery-1.10.2.js"></script>
	<script src="jquery-ui.js"></script>
	<script>
		$(function() {
		  $( "#ooo-from" ).datepicker({ dateFormat: 'dd-mm-yy' });
		  $( "#ooo-until" ).datepicker({ dateFormat: 'dd-mm-yy' });
		});
		$(document).keydown(function (e) {
		    if(e.keyCode==27){
		        gotoRefer();
		    }
		});
		function setMode() {
		    var mode = document.getElementById("ooo-mode").value;
		    if (mode == 1) {
					document.getElementById("ooo-from").disabled = false;
					document.getElementById("ooo-until").disabled = false;
					document.getElementById("ooo-subject").disabled = false;
					document.getElementById("ooo-message").disabled = false;
					document.getElementById("ooo-from").style.backgroundColor = "white";
					document.getElementById("ooo-until").style.backgroundColor = "white";
					document.getElementById("ooo-subject").style.backgroundColor = "white";
					document.getElementById("ooo-message").style.backgroundColor = "white";
					document.getElementById("ooo-mode").style.color = "green";

		    } else {
					document.getElementById("ooo-from").disabled = true;
					document.getElementById("ooo-until").disabled = true;
					document.getElementById("ooo-subject").disabled = true;
					document.getElementById("ooo-message").disabled = true;
					document.getElementById("ooo-from").style.backgroundColor = "lightgrey";
					document.getElementById("ooo-until").style.backgroundColor = "lightgrey";
					document.getElementById("ooo-subject").style.backgroundColor = "lightgrey";
					document.getElementById("ooo-message").style.backgroundColor = "lightgrey";
					document.getElementById("ooo-subject").value = "Out of Office";
					document.getElementById("ooo-message").value = "";
					document.getElementById("ooo-mode").style.color = "red";			
		    }
		}

		function gotoRefer() {
			window.location.href = "<?=$_SERVER['HTTP_REFERER']?>";
		}
	</script>
	<title>Zarafa (Un)Set Out of Office</title>
</head>
<body onload="setMode()">
<form action="./zarafa-action.php" method="get">
<input type="hidden" name="action" value="ooo"/>
<input type="hidden" name="username" value="<?=$username?>"/>
<input type="hidden" name="fullname" value="<?=$fullname?>"/>
<input type="hidden" name="email" value="<?=$email?>"/>
<input type="hidden" name="referer" value="<?=$_SERVER['HTTP_REFERER']?>"/>
<p class="ooo-title">Set/Unset Out-of-Office for <?=$fullname?> (<?=$email?>)</p>
<table id="ooo-table" align="center">
	<tr>
		<td>&nbsp;</td>	
		<td>
			<select name="mode" id="ooo-mode" style="width: 100%;" onchange="setMode()">
			  <option value="0" selected="selected">Disable Out-of-Office</option>
			  <option value="1"> Enable Out-of-Office</option>
			</select>
		</td>
		<td align="right">From:</td>
		<td><input id="ooo-from" name="from"/></td>
		<td align="right">Until:</td>
		<td><input id="ooo-until" name="until"/></td>
	</tr>
	<tr>
		<td>&nbsp;</td>	
		<td align="right" colspan="2">Subject:</td>
		<td colspan="3"><input type="text" name="subject" id="ooo-subject" value="Out of Office" style="width: 100%;"/></td>
	</tr>
	<tr>
		<td>&nbsp;</td>	
		<td colspan="5" align="left">AutoReply only once to each sender with the following text:</td>
	</tr>
	<tr>
		<td>&nbsp;</td>	
		<td colspan="5">
			<textarea rows="4" cols="50" name="message" id="ooo-message" style="width: 100%; resize: none;"></textarea>
		</td>
	</tr>
	<tr>
		<td>&nbsp;</td>	
		<td align="left"><input id="ooo-cancel" type="button" value="Cancel" onclick="gotoRefer()"/></td>
		<td colspan="3"></td>
		<td align="right"><input id="ooo-submit" type="submit" value="Submit"/></td>		
	</tr>	
</table>
</form>


</body></html>