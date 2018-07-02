import React from 'react';
import Classification from './Classification';
import TopicModeling from './TopicModeling';
import KeywordsExtraction from './KeywordsExtraction';
import {Link, Switch, Router, Route, hashHistory} from 'react-router-dom';

export class Main extends React.Component {
    componentDidMount() {
        console.log('fetching token');
        fetch('/api/token', {
            credentials: "same-origin"
        })
        .then(response => response.json())
        .then(data => {
            localStorage.clear();
            localStorage.setItem('api_token', data['api_token']);
            localStorage.setItem('test_token', data['test_token']);
        });
    }

    render() {
        return (
            <main>
                <ul className="nav-menu">
                    <li><Link to="/classification"><b>Classify</b></Link> | </li>
                    <li><Link to="/topic-modeling"><b>Topic Modeling</b></Link> | </li>
                    <li><Link to="/keywords-extraction"><b>Keywords Extraction</b></Link></li>
                </ul>
                <Switch>
                    <Route exact path='/' component={TopicModeling}/>
                    <Route path='/classification' component={Classify}/>
                    <Route path='/topic-modeling' component={TopicModeling}/>
                    <Route path='/keywords-extraction' component={KeywordsExtraction}/>
                </Switch>
            </main>
        );
    }
}

const Classify = () => <Classification />
//const TopicModel = () => <TopicModeling/>

export default Main;
