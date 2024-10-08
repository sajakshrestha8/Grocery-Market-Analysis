import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.jsx";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import TopSection from "./assets/Components/TopSection.jsx";
import WrongPath from "./assets/Components/WrongPath.jsx";
import DailyData from "./DailyData.jsx";
import MonthyAnalysis from "./MonthlyAnalysis.jsx";
import UserData from "./UserData.jsx";
import AnalyticalResult from "./assets/Components/AnalyticalResult.jsx";
import AnalysisResults from "./assets/Components/Results.jsx";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <Router>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/dailydata" element={<DailyData />} />
        <Route path="/monthlyanalysis" element={<MonthyAnalysis />} />
        <Route path="/analysticalresult" element={<AnalyticalResult />} />
        <Route path="/userdata" element={<UserData />} />
        <Route path="/results" element={<AnalysisResults />} />
        <Route path="*" element={<WrongPath />} />
      </Routes>
    </Router>
  </React.StrictMode>
);
