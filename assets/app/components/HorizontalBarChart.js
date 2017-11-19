import React from 'react';
import { scaleLinear, scaleBand } from 'd3-scale';
import { axisLeft, axisBottom } from 'd3-axis';
import { select } from 'd3-selection';
import { max } from 'd3-array';

var d3 = require('d3');

class HorizontalBarChart extends React.Component {
    constructor(props) {
        super(props);
    }

    componentWillMount = () => {
    }

    componentDidMount = () => {
        this.renderBar();
    }

    renderBar() {
        const {
            data,
            boundingClientRect,
            valueAccessor,
            labelAccessor,
            showGridLines,
            margins,
        } = this.props;

        //labelAccessor = labelAccessor || (d => d);
        //valueAccessor = valueAccessor || (d => d);

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

        const group = svg
            .attr('width', width + left + right)
            .attr('height', height + top + bottom)
            .append('g')
            .attr('transform', `translate(${left}, ${top})`);

        const x = scaleLinear()
            .range([0, width])
            .domain([0, max(data, d => valueAccessor(d))]);

        const y = scaleBand()
            .rangeRound([height, 0])
            .domain(data.map(d => labelAccessor(d)))
            .padding(0.2);

        const xx = scaleLinear()
            .range([0, width]);
        const yy = scaleLinear()
            .range([height, 0]);

        const xAxis = axisBottom(x);
        const yAxis = axisLeft(y);

        group
            .append('g')
            .attr('class', 'x-axis')
            .attr('transform', `translate(0, ${height})`)
            .call(xAxis);

        group
            .append('g')
            .attr('class', 'y-axis')
            .call(yAxis);

        function addXgrid() {
            return axisBottom(xx)
                .ticks(data.length)
                .tickSize(-height)
                .tickFormat('');
        }

        function addYgrid() {
            return axisLeft(yy)
                .ticks(data.length)
                .tickSize(-width)
                .tickFormat('');
        }

        function addGrid() {
            group
                .append('g')
                .attr('class', 'grid')
                .attr('transform', `translate(0, ${height})`)
                .call(addXgrid());

            group
                .append('g')
                .attr('class', 'grid')
                .call(addYgrid());
        }

        if (showGridLines) {
            addGrid();
        }
        let color = d3.scaleOrdinal(d3.schemeCategory20b);

        const legend = group
            .selectAll('.bar')
            .data(data)
            .enter()
            .append('rect')
            .attr('class', 'bar')
            .attr('fill', (d, i) => color(i))
            .attr('x', 0)
            .attr('y', d => y(labelAccessor(d)))
            .attr('height', y.bandwidth())
            .attr('width', d => x(valueAccessor(d)));
    }

    render() {
        if (this.props.show) {
            return (
                <svg
                    className="horizontalbar"
                    ref={(elem) => { this.svg = elem; }}
                />
            );
        }
        return (<div/>);
    }
}

export default HorizontalBarChart;
