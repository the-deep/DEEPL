import React from 'react';
import ClassificationForm from './ClassificationForm';
import PieChart from './PieChart';
import HorizontalBarChart from './HorizontalBarChart';

let dataset = [
  { label: 'Abulia', count: 10 },
  { label: 'Betelgeuse', count: 20 },
  { label: 'Cantaloupe', count: 30 },
  { label: 'Dijkstra', count: 40 }
];

export class Main extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            data: dataset,
            domain: {x: [0, 30], y: [0, 100]},
            dataset: dataset,
        };
        this.getData = this.getData.bind(this);
    }
    getData (data) {
        this.setState({dataset:data.tags});
    }
    render() {
        return (
            <div className="row">
                <div className="col-md-4">
                    <ClassificationForm sendData={this.getData} />
                </div>
                <div className="col-md-4">
                    <PieChart
                        innerRadius={100}
                        outerRadius={175}
                        boundingClientRect={{width:400, height:400}}
                        margins={{top:10,left:10, right:10,bottom:10}}
                        labelAccessor={d=>d.label}
                        valueAccessor={d=>d.count}
                        data={this.state.dataset}
                    />
                </div>
                <div className="col-md-4">
                    <HorizontalBarChart
                        boundingClientRect={{width:400, height:400}}
                        margins={{top:10,left:10, right:10,bottom:10}}
                        labelAccessor={d=>d.label}
                        valueAccessor={d=>d.count}
                        data={this.state.dataset}
                    />
                </div>
            </div>
        );
    }
}

export default Main;
