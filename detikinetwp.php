<?php
// include 'db_connect.php';
$servername = "localhost";
$username = "bogorsto_root";
$password = "3123661r";
$dbname = "bogorsto_keren";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$url = 'http://apis.detik.com/v1/newsfeed?channelid=105&limit=200';
$data = file_get_contents($url);
$wizards = json_decode($data, true);
//echo "<pre>"; print_r ($wizards);

foreach ($wizards['data']['nonheadline'] as $row) {
  if ($row['type'] == 'detiknews') {
    $urld = 'http://apis.detik.com/v1/detail?id='.$row['id'];
    //echo $urld;die();
    $datad = file_get_contents($urld);
    $detail = json_decode($datad, true);

    $slug = preg_replace('~[^\pL\d]+~u', '-', $detail['data']['title']);

    // transliterate
    $slug = iconv('utf-8', 'us-ascii//TRANSLIT', $slug);

    // remove unwanted characters
    $slug = preg_replace('~[^-\w]+~', '', $slug);

    // trim
    $slug = trim($slug, '-');

    // remove duplicate -
    $slug = preg_replace('~-+~', '-', $slug);

    // lowercase
    $slugid = strtolower($slug);

    //$slug = str_replace(" ","-",$detail['data']['title']);
    //$slug1 = preg_replace('/[^A-Za-z0-9\-]/', '', $slug); // Removes special chars.
    //$slugid = preg_replace('/-+/', '-', $slug1);

    $sql = "SELECT slug FROM posts_post WHERE slug='$slugid'";
    $result = $conn->query($sql);

    $content = html_entity_decode($detail['data']['content']);
    $content = preg_replace("/'/", "\&#39;", $content);
    if($result->num_rows == 0){
      //echo "<pre>"; print_r ($detail);die;
      $title =  preg_replace('/[^a-zA-Z0-9\s]/', '', strip_tags(html_entity_decode($detail['data']['title'])));
      $slug = $slugid;
      $image = $detail['data']['image_cover'][0]['name'];
      $content  = $content;
      $updated  = $detail['data']['date_published'];
      $timestamp  = $detail['data']['date_published'];
      $user_id  = $detail['data']['id_type'];
      $draft  = $detail['data']['flaghoax'];
      $publish  = $detail['data']['date_published'];
      $id_kategori_id  = $detail['data']['id_type'];
      $be_read  = $detail['data']['flaghoax'];

      $sql = "INSERT INTO posts_post (title, slug, image,content,updated,timestamp,user_id,draft,publish,id_kategori_id,be_read) VALUES ('$title', '$slug', '$image','$content','$updated','$timestamp','$user_id','$draft','$publish','$id_kategori_id','$be_read')";
        if($conn->query($sql) === true){
            echo "Records inserted successfully."; echo $title;echo "<br>";
        } else{
            echo "ERROR: Could not able to execute"; echo $title;echo $conn->error;
        }
    }
  }
}
//close connection
mysqli_close($conn);
