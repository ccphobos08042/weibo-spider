var linedata=[{
  xline:[1,2,3,4,5],//横轴标签
  sportline:[1,2,3,4,5],
  gameline:[1,2,3,4,5],
  realtimehotline:[1,2,3,4,5],
  entrankline:[1,2,3,4,5],
}]

var hdfslist=[];
function hdfspost(){
  fetch('/posthdfs', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify()
})
.then(response => response.json())
.then(data => {
    hdfslist=data.newData;
    const list = document.getElementById("hdfs");
    hdfslist.forEach(function(i){
      const li = document.createElement('li');
      li.classList=["item"];
      const a=document.createElement('a');
      a.href="http://192.168.217.10:9870/webhdfs/v1/user/hive/warehouse/cauc.db/"+i+".txt?op=OPEN";
      a.textContent =i+".txt";
      list.appendChild(li);
      li.appendChild(a);  
    });
    
})
.catch(error => console.error('Error:', error));
}
hdfspost();
function upload(){
  fetch("http://192.168.217.10:8080/upload",{
    method:'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify()
  })
  .then(response => response.json())
  .then(data => {
    if(data.result=="OK"){alert("备份成功");
      setTimeout(hdfspost(),1000);
    }
  })
  .catch(function(){
    
    alert("备份成功");
    setTimeout(hdfspost(),1000);
  }
)
  ;
}
function drop(){
  fetch("http://192.168.217.10:8080/delete",{
    method:'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify()
  })
  .then(response => response.json())
  .then(data => {
    if(data.result=="OK"){
      alert("删除备份成功");
      
    }
  })
  .catch(function(){
    alert("删除备份成功");
    const list = document.getElementById("hdfs");
    list.innerHTML='<div id="hdfs" class="scrollable-HDFS"></div>';
  }
)
  ;
}
function postline(s) {
        fetch('/postline', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({sep:s})
        })
        .then(response => response.json())
        .then(data => {
            linedata=[data.newData];
            line();
        })
        .catch(error => console.error('Error:', error));
    }
  postline(1);
// 基于准备好的dom，初始化echarts实例
function line(){    
var myChart = echarts.init(document.getElementById('main'));

// 指定图表的配置项和数据
var option = {

    tooltip: {
        trigger: 'axis'
    },
    legend: {
        data: ['主榜', '游戏', '文娱', '体育'],
        textStyle: {
                color: "#02a6b5" // 更改图例字体颜色
            }
    },
    xAxis: {
        type: 'category',
        data: linedata[0]["xline"]
    },
    yAxis: {
        type: 'value',
    },
    series: [
        {
            name: '主榜',
            type: 'line',
            data: linedata[0]["realtimehotline"]
        },
        {
            name: '游戏',
            type: 'line',
            data: linedata[0]["gameline"]
        },
        {
            name: '文娱',
            type: 'line',
            data: linedata[0]["entrankline"]
        },
        {
            name: '体育',
            type: 'line',
            data: linedata[0]["sportline"]
        }
    ]
};

// 使用刚指定的配置项和数据显示图表
myChart.setOption(option);}

var worddata=[
  {
              name: "暂无数据",
              value: 1,
            },
  
  {
              name: "暂无数据",
              value: 2,
            },
            {
              name: "暂无数据",
              value: 3,
            },
            {
              name: "暂无数据",
              value: 4,
            },
            {
              name: "暂无数据",
              value: 5,
            },
            {
              name: "暂无数据",
              value: 6,
            },
            {
              name: "暂无数据",
              value: 7,
            },{
              name: "暂无数据",
              value: 8,
            },{
              name: "暂无数据",
              value: 9,
            },{
              name: "暂无数据",
              value: 10,
            },{
              name: "暂无数据",
              value: 11,
            },{
              name: "暂无数据",
              value: 12,
            },{
              name: "暂无数据",
              value: 13,
            },{
              name: "暂无数据",
              value: 14,
            },{
              name: "暂无数据",
              value: 15,
            },{
              name: "暂无数据",
              value: 16,
            },{
              name: "暂无数据",
              value: 17,
            },{
              name: "暂无数据",
              value: 18,
            },{
              name: "暂无数据",
              value: 19,
            },{
              name: "暂无数据",
              value: 20,
            },{
              name: "暂无数据",
              value: 21,
            },{
              name: "暂无数据",
              value: 22,
            },{
              name: "暂无数据",
              value: 23,
            },{
              name: "暂无数据",
              value: 24,
            },{
              name: "暂无数据",
              value: 25,
            },{
              name: "暂无数据",
              value: 26,
            },{
              name: "暂无数据",
              value: 27,
            },{
              name: "暂无数据",
              value: 28,
            },{
              name: "暂无数据",
              value: 29,
            },{
              name: "NO DATA",
              value: 30,
            },
            ,{
              name: "NO DATA",
              value: 29,
            },
            
  ];
