import React, { useState } from "react";
import * as XLSX from "xlsx";
import axios from "axios";
import Sidebar from "./Sidebar";
import TopSection from "./TopSection";

export default function AnalyticalResult() {
  const [excelData, setExcelData] = useState([]);
  const [results, setResults] = useState(null); // State to store frequent itemsets and rules

  // Function to handle file upload and parsing
  const handleFileUpload = (event) => {
    const file = event.target.files[0];

    const reader = new FileReader();
    reader.onload = (e) => {
      const binaryStr = e.target.result;
      const workbook = XLSX.read(binaryStr, { type: "binary" });

      // Assuming the first sheet
      const sheetName = workbook.SheetNames[0];
      const worksheet = workbook.Sheets[sheetName];

      // Parse the data
      const data = XLSX.utils.sheet_to_json(worksheet, { header: 1 });
      setExcelData(data); // Store the parsed data in state
    };

    reader.readAsBinaryString(file);
  };

  // Convert JSON data to CSV format
  const convertToCSV = (data) => {
    return data.map((row) => row.join(",")).join("\n");
  };

  // Function to handle the POST request using Axios
  const handlePostData = async () => {
    const csvData = convertToCSV(excelData);

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/apriori",
        csvData,
        {
          headers: {
            "Content-Type": "text/csv",
          },
        }
      );

      // Store the response data in state
      setResults(response.data);

      console.log("Response from server:", response.data);
    } catch (error) {
      console.error("Error posting data:", error);
    }
  };

  return (
    <>
      <TopSection />
      <div className="main-container">
        <Sidebar />
        <div className="content-container">
          <h2>Upload Excel File</h2>
          <input type="file" accept=".xlsx, .xls" onChange={handleFileUpload} />
          {/* <div> */}
          {/* <h3>Excel Data:</h3> */}
          {/* <pre>{JSON.stringify(excelData, null, 2)}</pre>{" "} */}
          {/* Display parsed data */}
          {/* </div> */}
          <button onClick={handlePostData}>Post Data to Server</button>

          {results && (
            <div>
              <h3>Frequent Itemsets:</h3>
              <ul>
                {results.frequent_itemsets.map((itemset, index) => (
                  <li key={index}>{itemset.join(", ")}</li>
                ))}
              </ul>

              <h3>Rules:</h3>
              <ul>
                {results.rules.map((rule, index) => (
                  <li key={index}>
                    {rule.antecedent.join(", ")} = {rule.consequent.join(", ")}
                    (Confidence: {rule.confidence.toFixed(2)})
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>
    </>
  );
}
