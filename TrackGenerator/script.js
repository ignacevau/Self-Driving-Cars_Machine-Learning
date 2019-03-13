var myCanvas = $("#myCanvas");
var ctx = myCanvas[0].getContext('2d');
var canvasSize = { x: 800, y: 800 }
var points1 = [], points2 = [];
var middles1 = [], middles2 = [];
var points1_completed, points2_completed = false;
var currentMousePosition = [-1, -1];
var canvasOffset = myCanvas[0].getBoundingClientRect();
var status = "draw";
var dragIndex = [0, 0];
var closestIndex = 0;
var closestLinePoints = [[0, 0], [0, 0]];
var ProjPoint_temp, ProjPoint_updated = [0, 0];
var activatingCheckPoint = false;
var checkPointMode = false;
var startPoint = null;
var startPointMode = false;
var checkPoints = [];
var activeStartCheckPoint = [0, 0];

var insertPointActive = false;

myCanvas[0].width = canvasSize.x;
myCanvas[0].height = canvasSize.y;

//User checks/unchecks the checkpoint switch
$("#CheckPointSwitch").click(function (e) {
    if ($(this).is(":checked")) {
        checkPointMode = true;
    }
    else {
        checkPointMode = false;
    }
});

// User clicks the set start point button
$("#setStartPoint").click(function(e) {
    checkPointMode = false;
    $("#CheckPointSwitch").prop("checked", false);
    startPointMode = true;
});

//Prevent right click
$(document).ready(function () {
    myCanvas.on("contextmenu", function () {
        return false;
    });
});

//Update the mouse coordinates
myCanvas.mousemove(function (e) {
    currentMousePosition[0] = Math.round(e.pageX - canvasOffset.left);
    currentMousePosition[1] = Math.round(e.pageY - canvasOffset.top);
});

//User click, add the mouse coordinates as a new point
myCanvas.click(function (e) {
    if (status == "draw") {
        if (!points1_completed)
            points1.push([currentMousePosition[0], currentMousePosition[1]]);
        else if (!points2_completed)
            points2.push([currentMousePosition[0], currentMousePosition[1]]);
        latestPoint[0] = currentMousePosition[0];
        latestPoint[1] = currentMousePosition[1];

        draw();
    }
});

function getDistanceToLine(x, y, x1, y1, x2, y2) {
    var A = x - x1;
    var B = y - y1;
    var C = x2 - x1;
    var D = y2 - y1;

    var dot = A * C + B * D;
    var len_sq = C * C + D * D;
    var param = -1;
    if (len_sq != 0) //in case of 0 length line
        param = dot / len_sq;

    var xx, yy;

    if (param < 0) {
        xx = x1;
        yy = y1;
    }
    else if (param > 1) {
        xx = x2;
        yy = y2;
    }
    else {
        xx = x1 + param * C;
        yy = y1 + param * D;
    }

    var dx = x - xx;
    var dy = y - yy;

    //Save every projected (=closest) point calculated on a segment in a variable
    ProjPoint_temp = [xx, yy];

    return Math.sqrt(dx * dx + dy * dy);
}

function checkClosestLine(points, startPos) {
    var linePoints = [];
    var dist, minDist = null;

    for (var i = 0; i < points.length - 1; i++) {
        dist = getDistanceToLine(startPos[0], startPos[1], points[i][0], points[i][1], points[i + 1][0], points[i + 1][1]);
        if (minDist == null || dist < minDist) {
            minDist = dist;
            linePoints = [points[i], points[i + 1]];
            //Update the value of the projected point on the closed segment            
            ProjPoint_updated = ProjPoint_temp;
        }
    }
    //Compare first and last one from the list
    dist = getDistanceToLine(startPos[0], startPos[1], points[points.length - 1][0], points[points.length - 1][1], points[0][0], points[0][1]);
    if (minDist == null || dist < minDist) {
        minDist = dist;
        linePoints = [points[points.length - 1], points[0]];
        //Update the value of the projected point on the closed segment
        ProjPoint_updated = ProjPoint_temp;
    }
    return linePoints;
}

function canvasClear() {
    ctx.clearRect(0, 0, myCanvas[0].width, myCanvas[0].height);
}

myCanvas.mousemove(function (e) {
    if (dragIndex[0] != 0)
        dragPoint();

    if (points1_completed && points2_completed && checkPointMode) {
        //Outer layer of checkpoint has already been set
        if (activatingCheckPoint) {
            closestLinePoints = checkClosestLine(points1, currentMousePosition);
        }
        //None of the checkpoint layers has been set
        else {
            closestLinePoints = checkClosestLine(points2, currentMousePosition);
        }
    }

    if(startPointMode) {
        startPoint = jQuery.extend({}, currentMousePosition);
    }

    draw();
});

