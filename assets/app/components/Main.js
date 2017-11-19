import React from 'react';
import ClassificationForm from './ClassificationForm';
import Chart from './Chart';


export class Main extends React.Component {
    constructor(props) {
        super(props);
        this.state = {text:null}
        this.getData = this.getData.bind(this);
    }
    getData (data) {
        this.setState({result:JSON.stringify(data)});
    }
    render() {
        return (
            <div className="row">
                <div className="col-md-4">
                    <ClassificationForm sendData={this.getData} />
                </div>
                <div className="col-md-8">
                    <Chart {...this.state} />
                </div>
            </div>
        )
    }
}

export default Main;
