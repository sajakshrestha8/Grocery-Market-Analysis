import axios from "axios";
import { useEffect, useState } from "react";

export default function UserDataTable() {
  const [employeeInfo, setEmployeeInfo] = useState([]);

  useEffect(() => {
    async function fetchData() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/api/employees");
        setEmployeeInfo(response.data);
        console.log(response.data);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    }

    fetchData();
  }, []);
  return (
    <>
      <div className="right-container">
        <div className="heading">
          <label>Daily Transitions</label>
        </div>
        <div>
          <table className="data-table">
            <thead>
              <tr>
                <th>I.D</th>
                <th>Employee Name</th>
                <th>Position</th>
                <th>Department</th>
              </tr>
            </thead>
            <tbody>
              {employeeInfo.map((info) => (
                <tr key={info.id}>
                  <td>{info.id}</td>
                  <td>{info.name}</td>
                  <td>{info.position}</td>
                  <td>{info.department}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </>
  );
}
