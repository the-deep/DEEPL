import React from 'react';
import KeywordsExtractionForm from './KeywordsExtractionForm';


export default class KeywordsExtraction extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            data: {
                unigrams: [],
                bigrams: []
            },
            loaded: false,
        };
    }

    getData = (data) => {
        const loaded = true;
        this.setState({data, loaded});
    }

    render() {
        if (!this.state.loaded)
            return (
                <div className="row">
                    <div className="col-md-6">
                        <KeywordsExtractionForm sendData={this.getData} />
                    </div>
                </div>
            );
        return (
            <div className="row">
            <div className="col-md-6">
                <KeywordsExtractionForm sendData={this.getData} />
            </div>
            <div className="col-md-3">
                <h3> {this.state.loaded ? 'Unigrams':''}</h3>
                <table className="table table-bordered">
                    <tbody>
                    <tr><th>Unigram</th><th>Strength</th></tr>
                    {
                        this.state.data.unigrams.map((x, i) => (
                            <tr key={i}><td>{x[0]}</td><td>{x[1]}</td></tr>
                        ))
                    }
                    </tbody>
                </table>
            </div>
            <div className="col-md-3">
                <h3> {this.state.loaded ? 'Bigrams':''}</h3>
                <table className="table table-bordered">
                    <tbody>
                    <tr><th>Bigram</th><th>Strength</th></tr>
                    {
                        this.state.data.bigrams.map((x, i) => (
                            <tr key={i}><td>{x[0]}</td><td>{x[1]}</td></tr>
                        ))
                    }
                    </tbody>
                </table>
            </div>
            </div>
        );
    }
};