function postword(hotName) {
    fetch('/postword', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ hotName: hotName })
    })
    .then(response => response.json())
    .then(data => {
        var post_data=data.newData;
        insertscroll(post_data);
    })
    .catch(error => console.error('Error:', error));
}
function postData(hotName) {
  
    fetch('/post', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ hotName: hotName })
    })
    .then(response => response.json())
    .then(data => {
        worddata=data.newData;
        title=document.getElementById("title");
        title.textContent=hotName;
        wordword();
    })
    .catch(error => console.error('Error:', error));
    postword(hotName);

}

function wordword() {
  // 1. 实例化对象
  var myChart = echarts.init(document.querySelector(".words .chart"));
  option = {
    series: [
      {
        name: "热点分析",
        type: "wordCloud",
        // size: ['9%', '99%'],
        // sizeRange: [6, 66],//最小文字——最大文字
        // textRotation: [0, 45, 90, -45],
        // rotationRange: [-45, 90],//旋转角度区间
        // rotationStep: 90,//旋转角度间隔
        // shape: 'circle',
        // gridSize: 10,//字符间距
        textPadding: 0,
        autoSize: {
          enable: true,
          minSize: 6,
        },
        textStyle: {
          normal: {
            color: function () {
              return (
                "rgb(" +
                [
                  Math.round(Math.random() * 105) + 150,
                  Math.round(Math.random() * 105) + 150,
                  Math.round(Math.random() * 105) + 150,
                ].join(",") +
                ")"
              );
            },
          },
          emphasis: {
            shadowBlur: 10,
            shadowColor: "#333",
          },
        },data:worddata,
      },
    ],
  };

  // 3. 配置项和数据给我们的实例化对象
  myChart.setOption(option);
  // 4. 当我们浏览器缩放的时候，图表也等比例缩放
  window.addEventListener("resize", function () {
    // 让我们的图表调用 resize这个方法
    myChart.resize();
  });
}
wordword();
function transformFontSize(px) {
  let clientWidth = window.innerWidth || document.body.clientWidth
  if (!clientWidth) {
    return 0
  }
  let fontSize = clientWidth / 1920
  return px * fontSize
}
function showDiv(divId) {
  // Hide all content divs
  var divs =["sport","game","entrank","realtimehot"];
  divs.forEach(function(div) {
      var div = document.getElementById(div);
      div.style.display="none";
  });

  var selectedDiv = document.getElementById(divId);
  if (selectedDiv) {
      selectedDiv.style.display="block";
  }
}
function changecloud(){
  document.getElementById("cloud").style.display="";
  document.getElementById("wordscroll").style.display="none";
}
function changepost(){
  document.getElementById("cloud").style.display="none";
  document.getElementById("wordscroll").style.display="";
}
var stop=1;
var isroll = true;
function insertscroll(data){
  clearInterval(stop);
  const list = document.getElementById("wordscroll");
  list.innerHTML='<div style="display: none;" class="wordscroll" id="wordscroll"></div>';
  data.forEach(function(d){
    const li = document.createElement('li');
    const a=document.createElement('a');
    const hr=document.createElement('hr');
    a.textContent = d;
    list.appendChild(li);
    li.appendChild(a);  
    li.appendChild(hr);
  });

stop=setInterval(function(){
  const list = document.getElementById("wordscroll");
  if(isroll){list.scrollTop=list.scrollTop+1;}
  if(list.scrollTop>=list.scrollHeight-810){
    list.scrollTop=0;
  }
},15);
  } 

var element = document.getElementById("wordscroll");
isroll=true;
element.addEventListener("mouseover", function() {
  isroll = false;
  });
  
  element.addEventListener("mouseout", function() {
    isroll = true;
  });



