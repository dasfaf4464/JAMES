// 요약된 질문 받아오는 웹소켓 연결

const express = require('express');
const app = express();

app.use("/", function (req, res) {
  req.sendFile(__dirname + '/session.html');
});

app.listen(5500);

const WebSocket = require('ws');

const socket = new WebSocket.Server({
  port: 5501
});

socket.on('connection', (ws, req)=> {

  ws.on('message', (msg)=>{
    console.log('원문 : ' +msg)
    ws.send();
  })

})