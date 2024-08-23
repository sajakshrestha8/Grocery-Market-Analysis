import axios from "axios";
import CountDiv from "./assets/Components/CountDiv";
import "./assets/CSS/index.css";
import Sidebar from "./assets/Components/Sidebar";
import TopSection from "./assets/Components/TopSection";
import Graph from "./assets/Components/Graph";
import Growthcount from "./assets/Images/customer-count-img.jpeg";
import { useEffect, useState } from "react";

export default function App() {
  const [customerCount, setCustomerCount] = useState("");
  const [stockCount, setStockCount] = useState("");
  const [salesData, setSalesData] = useState([]);

  async function fetching() {
    const sajak = await axios
      .get("http://127.0.0.1:8000/api/total-customers")
      .then((data) => {
        setCustomerCount(data.data.total_customers);
      })
      .catch((e) => {
        console.log(e);
      });
  }

  async function stockcounting() {
    const stockcount = await axios
      .get("http://127.0.0.1:8000/api/stock-count")
      .then((data) => {
        setStockCount(data.data[0].quantity);
      })
      .catch((e) => {
        console.log(e);
      });
  }

  async function fetchSalesData() {
    try {
      const response = await axios.get("http://127.0.0.1:8000/api/daily-sales");
      const formattedData = response.data.map((item) => ({
        hour: `${item.hour}:00`,
        transaction_count: item.transaction_count,
      }));
      setSalesData(formattedData);
    } catch (error) {
      console.error("Error fetching sales data:", error);
    }
  }

  useEffect(() => {
    fetching();
    stockcounting();
    fetchSalesData();
  }, 2000);

  return (
    <>
      <div className="">
        <TopSection />
        <div className="main-container">
          <Sidebar />
          <div>
            <div className="top-container">
              <CountDiv
                title={"Coustomer Count"}
                customercount={customerCount}
                image={Growthcount}
              />
              <CountDiv
                title={"Stock Count"}
                customercount={stockCount}
                image={Growthcount}
              />
            </div>
            <br />
            <br />
            <Graph data={salesData} />
          </div>
        </div>
      </div>
    </>
  );
}
