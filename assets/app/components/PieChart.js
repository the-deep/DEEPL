import React from 'react';
import { scaleLinear, scaleBand } from 'd3-scale';
import { axisLeft, axisBottom } from 'd3-axis';
import { select } from 'd3-selection';
import { max } from 'd3-array';

const d3 = require('d3');

class PieChart extends React.Component {
    constructor(props) {
        super(props);
    }

    componentDidMount = () => {
        this.renderPie();
    }

    renderPie = () => {
        const {
            innerRadius,
            outerRadius,
            labelAccessor,
            valueAccessor,
            data,
            boundingClientRect,
            margins,
        } = this.props;

        if (!boundingClientRect.width) {
            return;
        }
        let { width, height } = boundingClientRect;
        const {
            top,
            right,
            bottom,
            left,
        } = margins;

        width = width - left - right;
        height = height - top - bottom;

        if (width < 0) width = 0;
        if (height < 0) height = 0;

        const svg = select(this.svg);
        svg.select('*').remove();

        const group = svg.attr("width", width)
            .attr("height", height)
            .append("svg:g")
            .attr("transform", "translate(" + outerRadius + "," + outerRadius + ")");

        let color = d3.scaleOrdinal(d3.schemeCategory20b);

        const arc = d3.arc()
            .innerRadius(innerRadius)
            .outerRadius(outerRadius);

        const pie = d3.pie()
            .value(valueAccessor)
            .sort(null);

        const labels = group
            .selectAll('path')
            .data(pie(data))
            .enter()
            .append('path')
            .attr('d', arc)
            .attr('fill', function(d) {
                return color(d.data.label);
            });
        labels
            .append("title")
          .text((d, i) => labelAccessor(d.data));

        var legendRectSize = 18;
        var legendSpacing = 4;

        let legend = group.selectAll('.legend')
            .data(color.domain())
            .enter()
            .append('g')
            .attr('class', 'legend')
            .attr('transform', function(d, i) {
                var height = legendRectSize + legendSpacing;
                var offset =  height * color.domain().length / 2;
                var horz = -2 * legendRectSize;
                var vert = i * height - offset;
                return 'translate(' + horz + ',' + vert + ')';
            });
        legend.append('rect')
            .attr('width', legendRectSize)
            .attr('height', legendRectSize)
            .style('fill', color)
            .style('stroke', color);

        // calculate total
        let total = data.map(x=> valueAccessor(x)).reduce((s, x)=> s+x);

        legend.append('text')
            .attr('x', legendRectSize + legendSpacing)
            .attr('y', legendRectSize - legendSpacing)
            .text((d, i) => d+"("+valueAccessor(data[i])*100/total+"%)");
    }

    render() {
        return (
            <svg
                className="piechart"
                ref={(elem) => { this.svg = elem; }}
            />
        );
    }
}

export default PieChart;
