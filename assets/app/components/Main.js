import React from 'react';
import Classification from './Classification';
import TopicModeling from './TopicModeling';
import {Link, Switch, Router, Route, hashHistory} from 'react-router-dom';

export class Main extends React.Component {
    render() {
        return (
            <main>
                <ul className="nav-menu">
                    <li><Link to="/classification"><b>Classify</b></Link> | </li>
                    <li><Link to="/topic-modeling"><b>Topic Modeling</b></Link></li>
                </ul>
                <Switch>
                    <Route exact path='/' component={TopicModeling}/>
                    <Route path='/classification' component={Classify}/>
                    <Route path='/topic-modeling' component={TopicModeling}/>
                </Switch>
            </main>
        );
    }
}

const Classify = () => <Classification />
//const TopicModel = () => <TopicModeling/>

export default Main;
