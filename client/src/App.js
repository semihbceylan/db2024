import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import eoas from './pages/eoas';
// Import your table components

function App() {
  return (
    <Router>
      <Switch>
        <Route path="/table1" component={eoas} />
      </Switch>
    </Router>
  );
}

export default App;
