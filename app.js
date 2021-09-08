/*
 * @Descripttion: 将美女网站的数据爬取下来并映射为表格
 * @version: 
 * @Author: shaojinxin
 * @Date: 2021-06-22 17:57:51
 * @LastEditors: shaojinxin
 * @LastEditTime: 2021-07-27 15:24:32
 */

// var http = require('http');
var express = require('express');
var cors = require("cors");
// var request = require('request');
var bodyParser = require('body-parser');
// var CronJob = require('cron').CronJob;
// var fs = require("fs");
var Pool = require('pg').Pool;
// var Canvas = require('canvas')
var app = express();
const opencc = require('node-opencc');

app.locals.pretty = true;
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({
    extended: true
}));
app.use(cors());
app.use(function (req, res, next) {
    console.log(`${req.method} request for '${req.url}' - ${JSON.stringify(req.body)}`);
    next();
});

var pool = new Pool({
    user: 'postgres',
    password: 'zjhzmcm2839667',
    host: '127.0.0.1',
    port: 5432,
    database: 'data',
    max: 20, // max number of clients in pool
    idleTimeoutMillis: 1000, // close & remove clients which have been idle > 1 second
});

app.get("/get/randomone", function (req, res) {
    pool.connect(function (err, client, release) {
        if (err) {
            resbac = { "status": 400, "result": err }
            res.json(resbac);
            return console.error('error running connection', err);
        } else {
            var num = Math.random();
            if(num>0.5){
                var query = 'SELECT author,title,paragraphs,"collect",age,length(paragraphs[1]) FROM poetry.shi_brief order by random() limit 1;';
            }else{
                var query = 'SELECT author,rhythmic title,paragraphs,"collect",age,length(paragraphs[1]) FROM poetry.ci where  array_length(paragraphs,1)<9 order by random() limit 1;'
            }
            client.query(query, function (err, result) {
                if (err) {
                    return console.error('error running query', err);
                } else {
                    release();
                    var back={"author": "",
                    "title": "",
                    "paragraphs": [],
                    "collect": false,
                    "age": "",
                    "length": 0};
                    back.collect = result.rows[0].collect;
                    back.age = result.rows[0].age;
                    back.length = result.rows[0].length;
                    back.author = opencc.simplifiedToTraditional(result.rows[0].author);
                    back.title = opencc.simplifiedToTraditional(result.rows[0].title);
                    result.rows[0].paragraphs.forEach(element => {
                        back.paragraphs.push(opencc.simplifiedToTraditional(element))
                    });
                    resbac = { "status": 200, "result": [back] };
                    res.json(resbac);
                    console.log("get random one poetry!");
                }
            });
        }
    });
});


app.get("/test",function(req,res){
    resbac = { "status": 200, "result": opencc.simplifiedToTraditional('雅淡精神，铅黄未洗，犹带残妆。') };
    res.json(resbac);
})
app.listen(3003, '0.0.0.0');
console.log('listening 3003');
