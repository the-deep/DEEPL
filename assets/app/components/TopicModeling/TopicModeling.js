import React from 'react';
import TopicModelingForm from './TopicModelingForm';

export default class TopicModeling extends React.Component {
    constructor(props) {
        super(props);
        this.state = {data:[], title:''};
    }

    getData = (data) => {
        let processed_data = Object.keys(data).map(
            key => [key, data[key].keywords.map(x=>x[0]), Object.keys(data[key].subtopics).map(
                subkey => [subkey, data[key].subtopics[subkey].keywords.map(x=>x[0]), {}]
            )]
        );
        this.setState({data:processed_data, title:'Topic Composition'});
    }
    render() {
        const data = this.state.data;
        let subtopicsmap = (x, i) => (
            <ul >
                <li className='child-li' key={i}><b>Sub-{x[0]}</b> -> {
                    x[1].map((x, j)=>(
                        <span key={j}>{x}, &nbsp;</span>
                    ))
                }
                </li>
            </ul>
        );
        return(
            <div className="row">
                <div className="col-md-5">
                    <br/>
                    <TopicModelingForm sendData={this.getData} />
                </div>
                <div className="col-md-7">
                    <h3>{this.state.title}</h3>
                    <hr />
                    <ul>
                     {data.map((x,i) => (
                         <li key={i}>
                            <b>{x[0]}</b> -> {
                                x[1].map((y,j) => (
                                    <span key={j}>{y},&nbsp;</span>
                                ))
                            }
                                {
                                    x[2].map(subtopicsmap)
                                }
                         <hr />
                         </li>
                     ))}
                    </ul>
                </div>
            </div>
        );
    }
}
