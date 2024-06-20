const http=require('http');
const hostname='0.0.0.0';
const port =3000;
const fs=require('fs');
//連接mysql
var url=require('url');
var mysql = require('mysql');
const querystring = require('querystring');
const { connect } = require('http2');
var connection = mysql.createConnection({
  host     : 'localhost',
  user     : 'root',
  password : 'password',
  database : 'AIOT'
});
function stdSQLStr(input){
  var str=input+"";
  return "'"+str+"'";
}
function stdSQLVal(input0,input1,input2,input3){
  var result;
  result="VALUES("+input0;
  if(input1!=undefined){
    result=result+","+input1;
  }
  if(input2!=undefined){
    result=result+","+input2;
  }
  if(input3!=undefined){
    result=result+","+input3;
  }
  return result+");";
}
function sqlQue(link,command,result){
  link.query(command,function(error, results, fields){
    if (error){
      throw error;
    }
    else{
      result=results;
      console.log("r");
      console.log(results);
    }
  });
}
function merchanInForm(merchanid,remain){
  var str="    <div>\n"+
  '      <label for="product1">id:</label>\n'+
  '      <input type="text" id="product1" name="product1" value="'+merchanid+'" readonly>\n'+
  '      <label for="stock1">remain:</label>\n'+
  '      <input type="number" id="stock1" name="stock1" value="'+remain+'" readonly>\n'+
  '      <label for="order1">add:</label>\n'+
  '      <input type="number" id="order1" name="order1" required>\n'+
 '    </div>'
 return str;
}
function carInForm(carid,status){
  str='<div\n>'+
  '<label for="vehicle1">車輛A:</label>\n'+
  '<input type="text" id="vehicle1" name="vehicle1" value="'+carid+'" readonly>\n'+
  '<label for="status1">車輛狀態:</label>\n'+
  '<input type="text" id="status1" name="status1" value="'+status+'" readonly>\n'+
'</div>'
return str;
}
var formSegment=[`
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Order Form</title>
</head>
<body>
  <h1>Order Form</h1>
  <form action="/submit" method="POST">
    <label for="taskID">taskid:</label>
      <input type="text" id="taskid" name="taskid">
`,
  "<hr>",
  `
    <button type="submit">Submit</button>
  </form>
  <script>
    document.getElementById('productForm').onsubmit = function(event) {
        event.preventDefault();

        const products = document.querySelectorAll('.product');
        const formData = [];

        products.forEach(product => {
            const productData = {
                product_id: product.querySelector('[name="product_id"]').value,
                stock: product.querySelector('[name="stock"]').value,
                order: product.querySelector('[name="order"]').value
            };
            formData.push(productData);
         });

        fetch('/submit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
         })
        .then(response => response.text())
        .then(data => alert(data))
        .catch(error => console.error('Error:', error));
    };
  </script>
</body>
</html>
`
]
function merchanSegment(link,str){
  var com="select * from id2remain";
  link.query(com,function(err,results,fields){
    if(err){
      throw err;
    }
    results.forEach(function(row){
      str+=merchanInForm(row['id'],toString(row['remain']));
    });
  });
}
function carSegment(link,str){
  var com="select * from id2remain";
  link.query(com,function(err,results,fields){
    if(err){
      throw err;
    }
    results.forEach(function(row){
      str+=merchanInForm(row['id'],row['remain']);
    });
  });
}
connection.connect();
console.log("123,456".split("."));
const server=http.createServer((req,res)=>{
  res.statusCode=200;
  var params = url.parse(req.url, true).query;
  if (req.method === 'GET' && req.url === '/') {
    var MS=formSegment[0];
    var com="select * from id2remain";
    connection.query(com,function(error2, results, fields){
      if (error2){
        throw error2;
      }
      results.forEach(function(row){
        MS+=merchanInForm(row['id'],row['remain'].toString());
        if(row==results.at(-1)){
          MS+=formSegment[2];
          console.log(MS);
          res.end(MS);
        }
      });
    });
  }
  else if (req.method === 'POST' && req.url === '/submit') {
    let body = '';
    req.on('data', chunk => {
      body += chunk.toString(); // 将数据块添加到请求体中
    });
    var tupData="";
    req.on('end', () => {
      console.log('Received body:', body);
      const parsedBody = querystring.parse(body);
      const taskid=parsedBody.taskid;
      const products = [];
      const productIds = Array.isArray(parsedBody.product1) ? parsedBody.product1 : [parsedBody.product1];
      const stocks = Array.isArray(parsedBody.stock1) ? parsedBody.stock1 : [parsedBody.stock1];
      const orders = Array.isArray(parsedBody.order1) ? parsedBody.order1 : [parsedBody.order1];

      for (let i = 0; i < productIds.length; i++) {
          if(i!=0){
            tupData+=";";
          }
          tupData=tupData+productIds[i].toString()+","+orders[i].toString();
          products.push({
              product_id: productIds[i],
              stock: stocks[i],
              order: orders[i]
           });
       }
       http.get('http://127.0.0.1:3000?command=addTask&department=0&taskID='+taskid+'&tup='+tupData, (getRes) => {
        let getResponseData = '';
        getRes.on('data', chunk => {
            getResponseData += chunk;
        });
        getRes.on('end', () => {
            console.log('GET request response:', getResponseData);
        });
        }).on('error', (e) => {
          console.error(`Got error: ${e.message}`);
        });
       res.writeHead(200, { 'Content-Type': 'text/plain' });
       console.log(products[0].order);
       console.log(tupData);
       res.end(`Received Data:\n${JSON.stringify(products, null, 2)}`);
       
    });
  }
  else {
    switch (params.command){
      //手動加入商品
      case "form":
        res.render("form");
        break;
      case "addMerchan":
        console.log(params);
        var com="INSERT INTO id2name "+stdSQLVal(stdSQLStr(params.id),stdSQLStr(params.name));
        //connection.connect()
        connection.query(com, function (error, results, fields){
          if (error){
            throw error;
          } 
          console.log("added");
          res.end("added");
          console.log("quit");
          //connection.end();
          });
        
        break;
      case "listMerchan":
        //手動查商品庫存
        var com="select * from id2name;";
        //connection.connect()
        console.log("connected");
        var queued=0;
        connection.query(com, function (error, results, fields){
          queued=1;
          if (error){
            throw error;
          }
          console.log(results);
          res.end(results[0]['name']);
          //connection.end();
          });
        break;
      case "addTask":
        //新增一筆task 手動或送貨小車
        //params:taskID,department,tup(用分號連接的2entry無括號tuple 例如"1,2;3,4"代表1號商品*2+3號商品*4)
        //會把tup拆解放進未完成task
        //http:127.0.0.1:3000?command=addTask&taskID=1&department=1&tup=1,2;3,4
        var tup=params.tup.split(";");
        var taskID=params.taskID;
        var department=params.department
        var gcom="insert into department2taskid "+stdSQLVal(stdSQLStr(department),stdSQLStr(taskID));
        sqlQue(connection,gcom);
        console.log(tup);
        console.log(tup[0]);
        console.log(tup[1]);
        tup.forEach(i => {
          console.log("this is i");
          console.log(i);
          var merchanID=i.split(",")[0];
          var quantity=i.split(",")[1];
          var com="insert into taskSingleRow "+stdSQLVal(stdSQLStr(taskID),stdSQLStr(merchanID),quantity,"0");
          sqlQue(connection,com);
          console.log("added");
          console.log(merchanID+","+quantity);
        });
        res.end("success");
        break;
      case "startTransferring":
        //理貨小車從貨架上取下某些商品
        //多台車要+carid
        var taskID=params.taskID;
        var quantity=params.quantity;
        var merchanID=params.merchanID;
        var com="insert into `merchantransporting` "+stdSQLVal(stdSQLStr(merchanID), quantity);
        sqlQue(connection,com);
        var com2="SELECT * FROM `tasktransporting` WHERE `taskid`="+stdSQLStr(taskID)+" and `merchanid`="+stdSQLStr(merchanID)+";";
        console.log(com2);
        connection.query(com2, function (err, results, fields){
          if (err){
            //throw err;
          }
          //console.log("--");
          //return results;
          if(results.length==0){
            var com3="select * from `tasksinglerow` where `taskid`="+stdSQLStr(taskID)+" and `merchanid`="+stdSQLStr(merchanID);
            connection.query(com3, function (err, data, fields){
              if (err){
                throw err;
              }
              console.log(data);
              var com4="insert into `tasktransporting` "+stdSQLVal(stdSQLStr(taskID),stdSQLStr(merchanID),data[0]['quantity']);
              sqlQue(connection,com4);
              var com5="update `tasksinglerow` set `executed`=1 where `taskid`="+stdSQLStr(taskID);
              sqlQue(connection,com5);
              res.end("successfully record a task as transporting");
            });
          }
          else{
            console.log("find");
            console.log(results[0]);
            res.end("successfully found existed task");
          }
        });
        
        
        
        break;
      case "transferArrive":
        //理貨小車抵達交貨地點
        var carid=params.carID;
        var com5="update `carstatus` set `status`='idle'";
        // where `carid`="+stdSQLStr(carid);
        sqlQue(connection,com5);
        var com="select * from `merchantransporting`";
        connection.query(com, function (err, cargos, fields){
          if(err){
            throw err;
          }
          var breaker0=0;
          cargos.forEach(function(i){
            console.log(i);
            var cargoid=i['merchan'];
            var com2="select * from `tasktransporting` where `merchanid`="+stdSQLStr(cargoid);
            connection.query(com2, function (err1, executing, fields){
              if (err1){
                throw err1;
              }
              var breaker1=0;
              console.log(executing);
              executing.forEach(function(task){
                a=parseInt(i['quantity']);
                b=parseInt(task['quantity']);
                console.log(task);
                if(breaker1==1){
                  return;
                }
                if(task['quantity']>i['quantity']){
                  console.log("accomodate");
                  var com3="update `tasktransporting` set `quantity`="+(b-a)+" where `taskid`="+stdSQLStr(task['taskid'])+" and `merchanid`="+stdSQLStr(task['merchanid']);
                  var com4="delete from `merchantransporting` where `merchan`="+stdSQLStr(task['merchanid']);
                  sqlQue(connection,com4);
                  console.log(com3);
                  console.log(com4);
                  sqlQue(connection,com3);
                  sqlQue(connection,com4);
                  
                  breaker1=1;
                  var com5="update `tasksinglerow` set `executed`=0 where `taskid`="+task['taskid']
                  if(i==cargos.at(-1)){
                    res.end("success");
                  }
                }
                else{
                  console.log("out"); 
                  var com3="delete from `tasktransporting` where `taskid`="+stdSQLStr(task['taskid'])+" and `merchanid`="+stdSQLStr(task['merchanid']);
                  var com4="update `tasksinglerow` set `executed`=2 where taskid="+stdSQLStr(task['taskid'])+"and `merchanid`="+stdSQLStr(task['merchanid']);
                  var com5="update `merchantransporting` set quantity= "+(a-b)+" where `merchan`="+stdSQLStr(task['merchanid']);
                  console.log(com3);
                  console.log(com4);
                  console.log(com5);
                  sqlQue(connection,com3);
                  sqlQue(connection,com4);
                  sqlQue(connection,com5);
                  var com6="delete from `merchantransporting` where `merchan`="+stdSQLStr(task['merchanid']);
                    sqlQue(connection,com6);
                    breaker1=1;
                  i['quantity']-=task['quantity'];
                  console.log('quantity');
                  console.log(i['quantity']);
                  if(i==cargos.at(-1)){
                    res.end("success");
                  }
                }
              });
            });
          });
          
        });  
        
        break;
      case "takeTask":
        //讓一個閒置的小車取得task
        var com="select * from `carstatus` where `status`='idle'";
        connection.query(com,function(err,data,fields){

          if(err){
            throw err;
          }
          var resStr="";
          data.forEach(function(car){
            var carid=car['carid'];
            console.log(car);
            var carstatus=car['status'];
            var accomodate=car['accomodate'];
            var cartype=car['cartype'];
            resStr=resStr+carid.toString()+","+carstatus+","+accomodate.toString()+","+cartype.toString()+"\n";
          });
          var com2="select * from `tasktransporting` where `quantity`!=0";
          connection.query(com2,function(err2,data2,fields2){
            if(data2.length==0){
              var com3="select * from `tasksinglerow` where `executed`=0";
              connection.query(com3,function(err3,data3,fields3){
                if(data3.length==0){
                  res.end(resStr);
                  return;
                }
                else{
                  var outid=data3[0]['taskid'];
                  console.log(outid);
                  resStr+="tasks incoming:\n";
                  for(let i=0;i<data3.length;i++){  
                    var row=data3[i];
                    if (outid!=row['taskid']){
                      
                    }
                    else{
                      resStr=resStr+row['taskid']+","+row['merchanid']+","+row['quantity'].toString()+"\n";
                    }
                    
                    
                  }
                  res.end(resStr);
                }
                
              })
            }
            else{
              resStr+="tasks unfulfilled:\n"
              console.log(data2);
              var outid=data2[0]['taskid'];
              console.log(outid);
              for(let i=0;i<data2.length;i++){
                var row=data2[i];
                if(outid!=row['taskid']){
                  
                }
                else{
                  resStr=resStr+row['taskid']+","+row['merchanid']+","+row['quantity'].toString()+"\n";
                }
                
              }
              res.end(resStr);
            }

          });
        });
      break;
      case "taskDecided":
        var taskid=params.taskID;
        comBusyCar="update `carstatus` set `status`='busy' where `status`='idle'";
        sqlQue(connection,comBusyCar);
        var com="update `tasksinglerow` set `executed`=1 where `taskid`="+stdSQLStr(taskid);
        var com2="select * from `tasksinglerow` where `taskid`="+stdSQLStr(taskid);
        sqlQue(connection,com);
        connection.query(com2,function(err,data,fields){
          data.forEach(function(row){
            var merchan=row['merchanid'];
            var quantity=row['quantity'];
            var com3="insert into `tasktransporting` "+stdSQLVal(stdSQLStr(taskid),stdSQLStr(merchan),quantity);
            sqlQue(connection,com3);
            if(row==data.at(-1)){
              res.end("decided");
            }
          })

        });

    }
  }
  return;
});
server.listen(port,hostname,()=>{
  console.log('server running at http://'+hostname+":"+port);
});