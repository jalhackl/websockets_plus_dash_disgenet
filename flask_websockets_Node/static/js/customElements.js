

class D3DrawWidget extends HTMLElement {
    constructor(){
     
    super();

    let template = document.querySelector('#d3pie-template').content;
    this.attachShadow({ mode: 'open' }).appendChild(template.cloneNode(true));

    let circle = this.shadowRoot.querySelector("#circle");
    circle.style.fill = this.getAttribute('color');

    let svgCont = this.shadowRoot.querySelector("#container");


        var width = 100
        var  height = 100
        var margin = 5

        // The radius of the pieplot is half the width or half the height (smallest one). I subtract a bit of margin.
        var radius = Math.min(width, height) / 2 - margin

        // append the svg object to the div called 'my_dataviz'
        var svg = d3.select(svgCont)
          .append("svg")
            .attr("width", width)
            .attr("height", height)
          .append("g")
            .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

        // Create dummy data
        //var data = {a: 9, b: 20, c:30, d:8, e:12}
        var data = this.getAttribute('data');
        console.log(data);
        // set the color scale
        var color = d3.scaleOrdinal()
          .domain(data)
          .range(["#5E4FA2", "#3288BD", "#66C2A5", "#ABDDA4", "#E6F598", "#FF00BF", "#F0E08B", "#0DAE61", "#006D43", "#D53E4F", "#9E0142"])

        // Compute the position of each group on the pie:
        var pie = d3.pie()
          .value(function(d) {return d.value; })
        var data_ready = pie(d3.entries(data))

        // Build the pie chart: Basically, each part of the pie is a path that we build using the arc function.
        svg
          .selectAll('whatever')
          .data(data_ready)
          .enter()
          .append('path')
          .attr('d', d3.arc()
            .innerRadius(49)         // This is the size of the donut hole
            .outerRadius(20)
          )
          .attr('fill', function(d){ return(color(d.data.key)) })
          //.attr("stroke", "black")
          //.style("stroke-width", "2px")
          .style("opacity", 0.7)



    circle.addEventListener('click', () => {
    console.log('select '+ this.getAttribute('id'));




     
    });
    
    }


}





class InputGene extends HTMLElement {


constructor() {
super();
let template = document.querySelector('#gene-template').content;
  this.attachShadow({ mode: 'open' }).appendChild(template.cloneNode(true));

  let name_button = this.shadowRoot.querySelector("#name");
  let x_button = this.shadowRoot.querySelector("#x");

  name_button.textContent = this.getAttribute('name');
  name_button.style.background=this.getAttribute('color');//("background",);

  name_button.addEventListener('click', () => {
  console.log('select '+ this.getAttribute('id'));
  });

  x_button.addEventListener('click', () => {
      console.log('remove '+ this.getAttribute('id'));
      this.remove();
  });
}
}




class D3HistoPlot extends HTMLElement {


constructor() {
  super();

  let template = document.querySelector('#d3bar-template').content;
    this.attachShadow({ mode: 'open' }).appendChild(template.cloneNode(true));

    let svgCont = this.shadowRoot.querySelector("#container");
    svgCont.style.width = 360;
    svgCont.style.height = 400;

    var margin = {top: 10, right: 30, bottom: 30, left: 30}
    var width = 460 - margin.left - margin.right
    var height = 400 - margin.top - margin.bottom

    // append the svg object to the body of the page
    
// append the svg object to the body of the page
    var svg = d3.select(svgCont)
      .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform",
              "translate(" + margin.left + "," + margin.top + ")");

    // get the data
    d3.csv("https://raw.githubusercontent.com/holtzy/data_to_viz/master/Example_dataset/1_OneNum.csv", function(data) {

      // X axis: scale and draw:
      var x = d3.scaleLinear()
          .domain([0, 1000])     // can use this instead of 1000 to have the max of data: d3.max(data, function(d) { return +d.price })
          .range([0, width]);
      svg.append("g")
          .attr("transform", "translate(0," + height + ")")
          .call(d3.axisBottom(x));

      // set the parameters for the histogram
      var histogram = d3.histogram()
          .value(function(d) { return d.price; })   // I need to give the vector of value
          .domain(x.domain())  // then the domain of the graphic
          .thresholds(x.ticks(70)); // then the numbers of bins

      // And apply this function to data to get the bins
      var bins = histogram(data);

      // Y axis: scale and draw:
      var y = d3.scaleLinear()
          .range([height, 0]);
          y.domain([0, d3.max(bins, function(d) { return d.length; })]);   // d3.hist has to be called before the Y axis obviously
      svg.append("g")
          .call(d3.axisLeft(y));

      // append the bar rectangles to the svg element
      svg.selectAll("rect")
          .data(bins)
          .enter()
          .append("rect")
            .attr("x", 1)
            .attr("transform", function(d) { return "translate(" + x(d.x0) + "," + y(d.length) + ")"; })
            .attr("width", function(d) { 
                var w = x(d.x1) - x(d.x0) - 1 ;
                if (w > 0){return w;}
                else {return 0;} })
            .attr("height", function(d) { return height - y(d.length); })
            .style("fill", "#69b3a2")
            // Show tooltip on hover
           // .on("mouseover", showTooltip )
           // .on("mousemove", moveTooltip )
          //  .on("mouseleave", hideTooltip )

    });

}


}



customElements.define('gene-button', InputGene);
customElements.define('d3draw-widget', D3DrawWidget);
customElements.define('d3bar-widget', D3HistoPlot);

