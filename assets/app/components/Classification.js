import React from 'react';
import ClassificationForm from './ClassificationForm';
import PieChart from './PieChart';
import HorizontalBarChart from './HorizontalBarChart';

export class Classification extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            domain: {x: [0, 30], y: [0, 100]},
            dataset: [],
            labelAccessor: (d => d[0]),
            valueAccessor: (d => d[1]),
        };
        this.getData = this.getData.bind(this);
    }
    getData (data) {
        this.setState({dataset:data.classification});
    }
    render() {
        return (
            <div className="row">
                <div className="col-md-5">
                    <br/>
                    <ClassificationForm sendData={this.getData} />
                </div>
                <div className="col-md-7 text-center">
                    <h3>Classification Results</h3>
                    <PieChart
                        innerRadius={50}
                        outerRadius={150}
                        boundingClientRect={{width:500, height:500}}
                        margins={{top:15,left:10, right:10,bottom:10}}
                        labelAccessor={this.state.labelAccessor}
                        valueAccessor={this.state.valueAccessor}
                        data={this.state.dataset}
                        show={true}
                    />
                </div>
                <div className="col-md-4">
                    <HorizontalBarChart
                        boundingClientRect={{width:400, height:400}}
                        margins={{top:10,left:10, right:10,bottom:10}}
                        labelAccessor={d=>d.label}
                        valueAccessor={d=>d.count}
                        data={this.state.dataset}
                        show={false}
                    />
                </div>
            </div>
        );
    }
}

export default Classification;
