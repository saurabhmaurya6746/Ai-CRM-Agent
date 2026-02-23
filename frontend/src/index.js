import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import { Provider } from 'react-redux'; // ✅ Ye missing tha
import { store } from './redux/store';   // ✅ Ye missing tha

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    {/* ⬇️ Ye Provider hi store ko poore App mein bhejta hai */}
    <Provider store={store}> 
      <App />
    </Provider>
  </React.StrictMode>
);