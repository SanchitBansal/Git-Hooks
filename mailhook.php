<?php

	$stringData = file_get_contents('php://input');
	
    if($stringData == "")
    {
        include('404.html');
        exit();
    }

    $arr = json_decode($stringData, true);

    $to = $_GET['mailto'];
    echo "To: " . $to . "<br><br>";

    $subject = $arr['user_name'] . " pushed to Repository: " . $arr['repository']['name'];
    echo "Subject: " . $subject;

    $commit_count = $arr['total_commits_count'];

    $body = "Repository: <a href='" . $arr['repository']['homepage'] . "'>" . $arr['repository']['name'] . "</a>"; 
    $body .= "\nTotal Commits in push: " . $commit_count;

    for ($i=0; $i < count($arr['commits']); $i++) 
    { 
    	$body .= "\n\n<b>Commit " . ($i + 1) . "</b>";
    	$body .= "\nMessage: " . $arr['commits'][$i]['message'];
    	$body .= "\nTime: " . $arr['commits'][$i]['timestamp'];
    	$body .= "\nLog: " . $arr['commits'][$i]['url'];
    	$body .= "\nAuthor: <a href='mailto:" . $arr['commits'][$i]['author']['email'] . "'>" . $arr['commits'][$i]['author']['name'] . "</a>";
    }

    echo "<br><br>Body: " . str_replace("\n", "<br>", $body);

    $header  = "MIME-V+ersion: 1.0\r\n";
 	$header .= "Content-type: text/html; charset: utf8\r\n";

 	mail($to, $subject, str_replace("\n", "<br>", $body), $header);

?>
