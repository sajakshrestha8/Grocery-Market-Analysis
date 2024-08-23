import axios from "axios";
import { useEffect, useState } from "react";

export default function RightContainerDailyData() {
  const [transactions, setTransactions] = useState([]);

  useEffect(() => {
    async function fetchData() {
      try {
        const response = await axios.get(
          "http://127.0.0.1:8000/api/daily-transactions"
        );
        setTransactions(response.data);
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
                <th>S.N.</th>
                <th>Name</th>
                <th>Qunatity</th>
                <th>Date</th>
              </tr>
            </thead>
            <tbody>
              {transactions.map((transaction) => (
                <tr key={transaction.product_name}>
                  <td>{transaction.id}</td>
                  <td>{transaction.product_name}</td>
                  <td>{transaction.quantity}</td>
                  <td>{transaction.transaction_date}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </>
  );
}
