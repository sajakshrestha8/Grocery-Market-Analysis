import Sidebar from "./assets/Components/Sidebar";
import TopSection from "./assets/Components/TopSection";
import UserDataTable from "./assets/Components/UserDataTable";

export default function UserData() {
  return (
    <>
      <TopSection />
      <div className="main-container">
        <Sidebar />
        <UserDataTable />
      </div>
    </>
  );
}
