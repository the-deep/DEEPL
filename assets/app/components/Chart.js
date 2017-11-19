import React from 'react';

class Chart extends React.Component {
    constructor(props) {
        super(props)
        this.state = {};
    }
    render() {
        return (
            <p>{this.props.result}</p>
        )
    }
}

export default Chart
