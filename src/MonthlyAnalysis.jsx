import { PieChart } from "recharts";
import CountDiv from "./assets/Components/CountDiv";
import Graph from "./assets/Components/Graph";
import Sidebar from "./assets/Components/Sidebar";
import TopSection from "./assets/Components/TopSection";
import Growthcount from "./assets/Images/customer-count-img.jpeg";
import Piechart from "./assets/Components/Piechart";

export default function MonthyAnalysis() {
  return (
    <>
      <TopSection />
      <div className="main-container">
        <Sidebar />
        <div>
          <div className="top-container">
            <CountDiv
              title={"Coustomer Count"}
              customercount={11}
              image={Growthcount}
            />
            <CountDiv
              title={"Stock Count"}
              customercount={1}
              image={Growthcount}
            />
          </div>
          <br />
          <br />
          <Piechart />
        </div>
      </div>
    </>
  );
}
