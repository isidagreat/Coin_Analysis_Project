function svgExample()
{
	// Select the body and begin DOM manipulation

	var canvas = d3.select(".bar-chart")
	.append("svg")
	.attr("width", 800)
	.attr("height", 500);

	var circle = canvas.append("circle")
		.attr("cx", 50)
		.attr("cy", 50)
		.attr("r", 50)
		.attr("fill", "red");
}