// import React, { useState } from "react";
// import * as XLSX from "xlsx";
// import axios from "axios";
// import Sidebar from "./Sidebar";
// import TopSection from "./TopSection";

// export default function AnalyticalResult() {
//   const [excelData, setExcelData] = useState([]);
//   const [results, setResults] = useState(null); // State to store frequent itemsets and rules

//   // Function to handle file upload and parsing
//   const handleFileUpload = (event) => {
//     const file = event.target.files[0];

//     const reader = new FileReader();
//     reader.onload = (e) => {
//       const binaryStr = e.target.result;
//       const workbook = XLSX.read(binaryStr, { type: "binary" });

//       // Assuming the first sheet
//       const sheetName = workbook.SheetNames[0];
//       const worksheet = workbook.Sheets[sheetName];

//       // Parse the data
//       const data = XLSX.utils.sheet_to_json(worksheet, { header: 1 });
//       setExcelData(data); // Store the parsed data in state
//     };

//     reader.readAsBinaryString(file);
//   };

//   // Convert JSON data to CSV format
//   const convertToCSV = (data) => {
//     return data.map((row) => row.join(",")).join("\n");
//   };

//   // Function to handle the POST request using Axios
//   const handlePostData = async () => {
//     const csvData = convertToCSV(excelData);

//     try {
//       const response = await axios.post(
//         "http://127.0.0.1:8000/apriori",
//         csvData,
//         {
//           headers: {
//             "Content-Type": "text/csv",
//           },
//         }
//       );

//       // Store the response data in state
//       setResults(response.data);

//       console.log("Response from server:", response.data);
//     } catch (error) {
//       console.error("Error posting data:", error);
//     }
//   };

//   return (
//     <>
//       <TopSection />
//       <div className="main-container">
//         <Sidebar />
//         <div className="content-container">
//           <h2>Upload Excel File</h2>
//           <input type="file" accept=".xlsx, .xls" onChange={handleFileUpload} />
//           {/* <div> */}
//           {/* <h3>Excel Data:</h3> */}
//           {/* <pre>{JSON.stringify(excelData, null, 2)}</pre>{" "} */}
//           {/* Display parsed data */}
//           {/* </div> */}
//           <button onClick={handlePostData}>Post Data to Server</button>

//           {results && (
//             <div>
//               <h3>Frequent Itemsets:</h3>
//               <ul>
//                 {results.frequent_itemsets.map((itemset, index) => (
//                   <li key={index}>{itemset.join(", ")}</li>
//                 ))}
//               </ul>

//               <h3>Rules:</h3>
//               <ul>
//                 {results.rules.map((rule, index) => (
//                   <li key={index}>
//                     {rule.antecedent.join(", ")} = {rule.consequent.join(", ")}
//                     (Confidence: {rule.confidence.toFixed(2)})
//                   </li>
//                 ))}
//               </ul>
//             </div>
//           )}
//         </div>
//       </div>
//     </>
//   );
// }

import React, { useState } from "react";
import axios from "axios";

const MarketBasketAnalysis = () => {
  const [data, setData] = useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();
    const transactions = data
      .trim()
      .split("\n")
      .map((line) => line.trim())
      .filter((line) => line.length > 0);

    if (transactions.length === 0) {
      alert("Please enter some transaction data.");
      return;
    }

    try {
      const response = await axios.post(
        "http://localhost:8000/apriori",
        transactions.join("\n"),
        {
          headers: {
            "Content-Type": "text/plain",
          },
        }
      );

      console.log("Analysis complete:", response.data);
      // Redirect to the results page
      window.location.href = "/results";
    } catch (error) {
      console.error("There was a problem with the fetch operation:", error);
      alert(
        "An error occurred while processing your request. Please try again. Error: " +
          error.message
      );
    }
  };

  return (
    <div className="container mt-5">
      <h1 className="mb-4">Market Basket Analysis</h1>
      <form id="analyze-form" onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="data">
            Enter transactions (comma-separated items per line):
          </label>
          <textarea
            id="data"
            className="form-control"
            rows="10"
            placeholder="Enter each transaction on a new line, with items separated by commas"
            value={data}
            onChange={(e) => setData(e.target.value)}
          />
        </div>
        <button type="submit" className="btn btn-primary">
          Analyze
        </button>
      </form>
    </div>
  );
};

export default MarketBasketAnalysis;
