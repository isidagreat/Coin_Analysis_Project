console.log("its working")

function parseData(data){
	var dataResponse = [];
	for (i = 0; i < data.length; i++ )
	{
		dataResponse.push(
		{
			date: new Date(data[i]['time']),
			value: +data[i]['price']
		});
	}
	return dataResponse
}


function drawChart(data,) {
	var svgWidth = 800, svgHeight = 500;
	var margin = { top: 20, right: 20, bottom: 30, left: 50 };
	var width = svgWidth - margin.left - margin.right;
	var height = svgHeight - margin.top - margin.bottom;

	var svg = d3.select(".line-chart")
	.attr("width", svgWidth)
	.attr("height", svgHeight);

	var g = svg.append("g")
	.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

	var x = d3.scaleTime()
	.rangeRound([0, width]);

	var y = d3.scaleLinear()
	.rangeRound([height, 0]);

	var line = d3.line()
	.x(function(d) { return x(d.date)})
	.y(function(d) { return y(d.value)})
	x.domain(d3.extent(data, function(d) { return d.date }));
	y.domain(d3.extent(data, function(d) { return d.value }));

	g.append("g")
	.attr("transform", "translate(0," + height + ")")
	.call(d3.axisBottom(x))
	.select(".domain")
	.remove();

	g.append("g")
	.call(d3.axisLeft(y))
	.append("text")
	.attr("fill", "#000")
	.attr("transform", "rotate(-90)")
	.attr("y", 6)
	.attr("dy", "0.71em")
	.attr("text-anchor", "end")
	.text("Price ($)");

	g.append("path")
	.datum(data)
	.attr("fill", "none")
	.attr("stroke", "steelblue")
	.attr("stroke-linejoin", "round")
	.attr("stroke-linecap", "round")
	.attr("stroke-width", 1.5)
	.attr("d", line);
}
function drawChart2(data, theDiv) {
	var svgWidth = 800, svgHeight = 500;
	var margin = { top: 20, right: 20, bottom: 30, left: 50 };
	var width = svgWidth - margin.left - margin.right;
	var height = svgHeight - margin.top - margin.bottom;

	var svg = d3.select(theDiv)
	.attr("width", svgWidth)
	.attr("height", svgHeight);

	var g = svg.append("g")
	.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

	var x = d3.scaleTime()
	.rangeRound([0, width]);

	var y = d3.scaleLinear()
	.rangeRound([height, 0]);

	var line = d3.line()
	.x(function(d) { return x(d.date)})
	.y(function(d) { return y(d.value)})
	x.domain(d3.extent(data, function(d) { return d.date }));
	y.domain(d3.extent(data, function(d) { return d.value }));

	g.append("g")
	.attr("transform", "translate(0," + height + ")")
	.call(d3.axisBottom(x))
	.select(".domain")
	.remove();

	g.append("g")
	.call(d3.axisLeft(y))
	.append("text")
	.attr("fill", "#000")
	.attr("transform", "rotate(-90)")
	.attr("y", 6)
	.attr("dy", "0.71em")
	.attr("text-anchor", "end")
	.text("Price ($)");

	g.append("path")
	.datum(data)
	.attr("fill", "none")
	.attr("stroke", "steelblue")
	.attr("stroke-linejoin", "round")
	.attr("stroke-linecap", "round")
	.attr("stroke-width", 1.5)
	.attr("d", line);
}