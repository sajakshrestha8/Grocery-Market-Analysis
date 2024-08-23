import RightContainerDailyData from "./assets/Components/RightContainer-DailyData";
import Sidebar from "./assets/Components/Sidebar";
import TopSection from "./assets/Components/TopSection";

export default function DailyData() {
  return (
    <>
      <TopSection />
      <div className="main-container">
        <Sidebar />
        <RightContainerDailyData />
      </div>
    </>
  );
}
