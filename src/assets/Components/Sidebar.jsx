// import { Link } from "react-router-dom";

import Profile from "../Images/profile.jpeg";
import { Link } from "react-router-dom";

export default function Sidebar(props) {
  return (
    <>
      <div className="left-container">
        <div className="profile-grid">
          <div className="profile-logo">
            <img src={Profile} alt="profile" />
          </div>
          <div>
            <div className="profile-name">
              <label>Sajak Shrestha</label>
            </div>
            <div className="profile-status">
              <label>Active</label>
            </div>
          </div>
        </div>
        <Link to={"/"} className="menu">
          <label>Dashboard</label>
        </Link>
        <Link to={"/dailydata"} className="menu">
          <label>Daily Data</label>
        </Link>
        <Link to={"/monthlyanalysis"} className="menu">
          <label>Monthly Analysis</label>
        </Link>
        <Link to={"/analysticalresult"} className="menu">
          <label>Analytical Result</label>
        </Link>
        <div className="menu">
          <label>Prediction Report </label>
        </div>
        <Link to={"/userdata"} className="menu">
          <label>User Database</label>
        </Link>
        <div className="menu">
          <label>Add Transitions</label>
        </div>
        <div className="menu">
          <label>LogOut</label>
        </div>
      </div>
    </>
  );
}