myCanvas.on('mouseup', function (e) {
    dragIndex = [0, 0];
});

function checkForClickedPoints(points, radius) {
    for (i = 0; i < points.length; i++) {
        if (Math.abs(currentMousePosition[0] - points[i][0]) < radius && Math.abs(currentMousePosition[1] - points[i][1]) < radius) {
            return i;
        }
    }
    return -1;
}

myCanvas.on('mousedown', function (e) {
    var _keycode = e.which;

    if (points1_completed && points2_completed) {
        //check whether the user clicked one of the first layer points
        var _p1Click = checkForClickedPoints(points1, 5);
        var _p2Click = checkForClickedPoints(points2, 5);

        //if clicked on point with the left mouse button, set the dragIndex
        if (_keycode == 1) {
            if (_p1Click != -1)
                dragIndex = [1, _p1Click];
            if (_p2Click != -1)
                dragIndex = [2, _p2Click];
        }
        //if clicked on point with right mouse button, delete the point
        else if (_keycode == 3) {
            if (_p1Click != -1)
                points1.splice(_p1Click, 1);
            if (_p2Click != -1)
                points2.splice(_p2Click, 1);
        }

        //User is holding Ctrl and both layers are done
        if (insertPointActive) {
            var _m1Click = checkForClickedPoints(middles1, 6);
            var _m2Click = checkForClickedPoints(middles2, 6);

            if (_keycode == 1) {
                //Add the point to the layer
                if (_m1Click != -1)
                    points1.splice(_m1Click + 1, 0, [currentMousePosition[0], currentMousePosition[1]]);
                if (_m2Click != -1)
                    points2.splice(_m2Click + 1, 0, [currentMousePosition[0], currentMousePosition[1]]);
            }
        }

        // User is placing checkpoints
        if (checkPointMode) {
            // First layer has already been set
            if (activatingCheckPoint) {
                checkPoints.push([activeStartCheckPoint, ProjPoint_updated]);
                activatingCheckPoint = false;

                // Make the position off the projected ball again to points2
                closestLinePoints = checkClosestLine(points2, currentMousePosition);
            }
            // First layer hasn't been set yet
            else {
                activeStartCheckPoint = ProjPoint_updated;
                activatingCheckPoint = true;
            }
        }

        if(startPointMode) {
            startPointMode = false;
        }

        draw();
    }
});

//Ctrl key pressed
$(document).keydown(function (e) {
    if (e.which == 17 && points1_completed && points2_completed) {
        insertPointActive = true;
        draw();
    }
});

//Ctrl key released
$(document).keyup(function (e) {
    if (e.which == 17) {
        insertPointActive = false;
        ctx.clearRect(0, 0, myCanvas[0].width, myCanvas[0].height);
        draw();
    }
})

function drawMiddles(_middles, color) {
    ctx.fillStyle = color;

    for (var i = 0; i < _middles.length; i++) {
        ctx.beginPath()
        ctx.arc(_middles[i][0], _middles[i][1], 6, 0, 2 * Math.PI, true)
        ctx.fill();
    }
}

function getLineMiddles(points) {
    var _middles = [];
    for (var i = 0; i < points.length - 1; i++) {
        _middles.push([(points[i][0] + points[i + 1][0]) / 2, (points[i][1] + points[i + 1][1]) / 2 ]);
    }
    //Add the middle of the last point and the first point
    _middles.push([(points[points.length - 1][0] + points[0][0]) / 2, (points[points.length - 1][1] + points[0][1]) / 2]);

    return _middles;
}

function dragPoint() {
    if (dragIndex[0] == 1) {
        points1[dragIndex[1]][0] = currentMousePosition[0];
        points1[dragIndex[1]][1] = currentMousePosition[1];
    }
    else if (dragIndex[0] == 2) {
        points2[dragIndex[1]][0] = currentMousePosition[0];
        points2[dragIndex[1]][1] = currentMousePosition[1];
    }
}

//Check for enter key
$(document).keypress(function (e) {
    if (e.which == 13) {
        if (!points1_completed)
            points1_completed = true;
        else if (!points2_completed) {
            points2_completed = true;
            status = "done";
        }

        draw();
    }
});

// Export the track
$('#exportBtn').click(function(e) {
    var data = {};
    data.points1 = points1;
    data.points2 = points2;
    data.checkPoints = checkPoints;
    data.startPoint = startPoint;

    var encodedData = "text/json; charset=utf-8," + encodeURIComponent(JSON.stringify(data));

    var temp_a = document.createElement('a');
    document.body.appendChild(temp_a);
    temp_a.download = 'Track.json';
    temp_a.href = "data:" + encodedData;

    temp_a.click();
    temp_a.remove();
});

