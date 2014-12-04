// Tony Cannistra, Brett Fischler, Dan Griffin
// Fall 2014
// Comp50 Final Project

// Reformats the given list of lists
function setList(ListofLists) {
    var temp = {};
    for (var i = 0; i < ListofLists.length; i++){
      List = ListofLists[i];
      for (var j = 0; j < List.length; j++){ 
        temp[List[j]] = true;
      }
    }
    var r = [];
    for (var k in temp)
        r.push(parseInt(k));
    return r;
}

// 
function search() {
    var from_text = document.getElementById("from_text").value
    var to_text = document.getElementById("to_text").value
    if (from_text == "" || to_text == "") {
        alert("Please enter source and destination");
    } else {
        $("svg").remove();
        document.getElementById("searching").style.visibility = "visible";
        $.ajax({
            type: "GET",
            url: "/getData",
            data: { "from_page": from_text, "to_page": to_text },
            success: function(data){
                document.getElementById("searching").style.visibility = "hidden";
                if (data["error"] == "error") {
                    alert("Unable to access server");
                    return;
                }
                if (data.length < 1) {
                    alert("No paths found");
                    return;     
                }
                //console.log(data);  
                nodesDic = {};
                nodes = [];
                links = [];
                pathsLinks = {};
                var first_path_count = 0;
                var num_paths = data.length;
                for(var i = 0; i < num_paths; i++){
                    current_path = [];
                    var path = data[i];
                    var num_in_path = path.length;
                    for (var j = 0; j < num_in_path; j++){
                        index = nodesDic[path[j]];
                        if (index == undefined){
                            nodesDic[path[j]] = nodes.length;
                            if (i == 0){
                                nodes.push({"name": path[j], "group":1});
                            }else{
                                nodes.push({"name": path[j], "group":2});
                            }
                        }
                    }
                    //{"source":1,"target":0,"value":1},
                    if (i == 0){
                        first_path_count = num_in_path - 1;
                    }
                    for (var j = 0; j < num_in_path - 1; j++) {
                        current_path.push( links.length );
                        if (i == 0){
                            links.push({"source": nodesDic[path[j]],
                                "target": nodesDic[path[j + 1]], "value": 10});
                        }else{
                            links.push({"source": nodesDic[path[j]],
                                "target": nodesDic[path[j + 1]], "value": 1});
                        }
                    }
                    for (var j = 0; j < num_in_path; j++){
                        if(pathsLinks[path[j]] == undefined){
                            pathsLinks[path[j]] = [];
                        }
                        pathsLinks[path[j]].push(current_path);
                    }
                }

                for (var k in pathsLinks){
                    pathsLinks[k] = setList(pathsLinks[k]);
                }

                var graph = {"nodes": nodes, "links": links};

                var width = 1080;
                var height = 1080;

                var color = d3.scale.category20();

                // Sets force parameters
                var force = d3.layout.force()
                    .charge(-500)
                    .linkDistance(250)
                    .friction(0.95)
                    .gravity(0.1)
                    .linkStrength(0.01)
                    .size([width, height]);

                var svg = d3.select("body").append("svg")
                    .attr("width", width)
                    .attr("height", height);

                var drawGraph = function(graph) {
                    force
                        .nodes(graph.nodes)
                        .links(graph.links)
                        .start();

                    var link = svg.selectAll(".link")
                        .data(graph.links)
                        .enter().append("line")
                        .attr("class", "link")
                        .style("stroke-width", function(d) { 
                            return Math.sqrt(d.value);
                        });

                    var gnodes = svg.selectAll('g.gnode')
                        .data(graph.nodes)
                        .enter()
                        .append('g')
                        .classed('gnode', true);

                    var node = gnodes.append("circle")
                        .attr("class", "node")
                        .attr("r", 5)
                        .style("fill", function(d) { 
                            return color(d.group);
                        })
                        .call(force.drag);



                    node.on('mouseover', function(d) {
                        linksPresent = pathsLinks[d["name"]];
                        link.classed("currentPath", function(l,i) {
                            return (linksPresent.indexOf(i) != -1);
                        });

                    });

                    // Set the stroke width back to normal when mouse leaves
                    node.on('mouseout', function() {
                        link.classed("currentPath",false);
                    });

                    var labels = gnodes.append("text")
                        .text(function(d) { return d.name; });

                    console.log(labels);
                    
                  force.on("tick", function() {
                    link.attr("x1", function(d) { return d.source.x; })
                        .attr("y1", function(d) { return d.source.y; })
                        .attr("x2", function(d) { return d.target.x; })
                        .attr("y2", function(d) { return d.target.y; });

                    gnodes.attr("transform", function(d) { 
                        return 'translate(' + [d.x, d.y] + ')'; 
                    });
                      
                    
                      
                  });
                };

                // Draws the Force-Directed Graph
                drawGraph(graph);

                lines = $("line");
                for (var i = 0; i < first_path_count; i++){
                    lines[i].style.stroke = "red";
                }

              },
          dataType: "json"
        });
    }
}
