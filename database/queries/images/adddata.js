'use strict';
var mysql = require('mysql');
require('dotenv').load();

var connection = mysql.createConnection({
  host     : process.env.HOST,
  user     : process.env.USER,
  password : process.env.PASSWORD,
  port     : process.env.PORT,
  database : "ImageDB"
});

connection.connect(function(err) {
  if (err) {
    console.error('Database connection failed: ' + err.stack);
	connection.end()
    return;
  }

  console.log('Connected to database.');
  connection.query("INSERT INTO images (PostId, ImageLink, ImageName) VALUES ?", [[[1, "HI I MINDY", "POTATO"], [2, "HI I MINDU", "POTATOS"]]]);
  connection.end()
});
