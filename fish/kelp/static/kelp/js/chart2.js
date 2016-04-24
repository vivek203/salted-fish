var margin = {top: 20, right: 40, bottom: 30, left: 40},
									width = 960 - margin.left - margin.right,
									height = 550 - margin.top - margin.bottom;

								var x = d3.scale.ordinal()
									.rangeRoundBands([0, width], .1);

								var y = d3.scale.linear()
									.range([height, 0]);
		
								var y1 = d3.scale.linear()
									.range([height, 0]);

								var xAxis = d3.svg.axis()
									.scale(x)
									.orient("bottom");

								var yAxis = d3.svg.axis()
									.scale(y)
									.orient("left");
			
								var yAxisRight = d3.svg.axis()
									.scale(y1)
									.orient("right");
									// .ticks(5); 

								var svg2 = d3.select("#portfolioModal2").append("svg")
									.attr("width", width + margin.left + margin.right)
									.attr("height", height + margin.top + margin.bottom)
								  .append("g")
									.attr("transform", "translate(" + margin.left + "," + margin.top + ")");
			
								var line = d3.svg.line()
										.x(function(d) { return ( x(d.date)+10 ); })
										.y(function(d) { return y1(d.temperature); });

								d3.tsv("{% static 'kelp/data/dateTemp.tsv' %}", type, function(error, data) {
								  if (error) throw error;

								  x.domain(data.map(function(d) { return d.date; }));
								  y.domain([0, d3.max(data, function(d) { return d.temperature; })]);
								  y1.domain([0, d3.max(data, function(d) { return d.temperature; })]);

								  svg2.append("g")
									  .attr("class", "x axis")
									  .attr("transform", "translate(0," + height + ")")
									  .call(xAxis)
									.append("text")
									  .style("text-anchor", "end")
									  .attr("x", 450)
									  .attr("dy", "2.65em")
									  .text("Date");

									svg2.append("g")
									  .attr("class", "y axis")
									  .call(yAxis)
									.append("text")
									  .attr("transform", "rotate(-90)")
									  .attr("y", 6)
									  .attr("dy", ".71em")
									  .style("text-anchor", "end")
									  .text("Temperature");
			  
									svg2.append("g")				
										.attr("class", "y axis")	
										.attr("transform", "translate(" + width + " ,0)")
										.style("fill", "red")		
										.call(yAxisRight);

								  svg2.selectAll(".bar")
									  .data(data)
									.enter().append("rect")
									  .attr("class", "bar")
									  .attr("x", function(d) { return x(d.date); })
									  .attr("width", x.rangeBand())
									  .attr("y", function(d) { return y(d.temperature); })
									  .attr("height", function(d) { return height - y(d.temperature); });
			  
			
				
									svg2.append("path")
									  .datum(data)
									  .attr("class", "line")
									  .attr("d", line);
			  
			  
								});

								function type(d) {
								  d.temperature = +d.temperature;
								  return d;
								}