// Import the track
$('#importBtn').click(function() {
    var input = document.createElement('input');
    document.body.appendChild(input);
    input.style = "display: none;";
    input.type = "file";
    input.click();
    input.onchange = function(event) {
        var reader = new FileReader();

        reader.onload = function (event) {
            var json = JSON.parse(event.target.result);

            points1 = json.points1;
            points2 = json.points2;
            checkPoints = json.checkPoints;
            startPoint = json.startPoint;
    
            points1_completed = true;
            points2_completed = true;
            draw();

            input.remove();
        }
        reader.readAsText(event.target.files[0])
    };
});

var latestPoint = [0, 0];
function draw() {
    canvasClear();

    if (!points1_completed) {
        drawPoints(points1);
        drawMouseLine(points1);
    }
    else if (!points2_completed) {
        drawPoints(points1);
        drawPoints(points2);
        drawMouseLine(points2);

        drawCompleted(points1);
    }
    else {
        drawPoints(points1);
        drawPoints(points2);

        drawCompleted(points1);
        drawCompleted(points2);
    }

    if(startPoint != null) {
        ctx.fillStyle = '#3ec572';
        ctx.beginPath();
        ctx.arc(startPoint[0], startPoint[1], 13, 0, 2 * Math.PI, true);
        ctx.fill();
        
        ctx.fillStyle = 'white';
        ctx.beginPath();
        ctx.arc(startPoint[0], startPoint[1], 8, 0, 2 * Math.PI, true);
        ctx.fill();

        ctx.fillStyle = '#3ec572';
        ctx.beginPath();
        ctx.arc(startPoint[0], startPoint[1], 5, 0, 2 * Math.PI, true);
        ctx.fill();
    }

    drawBalls(points1, '#3f8efc');
    drawBalls(points2, '#ff5454');

    // Both layers have been set
    if(points1_completed && points2_completed) {
        if(checkPointMode) {
            // Draw active segment (yellow selection line)
            drawLine(closestLinePoints[0][0], closestLinePoints[0][1], closestLinePoints[1][0], closestLinePoints[1][1], 'yellow', 2);
            drawBalls(closestLinePoints, 'yellow');

            //Draw projected ball
            ctx.fillStyle = 'limegreen';
            ctx.beginPath()
            ctx.arc(ProjPoint_updated[0], ProjPoint_updated[1], 4, 0, 2 * Math.PI, true)
            ctx.fill();
            
            // First checkpoint layer has been set - draw the connect line
            if(activatingCheckPoint) {
                drawBalls([activeStartCheckPoint], 'limegreen');
                drawLine(activeStartCheckPoint[0], activeStartCheckPoint[1], ProjPoint_updated[0], ProjPoint_updated[1], 'limegreen', 1);
            }
        }

        // Draw all the checkpoints
        if(checkPoints.length > 0) {
            for(var i = 0; i < checkPoints.length; i++) {
                drawLine(checkPoints[i][0][0], checkPoints[i][0][1], checkPoints[i][1][0], checkPoints[i][1][1], 'limegreen', 1);
            }
        }
    }

    if (insertPointActive) {
        middles1 = getLineMiddles(points1);
        middles2 = getLineMiddles(points2);
        drawMiddles(middles1, '#a9cbfc');
        drawMiddles(middles2, '#ff8282');
    }
}

function drawCompleted(points) {
    drawLine(points[0][0], points[0][1], points[points.length - 1][0], points[points.length - 1][1]);
}

function drawPoints(points) {
    if (points.length >= 2) {
        for (var i = 0; i < points.length - 1; i++) {
            drawLine(points[i][0], points[i][1], points[i + 1][0], points[i + 1][1]);
        }
    }
}

function drawBalls(points, color) {
    ctx.fillStyle = color;
    for (var i = 0; i < points.length; i++) {
        ctx.beginPath();
        ctx.arc(points[i][0], points[i][1], 5, 0, 2 * Math.PI, true);
        ctx.fill();
    }
}

function drawLine(x1, y1, x2, y2, color = 'black', width = 1) {
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(x2, y2);
    ctx.strokeStyle = color;
    ctx.lineWidth = width;
    ctx.stroke();
}

function drawMouseLine(points) {
    if (points.length >= 1) {
        drawLine(latestPoint[0], latestPoint[1], currentMousePosition[0], currentMousePosition[1]);
    }
}