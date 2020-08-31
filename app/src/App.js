import React from 'react';
import './App.scss';
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom";
import EmbedG from "./pages/Embedg";
import 'react-notifications/lib/notifications.css';
import {NotificationContainer} from 'react-notifications';

function App() {
  return (
    <div>
      <Router>
        <ul>
          <li>
            <Link to="/">Home</Link>
          </li>
          <li>
            <Link to="/embedg"> Embed Generator</Link>
          </li>
        </ul>

        <Switch>
          <Route exact path="/">
            <h1>Home</h1>
          </Route>
          <Route path="/embedg">
            <EmbedG/>
          </Route>

          <Route path="*">
            <h1>Not Found</h1>
          </Route>
        </Switch>
      </Router>
      <NotificationContainer/>
    </div>
  );
}

export default App;
