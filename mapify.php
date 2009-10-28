

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
	<head>
		<title>Subterranean mapper</title>
		<style type="text/css" rel="stylesheet">
			textarea {
				width: 100%;
				height: 700px;
			}
			#background {
				width: 1024px;
				height: 768px;
				background: transparent url('./data/backgrounds/foo.png') no-repeat top left;
				overflow: hidden;
			}
			
			#background label {
				float: left;
				background: transparent;
				width: 16px;
				height: 16px;
				display: block;
				overflow: hidden;
				text-align: center;
			}
			
			#background input {
				width: 15px;
				height: 15px;
				opacity: 0;
			}
			
			#background input:hover,#background input:checked {
				opacity:1;
			}
			
			button {
				margin: 10px 0 0 0;
				width: 1024px;
				padding: 10px;
				font-size: 20px;
			}
		</style>
	</head>
	<body>
	<?php
	if(!empty($_POST)) {
		echo '<textarea>';
		$size = 64*48;
		for($i=1;$i<=$size;$i++) {
			if(isset($_POST['f'.$i])) {
				echo'x,';
			}
			else {
				echo '1,';
			}
		}
		echo '</textarea>';	
		die();
	}
	?>
	<form method="post" action="mapify.php">
		<div id="background">
		<?php
		$size = 64*48;
		for($i=1;$i<=$size;$i++) {
			echo '<label for="id="f'.$i.'""><input type="checkbox" id="f'.$i.'" name="f'.$i.'" value="x"></label>';
		}
		?>
		</div>
		<button type="submit">Generate awesome map file</button>
	</form>
	
	</body>
</html>
